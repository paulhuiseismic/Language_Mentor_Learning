from langchain_core.messages import AIMessage

from agents.session_history import get_session_history
from agents.agent_base import AgentBase
from utils.logger import LOG


class ConversationAgent(AgentBase):
    """
    Conversation Agent with history
    """
    def __init__(self, session_id=None):
        super().__init__(
            name="conversation",
            prompt_file="../prompts/conversation_prompt.txt",
            session_id=session_id
        )