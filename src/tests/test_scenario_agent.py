"""
Unit tests for ScenarioAgent class
"""
import pytest
from unittest.mock import MagicMock, patch, mock_open
from agents.scenario_agent import ScenarioAgent
from langchain_core.messages import AIMessage


class TestScenarioAgent:
    """Test ScenarioAgent functionality"""

    @patch('agents.scenario_agent.AgentBase.__init__')
    def test_init_constructs_file_paths(self, mock_super_init, clear_session_store):
        """Test that ScenarioAgent constructs correct file paths"""
        mock_super_init.return_value = None

        agent = ScenarioAgent(scenario_name="job_interview")

        # Verify super().__init__ was called with correct paths
        mock_super_init.assert_called_once()
        call_kwargs = mock_super_init.call_args[1]

        assert call_kwargs['name'] == "job_interview"
        assert call_kwargs['prompt_file'] == "../prompts/job_interview_prompt.txt"
        assert call_kwargs['intro_file'] == "../content/intro/job_interview.json"

    @patch('agents.scenario_agent.AgentBase.__init__')
    def test_init_with_custom_session_id(self, mock_super_init, clear_session_store):
        """Test initialization with custom session ID"""
        mock_super_init.return_value = None

        agent = ScenarioAgent(
            scenario_name="hotel_checkin",
            session_id="custom_hotel_session"
        )

        call_kwargs = mock_super_init.call_args[1]
        assert call_kwargs['session_id'] == "custom_hotel_session"

    @patch('agents.agent_base.RunnableWithMessageHistory')
    @patch('builtins.open', new_callable=mock_open, read_data='You are a hotel receptionist.')
    def test_start_new_session_empty_history(self, mock_file, mock_runnable, tmp_path, clear_session_store):
        """Test starting a new session with empty history"""
        # Create intro file
        intro_file = tmp_path / "hotel_checkin.json"
        intro_file.write_text('["Hello, welcome!", "Good day!"]', encoding="utf-8")

        prompt_file = tmp_path / "hotel_checkin_prompt.txt"
        prompt_file.write_text("You are a hotel receptionist.", encoding="utf-8")

        with patch('agents.scenario_agent.ScenarioAgent.__init__') as mock_init:
            mock_init.return_value = None
            agent = ScenarioAgent.__new__(ScenarioAgent)
            agent.name = "hotel_checkin"
            agent.session_id = "test_session"
            agent.intro_messages = ["Hello, welcome!", "Good day!"]

        initial_message = agent.start_new_session()

        assert initial_message in agent.intro_messages

    @patch('agents.scenario_agent.get_session_history')
    def test_start_new_session_with_existing_history(self, mock_get_history, clear_session_store):
        """Test starting a session when history already exists"""
        # Create mock history with existing messages
        mock_history = MagicMock()
        mock_last_message = MagicMock()
        mock_last_message.content = "Previous message"
        mock_history.messages = [mock_last_message]
        mock_get_history.return_value = mock_history

        with patch('agents.scenario_agent.ScenarioAgent.__init__') as mock_init:
            mock_init.return_value = None
            agent = ScenarioAgent.__new__(ScenarioAgent)
            agent.name = "test_scenario"
            agent.session_id = "existing_session"
            agent.intro_messages = ["Intro message"]

        result = agent.start_new_session()

        assert result == "Previous message"
        # Should not add new message when history exists
        mock_history.add_message.assert_not_called()

    @patch('agents.scenario_agent.get_session_history')
    def test_start_new_session_adds_ai_message(self, mock_get_history, clear_session_store):
        """Test that start_new_session adds AI message to history"""
        mock_history = MagicMock()
        mock_history.messages = []
        mock_get_history.return_value = mock_history

        with patch('agents.scenario_agent.ScenarioAgent.__init__') as mock_init:
            mock_init.return_value = None
            agent = ScenarioAgent.__new__(ScenarioAgent)
            agent.name = "test_scenario"
            agent.session_id = "new_session"
            agent.intro_messages = ["Welcome message"]

        result = agent.start_new_session()

        # Verify AI message was added
        mock_history.add_message.assert_called_once()
        call_args = mock_history.add_message.call_args[0][0]
        assert isinstance(call_args, AIMessage)
        assert call_args.content in agent.intro_messages

    def test_scenario_name_variations(self, clear_session_store):
        """Test that different scenario names construct correct paths"""
        scenarios = ["job_interview", "hotel_checkin", "renting_house", "airport_checkin"]

        for scenario in scenarios:
            with patch('agents.scenario_agent.AgentBase.__init__') as mock_init:
                mock_init.return_value = None
                agent = ScenarioAgent(scenario_name=scenario)

                call_kwargs = mock_init.call_args[1]
                assert scenario in call_kwargs['prompt_file']
                assert scenario in call_kwargs['intro_file']

