"""
Unit tests for ConversationAgent class
"""
import pytest
from unittest.mock import MagicMock, patch
from agents.conversation_agent import ConversationAgent


class TestConversationAgent:
    """Test ConversationAgent functionality"""

    @patch('agents.conversation_agent.AgentBase.__init__')
    def test_init_default_session(self, mock_super_init, clear_session_store):
        """Test initialization with default session"""
        mock_super_init.return_value = None

        agent = ConversationAgent()

        # Verify super().__init__ was called with correct parameters
        mock_super_init.assert_called_once()
        call_kwargs = mock_super_init.call_args[1]

        assert call_kwargs['name'] == "conversation"
        assert call_kwargs['prompt_file'] == "../prompts/conversation_prompt.txt"
        assert call_kwargs['session_id'] is None

    @patch('agents.conversation_agent.AgentBase.__init__')
    def test_init_custom_session(self, mock_super_init, clear_session_store):
        """Test initialization with custom session ID"""
        mock_super_init.return_value = None

        agent = ConversationAgent(session_id="custom_conversation_session")

        call_kwargs = mock_super_init.call_args[1]
        assert call_kwargs['session_id'] == "custom_conversation_session"

    @patch('agents.agent_base.RunnableWithMessageHistory')
    @patch('builtins.open')
    def test_conversation_agent_inherits_chat_functionality(self, mock_file, mock_runnable, tmp_path, clear_session_store):
        """Test that ConversationAgent can use inherited chat functionality"""
        # Create temporary prompt file
        prompt_file = tmp_path / "conversation_prompt.txt"
        prompt_file.write_text("You are a friendly conversation partner.", encoding="utf-8")

        mock_response = MagicMock()
        mock_response.content = "Nice to meet you!"

        mock_runnable_instance = MagicMock()
        mock_runnable_instance.invoke.return_value = mock_response
        mock_runnable.return_value = mock_runnable_instance

        with patch('agents.conversation_agent.ConversationAgent.__init__') as mock_init:
            mock_init.return_value = None
            agent = ConversationAgent.__new__(ConversationAgent)
            agent.name = "conversation"
            agent.session_id = "test_conv_session"
            agent.chatbot_with_history = mock_runnable_instance

        # Manually call the parent's chat method
        from agents.agent_base import AgentBase
        response = AgentBase.chat_with_history(agent, "Hello!")

        assert response == "Nice to meet you!"

    def test_no_intro_file_required(self, clear_session_store):
        """Test that ConversationAgent doesn't require intro file"""
        with patch('agents.conversation_agent.AgentBase.__init__') as mock_init:
            mock_init.return_value = None

            agent = ConversationAgent()

            call_kwargs = mock_init.call_args[1]
            # ConversationAgent should not pass intro_file
            assert 'intro_file' not in call_kwargs or call_kwargs.get('intro_file') is None

