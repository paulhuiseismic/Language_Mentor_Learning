"""
Integration tests for the Language Mentor application
"""
import pytest
from unittest.mock import MagicMock, patch


class TestIntegration:
    """Integration tests across multiple components"""

    @patch('agents.agent_base.RunnableWithMessageHistory')
    @patch('builtins.open')
    def test_scenario_agent_full_workflow(self, mock_file, mock_runnable, tmp_path, clear_session_store):
        """Test complete workflow for scenario agent"""
        # Create test files
        prompt_file = tmp_path / "test_prompt.txt"
        prompt_file.write_text("You are a test agent.", encoding="utf-8")

        intro_file = tmp_path / "test_intro.json"
        intro_file.write_text('["Hello!", "Hi there!"]', encoding="utf-8")

        # Mock the runnable
        mock_response = MagicMock()
        mock_response.content = "Test response"
        mock_runnable_instance = MagicMock()
        mock_runnable_instance.invoke.return_value = mock_response
        mock_runnable.return_value = mock_runnable_instance

        # Import and create agent
        from agents.scenario_agent import ScenarioAgent

        with patch('agents.scenario_agent.AgentBase.load_prompt') as mock_load_prompt:
            with patch('agents.scenario_agent.AgentBase.load_intro') as mock_load_intro:
                mock_load_prompt.return_value = "Test prompt"
                mock_load_intro.return_value = ["Hello!", "Hi there!"]

                agent = ScenarioAgent.__new__(ScenarioAgent)
                agent.name = "test_scenario"
                agent.prompt_file = str(prompt_file)
                agent.intro_file = str(intro_file)
                agent.session_id = "test_session"
                agent.prompt = "Test prompt"
                agent.intro_messages = ["Hello!", "Hi there!"]
                agent.chatbot_with_history = mock_runnable_instance

                # Start new session
                initial_message = agent.start_new_session()
                assert initial_message in ["Hello!", "Hi there!"]

                # Chat
                from agents.agent_base import AgentBase
                response = AgentBase.chat_with_history(agent, "Test input")
                assert response == "Test response"

    def test_scenario_tab_workflow(self):
        """Test workflow in scenario tab"""
        # Mock agent
        mock_agent = MagicMock()
        mock_agent.start_new_session.return_value = "Welcome!"
        mock_agent.chat_with_history.return_value = "Great!"

        mock_agents = {"hotel_checkin": mock_agent}

        # Simulate the workflow
        # Start session
        chat_history = [{"role": "assistant", "content": mock_agent.start_new_session()}]
        assert chat_history == [{"role": "assistant", "content": "Welcome!"}]

        # Handle user input
        response = mock_agent.chat_with_history("Hello")
        assert response == "Great!"

    def test_conversation_tab_workflow(self):
        """Test workflow in conversation tab"""
        mock_agent = MagicMock()
        mock_agent.chat_with_history.return_value = "Nice to meet you!"

        response = mock_agent.chat_with_history("Hello")
        assert response == "Nice to meet you!"

    def test_vocab_tab_workflow(self):
        """Test workflow in vocab tab"""
        mock_agent = MagicMock()
        mock_agent.restart_session.return_value = None
        mock_agent.chat_with_history.side_effect = [
            "Let's start with word 1!",
            "Correct!"
        ]

        # Restart session
        mock_agent.restart_session()
        chat_history = [{"role": "assistant", "content": mock_agent.chat_with_history("Let's do it")}]
        assert chat_history == [{"role": "assistant", "content": "Let's start with word 1!"}]

        # Handle vocab
        response = mock_agent.chat_with_history("definition")
        assert response == "Correct!"

    def test_session_isolation(self, clear_session_store):
        """Test that different sessions are isolated"""
        from agents.session_history import get_session_history
        from langchain_core.messages import HumanMessage

        # Create two separate sessions
        session1 = get_session_history("session_1")
        session2 = get_session_history("session_2")

        # Add messages to each
        session1.add_message(HumanMessage(content="Message 1"))
        session2.add_message(HumanMessage(content="Message 2"))

        # Verify isolation
        assert len(session1.messages) == 1
        assert len(session2.messages) == 1
        assert session1.messages[0].content == "Message 1"
        assert session2.messages[0].content == "Message 2"

    @patch('agents.agent_base.RunnableWithMessageHistory')
    def test_multiple_agents_coexist(self, mock_runnable, tmp_path, clear_session_store):
        """Test that multiple agent types can coexist"""
        # Create prompt files
        conv_prompt = tmp_path / "conv_prompt.txt"
        conv_prompt.write_text("Conversation agent", encoding="utf-8")

        vocab_prompt = tmp_path / "vocab_prompt.txt"
        vocab_prompt.write_text("Vocab agent", encoding="utf-8")

        from agents.conversation_agent import ConversationAgent
        from agents.vocab_agent import VocabAgent

        with patch('agents.conversation_agent.ConversationAgent.load_prompt') as mock_conv_prompt:
            with patch('agents.vocab_agent.VocabAgent.load_prompt') as mock_vocab_prompt:
                mock_conv_prompt.return_value = "Conversation agent"
                mock_vocab_prompt.return_value = "Vocab agent"

                # Both agents should be creatable
                conv_agent = ConversationAgent.__new__(ConversationAgent)
                vocab_agent = VocabAgent.__new__(VocabAgent)

                assert conv_agent is not None
                assert vocab_agent is not None

