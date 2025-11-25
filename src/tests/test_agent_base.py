"""
Unit tests for AgentBase class
"""
import pytest
import json
from unittest.mock import MagicMock, patch, Mock
from agents.agent_base import AgentBase


class ConcreteAgent(AgentBase):
    """Concrete implementation of AgentBase for testing"""
    pass


class TestAgentBase:
    """Test AgentBase functionality"""

    def test_init_with_prompt_only(self, sample_prompt_file, mock_chat_model, clear_session_store):
        """Test initialization with only prompt file"""
        agent = ConcreteAgent(
            name="test_agent",
            prompt_file=sample_prompt_file,
            intro_file=None
        )

        assert agent.name == "test_agent"
        assert agent.prompt_file == sample_prompt_file
        assert agent.intro_file is None
        assert agent.session_id == "test_agent"
        assert agent.prompt == "You are a helpful English teacher."
        assert agent.intro_messages == []

    def test_init_with_intro_file(self, sample_prompt_file, sample_intro_file, mock_chat_model, clear_session_store):
        """Test initialization with both prompt and intro files"""
        agent = ConcreteAgent(
            name="test_agent",
            prompt_file=sample_prompt_file,
            intro_file=sample_intro_file
        )

        assert len(agent.intro_messages) == 3
        assert "Hello! Welcome to the session." in agent.intro_messages

    def test_init_with_custom_session_id(self, sample_prompt_file, mock_chat_model, clear_session_store):
        """Test initialization with custom session ID"""
        agent = ConcreteAgent(
            name="test_agent",
            prompt_file=sample_prompt_file,
            session_id="custom_session_123"
        )

        assert agent.session_id == "custom_session_123"

    def test_load_prompt_file_not_found(self, clear_session_store):
        """Test error handling when prompt file is not found"""
        with pytest.raises(FileNotFoundError) as exc_info:
            ConcreteAgent(
                name="test_agent",
                prompt_file="nonexistent_prompt.txt"
            )

        assert "Prompt file" in str(exc_info.value)

    def test_load_intro_file_not_found(self, sample_prompt_file, clear_session_store):
        """Test error handling when intro file is not found"""
        with pytest.raises(FileNotFoundError) as exc_info:
            ConcreteAgent(
                name="test_agent",
                prompt_file=sample_prompt_file,
                intro_file="nonexistent_intro.json"
            )

        assert "Intro file" in str(exc_info.value)

    def test_load_intro_invalid_json(self, sample_prompt_file, tmp_path, clear_session_store):
        """Test error handling when intro file has invalid JSON"""
        invalid_json_file = tmp_path / "invalid.json"
        invalid_json_file.write_text("{ invalid json }", encoding="utf-8")

        with pytest.raises(ValueError) as exc_info:
            ConcreteAgent(
                name="test_agent",
                prompt_file=sample_prompt_file,
                intro_file=str(invalid_json_file)
            )

        assert "invalid" in str(exc_info.value).lower()

    @patch('agents.agent_base.RunnableWithMessageHistory')
    def test_create_chatbot(self, mock_runnable, sample_prompt_file, mock_chat_model, clear_session_store):
        """Test chatbot creation"""
        agent = ConcreteAgent(
            name="test_agent",
            prompt_file=sample_prompt_file
        )

        assert agent.chatbot is not None
        assert agent.chatbot_with_history is not None

    @patch('agents.agent_base.RunnableWithMessageHistory')
    def test_chat_with_history(self, mock_runnable_class, sample_prompt_file, clear_session_store):
        """Test chat with history functionality"""
        # Setup mock
        mock_response = MagicMock()
        mock_response.content = "AI response to user input"

        mock_runnable_instance = MagicMock()
        mock_runnable_instance.invoke.return_value = mock_response
        mock_runnable_class.return_value = mock_runnable_instance

        agent = ConcreteAgent(
            name="test_agent",
            prompt_file=sample_prompt_file
        )

        # Test chat
        response = agent.chat_with_history("Hello, how are you?")

        assert response == "AI response to user input"
        mock_runnable_instance.invoke.assert_called_once()

    @patch('agents.agent_base.RunnableWithMessageHistory')
    def test_chat_with_custom_session_id(self, mock_runnable_class, sample_prompt_file, clear_session_store):
        """Test chat with custom session ID"""
        mock_response = MagicMock()
        mock_response.content = "Custom session response"

        mock_runnable_instance = MagicMock()
        mock_runnable_instance.invoke.return_value = mock_response
        mock_runnable_class.return_value = mock_runnable_instance

        agent = ConcreteAgent(
            name="test_agent",
            prompt_file=sample_prompt_file,
            session_id="default_session"
        )

        response = agent.chat_with_history("Test message", session_id="custom_session")

        assert response == "Custom session response"

        # Verify invoke was called
        mock_runnable_instance.invoke.assert_called_once()

        # Check that custom session_id was passed in config
        call_args = mock_runnable_instance.invoke.call_args
        config_arg = call_args[0][1] if len(call_args[0]) > 1 else call_args[1]
        assert config_arg["configurable"]["session_id"] == "custom_session"

