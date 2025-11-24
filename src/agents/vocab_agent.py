from langchain_core.messages import AIMessage

from agents.session_history import get_session_history
from agents.agent_base import AgentBase
from utils.logger import LOG

class VocabAgent(AgentBase):
    def __init__(self, session_id=None):
        super().__init__(
            name="vocab_study",
            prompt_file="../prompts/vocab_study_prompt.txt",
            session_id=session_id
        )

    def restart_session(self, session_id=None):
        if session_id is None:
            session_id = self.session_id

        history = get_session_history(session_id)
        history.clear()
        LOG.debug(f"[history][{session_id}]: {history}")

        return history