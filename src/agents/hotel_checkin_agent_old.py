from azure_openai import chat_model
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage
from utils.logger import LOG

from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory
)
from langchain_core.runnables.history import RunnableWithMessageHistory

from agents.base_scenario_agent import ScenarioAgent

store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """
    get or create session history
    :param session_id:
    :return: BaseChatMessageHistory
    """
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


class HotelCheckInAgent(ScenarioAgent):
    """
    Hotel Check-In Scenario Agent
    """
    def __init__(self):
        super().__init__()
        self.name = "Hotel Check-In Agent"

        with open("prompts/hotel_checkin_prompt.txt", "r", encoding="utf-8") as file:
            self.system_prompt = file.read().strip()

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            MessagesPlaceholder(variable_name="messages"),
        ])

        self.chatbot = self.prompt | chat_model

        self.chatbot_with_history = RunnableWithMessageHistory(self.chatbot, get_session_history)

        self.config = {"configurable": {"session_id": "abc123"}}


    def chat(self, user_input: str) -> str:
        """
        chat with user input
        :param user_input:
        :return: response content
        """
        response = self.chatbot.invoke(
            [HumanMessage(content=user_input)],
        )
        return response.content


    def chat_with_history(self, user_input: str) -> str:
        """
        chat with history
        :param user_input:
        :return: response content
        """
        response = self.chatbot_with_history.invoke(
            [HumanMessage(content=user_input)],
            self.config
        )
        LOG.debug(response)
        return response.content