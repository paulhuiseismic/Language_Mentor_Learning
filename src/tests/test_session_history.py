"""
Unit tests for session_history module
"""
import pytest
from agents.session_history import get_session_history, store
from langchain_core.messages import HumanMessage, AIMessage


class TestSessionHistory:
    """Test session history functionality"""

    def test_get_new_session_history(self, clear_session_store):
        """Test creating a new session history"""
        session_id = "test_session_1"
        history = get_session_history(session_id)

        assert session_id in store
        assert len(history.messages) == 0

    def test_get_existing_session_history(self, clear_session_store):
        """Test retrieving an existing session history"""
        session_id = "test_session_2"

        # Create initial session
        history1 = get_session_history(session_id)
        history1.add_message(HumanMessage(content="Hello"))

        # Retrieve same session
        history2 = get_session_history(session_id)

        assert history1 is history2
        assert len(history2.messages) == 1
        assert history2.messages[0].content == "Hello"

    def test_multiple_sessions(self, clear_session_store):
        """Test managing multiple sessions"""
        session_id_1 = "session_1"
        session_id_2 = "session_2"

        history1 = get_session_history(session_id_1)
        history2 = get_session_history(session_id_2)

        history1.add_message(HumanMessage(content="Message 1"))
        history2.add_message(HumanMessage(content="Message 2"))

        assert len(store) == 2
        assert history1.messages[0].content == "Message 1"
        assert history2.messages[0].content == "Message 2"

    def test_session_message_persistence(self, clear_session_store):
        """Test that messages persist in session"""
        session_id = "test_persistence"
        history = get_session_history(session_id)

        history.add_message(HumanMessage(content="User message"))
        history.add_message(AIMessage(content="AI response"))

        # Retrieve again
        same_history = get_session_history(session_id)

        assert len(same_history.messages) == 2
        assert same_history.messages[0].content == "User message"
        assert same_history.messages[1].content == "AI response"

    def test_clear_session(self, clear_session_store):
        """Test clearing session history"""
        session_id = "test_clear"
        history = get_session_history(session_id)

        history.add_message(HumanMessage(content="Test"))
        assert len(history.messages) == 1

        history.clear()
        assert len(history.messages) == 0

