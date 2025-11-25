"""
Unit tests for VocabAgent class
"""
import pytest
from unittest.mock import MagicMock, patch
from agents.vocab_agent import VocabAgent


class TestVocabAgent:
    """Test VocabAgent functionality"""

    @patch('agents.vocab_agent.AgentBase.__init__')
    def test_init_default_session(self, mock_super_init, clear_session_store):
        """Test initialization with default session"""
        mock_super_init.return_value = None

        agent = VocabAgent()

        # Verify super().__init__ was called with correct parameters
        mock_super_init.assert_called_once()
        call_kwargs = mock_super_init.call_args[1]

        assert call_kwargs['name'] == "vocab_study"
        assert call_kwargs['prompt_file'] == "../prompts/vocab_study_prompt.txt"
        assert call_kwargs['session_id'] is None

    @patch('agents.vocab_agent.AgentBase.__init__')
    def test_init_custom_session(self, mock_super_init, clear_session_store):
        """Test initialization with custom session ID"""
        mock_super_init.return_value = None

        agent = VocabAgent(session_id="custom_vocab_session")

        call_kwargs = mock_super_init.call_args[1]
        assert call_kwargs['session_id'] == "custom_vocab_session"

    @patch('agents.vocab_agent.get_session_history')
    def test_restart_session_clears_history(self, mock_get_history, clear_session_store):
        """Test that restart_session clears the history"""
        mock_history = MagicMock()
        mock_get_history.return_value = mock_history

        with patch('agents.vocab_agent.VocabAgent.__init__') as mock_init:
            mock_init.return_value = None
            agent = VocabAgent.__new__(VocabAgent)
            agent.name = "vocab_study"
            agent.session_id = "test_vocab_session"

        result = agent.restart_session()

        # Verify get_session_history was called
        mock_get_history.assert_called_once_with("test_vocab_session")

        # Verify clear was called
        mock_history.clear.assert_called_once()

        # Verify it returns the history
        assert result == mock_history

    @patch('agents.vocab_agent.get_session_history')
    def test_restart_session_with_custom_session_id(self, mock_get_history, clear_session_store):
        """Test restart_session with custom session ID"""
        mock_history = MagicMock()
        mock_get_history.return_value = mock_history

        with patch('agents.vocab_agent.VocabAgent.__init__') as mock_init:
            mock_init.return_value = None
            agent = VocabAgent.__new__(VocabAgent)
            agent.name = "vocab_study"
            agent.session_id = "default_session"

        result = agent.restart_session(session_id="specific_session")

        # Verify the specific session ID was used
        mock_get_history.assert_called_once_with("specific_session")
        mock_history.clear.assert_called_once()

    @patch('agents.vocab_agent.get_session_history')
    def test_restart_session_uses_default_session_id(self, mock_get_history, clear_session_store):
        """Test that restart_session uses default session_id when none provided"""
        mock_history = MagicMock()
        mock_get_history.return_value = mock_history

        with patch('agents.vocab_agent.VocabAgent.__init__') as mock_init:
            mock_init.return_value = None
            agent = VocabAgent.__new__(VocabAgent)
            agent.name = "vocab_study"
            agent.session_id = "my_default_session"

        agent.restart_session()

        mock_get_history.assert_called_once_with("my_default_session")

    def test_no_intro_file_required(self, clear_session_store):
        """Test that VocabAgent doesn't require intro file"""
        with patch('agents.vocab_agent.AgentBase.__init__') as mock_init:
            mock_init.return_value = None

            agent = VocabAgent()

            call_kwargs = mock_init.call_args[1]
            # VocabAgent should not pass intro_file
            assert 'intro_file' not in call_kwargs or call_kwargs.get('intro_file') is None

