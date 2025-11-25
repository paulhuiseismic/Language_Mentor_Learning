"""
Unit tests for vocab_tab module
"""
import pytest
from unittest.mock import MagicMock, patch, mock_open


class TestVocabTab:
    """Test vocab tab functionality"""

    @patch('builtins.open', new_callable=mock_open, read_data='# Vocabulary Study\nLearn new words!')
    def test_get_page_desc_success(self, mock_file):
        """Test getting page description successfully"""
        from tabs.vocab_tab import get_page_desc

        result = get_page_desc("vocab_study")

        assert result == "# Vocabulary Study\nLearn new words!"

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_get_page_desc_file_not_found(self, mock_file):
        """Test handling of missing page description file"""
        from tabs.vocab_tab import get_page_desc

        result = get_page_desc("nonexistent_feature")

        assert "not found" in result.lower()

    @patch('tabs.vocab_tab.vocab_agent')
    def test_restart_vocab_study_chatbot(self, mock_agent):
        """Test restarting vocab study chatbot"""
        from tabs.vocab_tab import restart_vocab_study_chatbot

        mock_agent.restart_session.return_value = None
        mock_agent.chat_with_history.return_value = "Let's learn 10 new words today!"

        result = restart_vocab_study_chatbot()

        assert result == [{"role": "assistant", "content": "Let's learn 10 new words today!"}]
        mock_agent.restart_session.assert_called_once()
        mock_agent.chat_with_history.assert_called_once_with("Let's do it")

    @patch('tabs.vocab_tab.vocab_agent')
    def test_handle_vocab(self, mock_agent):
        """Test handling vocab interaction"""
        from tabs.vocab_tab import handle_vocab

        mock_agent.chat_with_history.return_value = "Excellent! The word means..."

        result = handle_vocab("What does 'serendipity' mean?", [])

        assert result == "Excellent! The word means..."
        mock_agent.chat_with_history.assert_called_once_with("What does 'serendipity' mean?")

    @patch('tabs.vocab_tab.vocab_agent')
    def test_handle_vocab_with_history(self, mock_agent):
        """Test handling vocab with existing chat history"""
        from tabs.vocab_tab import handle_vocab

        mock_agent.chat_with_history.return_value = "That's correct! Next word..."

        chat_history = [
            {"role": "assistant", "content": "What's the meaning of 'ephemeral'?"},
            {"role": "user", "content": "Lasting for a short time"}
        ]

        result = handle_vocab("Is that right?", chat_history)

        assert result == "That's correct! Next word..."

    def test_vocab_agent_initialized(self):
        """Test that vocab agent is properly initialized"""
        from tabs.vocab_tab import vocab_agent

        assert vocab_agent is not None
        assert hasattr(vocab_agent, 'chat_with_history')
        assert hasattr(vocab_agent, 'restart_session')

    def test_feature_constant(self):
        """Test that feature constant is set correctly"""
        from tabs.vocab_tab import feature

        assert feature == "vocab_study"

