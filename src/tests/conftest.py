"""
Pytest configuration and shared fixtures
"""
import sys
import os
from pathlib import Path

# Add src directory to path (parent of tests)
src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

import pytest
from unittest.mock import MagicMock, patch


@pytest.fixture
def mock_chat_model():
    """Mock chat model to avoid actual API calls"""
    with patch('azure_openai.chat_model') as mock:
        mock_response = MagicMock()
        mock_response.content = "Mock AI response"
        mock.invoke.return_value = mock_response
        yield mock


@pytest.fixture
def mock_azure_openai():
    """Mock Azure OpenAI client"""
    with patch('azure_openai.client') as mock:
        yield mock


@pytest.fixture
def sample_prompt_file(tmp_path):
    """Create a temporary prompt file"""
    prompt_file = tmp_path / "test_prompt.txt"
    prompt_file.write_text("You are a helpful English teacher.", encoding="utf-8")
    return str(prompt_file)


@pytest.fixture
def sample_intro_file(tmp_path):
    """Create a temporary intro JSON file"""
    import json
    intro_file = tmp_path / "test_intro.json"
    intro_data = [
        "Hello! Welcome to the session.",
        "Hi there! Let's get started.",
        "Greetings! Ready to practice?"
    ]
    intro_file.write_text(json.dumps(intro_data), encoding="utf-8")
    return str(intro_file)


@pytest.fixture
def clear_session_store():
    """Clear the session history store before and after tests"""
    from agents.session_history import store
    store.clear()
    yield
    store.clear()

