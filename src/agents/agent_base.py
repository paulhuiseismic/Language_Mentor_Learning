import json
from abc import ABC, abstractmethod

from azure_openai import chat_model
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage
from langchain_core.runnables.history import RunnableWithMessageHistory

from agents.session_history import get_session_history
from utils.logger import LOG

class AgentBase(ABC):
    def __init__(self, name, prompt_file, intro_file=None, session_id=None):
        self.name = name
        self.prompt_file = prompt_file
        self.intro_file = intro_file
        self.session_id = session_id if session_id else self.name
        self.prompt = self.load_prompt()
        self.intro_messages = self.load_intro() if self.intro_file else []
        self.create_chatbot()


    def load_prompt(self):
        try:
            with open(self.prompt_file, "r", encoding="utf-8") as file:
                return file.read().strip()
        except FileNotFoundError:
            raise FileNotFoundError(f"Prompt file {self.prompt_file} not found")


    def load_intro(self):
        try:
            with open(self.intro_file, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Intro file {self.intro_file} not found")
        except json.JSONDecodeError:
            raise ValueError(f"Intro file {self.intro_file} is invalid")

    def create_chatbot(self):
        system_prompt = ChatPromptTemplate.from_messages([
            ("system", self.prompt),
            MessagesPlaceholder(variable_name="messages"),
        ])

        self.chatbot = system_prompt | chat_model

        self.chatbot_with_history = RunnableWithMessageHistory(self.chatbot, get_session_history)

    def chat_with_history(self, user_input, session_id=None):
        if session_id is None:
            session_id = self.session_id

        response = self.chatbot_with_history.invoke(
            [HumanMessage(content=user_input)],
            {"configurable": {"session_id": session_id}},
        )

        LOG.debug(f"[ChatBot][{self.name}] {response.content}")
        return response.content