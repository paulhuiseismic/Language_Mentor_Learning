import json
import random

from azure_openai import chat_model
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables.history import RunnableWithMessageHistory

from agents.session_history import get_session_history
from utils.logger import LOG

class ScenarioAgent:
    """
    Base Scenario Agent
    """
    def __init__(self, scenario_name: str):
        self.name = scenario_name
        self.prompt_file = f"prompts/{self.name}_prompt.txt"
        self.intro_file = f"content/intro/{self.name}.json"
        self.prompt = self.load_prompt()
        self.intro_messages = self.load_intro()

        self.create_chatbot()


    def load_prompt(self):
        """
        Load system prompt from file
        """
        try:
            with open(self.prompt_file, "r", encoding="utf-8") as file:
                return file.read().strip()
        except FileNotFoundError:
            raise FileNotFoundError(f"Prompt file {self.prompt_file} not found.")

    def load_intro(self):
        """
        Load scenario introduction from JSON file
        """
        try:
            with open(self.intro_file, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Intro file {self.intro_file} not found.")
        except json.JSONDecodeError:
            raise ValueError(f"Intro file {self.intro_file} is not a valid JSON.")

    def create_chatbot(self):
        """
        Create chatbot with prompt and history
        """
        system_prompt = ChatPromptTemplate.from_messages([
            ("system", self.prompt),
            MessagesPlaceholder(variable_name="messages"),
        ])
        self.chatbot = system_prompt | chat_model

        self.chatbot_with_history = RunnableWithMessageHistory(self.chatbot, get_session_history)

    def start_new_session(self, session_id: str = None):
        """
        Start a new chat session with intro messages
        :param session_id:
        """
        if session_id is None:
            session_id = self.name

        history = get_session_history(session_id)
        LOG.debug(f"[history]: {history}")

        if not history.messages:
            initial_ai_message = random.choice(self.intro_messages)
            history.add_message(AIMessage(content=initial_ai_message))
            return initial_ai_message
        else:
            return history.messages[-1].content

    def chat_with_history(self, user_input: str, session_id: str = None) -> str:
        """
        Chat with user input and history
        :param user_input:
        :param session_id:
        :return: response content
        """
        if session_id is None:
            session_id = self.name

        response = self.chatbot_with_history.invoke(
            [HumanMessage(content=user_input)],
            {"configurable": {"session_id": session_id}},
        )
        LOG.debug(response)
        return response.content
