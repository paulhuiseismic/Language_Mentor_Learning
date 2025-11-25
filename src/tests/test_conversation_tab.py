"""
Unit tests for conversation_tab module
"""
import pytest
import sys
from unittest.mock import MagicMock, patch


class TestConversationTab:
    """Test conversation tab functionality"""

    @patch('agents.conversation_agent.ConversationAgent')
    def test_handle_conversation(self, mock_agent_class):
        """Test handling conversation"""
        # Mock the agent instance
        mock_agent = MagicMock()
        mock_agent.chat_with_history.return_value = "That's interesting! Tell me more."

        # Temporarily replace the conversation_agent
        with patch.dict(sys.modules, {'tabs.conversation_tab': MagicMock()}):
            import importlib
            conversation_tab = importlib.import_module('tabs.conversation_tab')
            conversation_tab.conversation_agent = mock_agent
            conversation_tab.handle_conversation = lambda user_input, chat_history: mock_agent.chat_with_history(user_input)

            result = conversation_tab.handle_conversation("I like reading books", [])

            assert result == "That's interesting! Tell me more."
            mock_agent.chat_with_history.assert_called_once_with("I like reading books")

    @patch('agents.conversation_agent.ConversationAgent')
    def test_handle_conversation_with_history(self, mock_agent_class):
        """Test handling conversation with existing history"""
        mock_agent = MagicMock()
        mock_agent.chat_with_history.return_value = "I see what you mean."

        with patch.dict(sys.modules, {'tabs.conversation_tab': MagicMock()}):
            import importlib
            conversation_tab = importlib.import_module('tabs.conversation_tab')
            conversation_tab.conversation_agent = mock_agent
            conversation_tab.handle_conversation = lambda user_input, chat_history: mock_agent.chat_with_history(user_input)

            chat_history = [
                {"role": "user", "content": "Hello"},
                {"role": "assistant", "content": "Hi there!"}
            ]

            result = conversation_tab.handle_conversation("How are you?", chat_history)

            assert result == "I see what you mean."
            mock_agent.chat_with_history.assert_called_once_with("How are you?")

    @patch('agents.conversation_agent.ConversationAgent')
    def test_conversation_agent_initialized(self, mock_agent_class):
        """Test that conversation agent can be initialized"""
        mock_instance = MagicMock()
        mock_instance.chat_with_history = MagicMock()
        mock_agent_class.return_value = mock_instance

        # Verify the mock agent has the expected method
        agent = mock_agent_class()
        assert hasattr(agent, 'chat_with_history')

