import random

from langchain_core.messages import AIMessage

from agents.session_history import get_session_history
from agents.agent_base import AgentBase
from utils.logger import LOG

class ScenarioAgent(AgentBase):
    """
    Scenario Agent
    """
    def __init__(self, scenario_name: str, session_id: str = None):
        prompt_file = f"../prompts/{scenario_name}_prompt.txt"
        intro_file = f"../content/intro/{scenario_name}.json"
        super().__init__(
            name=scenario_name,
            prompt_file=prompt_file,
            intro_file=intro_file,
            session_id=session_id
        )

    def start_new_session(self, session_id: str = None):
        """
        Start a new chat session with intro messages
        :param session_id:
        """
        if session_id is None:
            session_id = self.session_id

        history = get_session_history(session_id)
        LOG.debug(f"[history][{session_id}]: {history}")

        if not history.messages:
            initial_ai_message = random.choice(self.intro_messages)
            history.add_message(AIMessage(content=initial_ai_message))
            return initial_ai_message
        else:
            return history.messages[-1].content
