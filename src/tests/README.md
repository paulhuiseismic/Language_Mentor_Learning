# Test Suite for Language Mentor
5. Keep tests focused and independent
4. Use descriptive test names
3. Test both success and failure cases
2. Mock external dependencies (APIs, file systems)
1. Write tests before or alongside implementation (TDD)
When adding new features, ensure:

## Writing New Tests

```
  uses: codecov/codecov-action@v3
- name: Upload coverage

  run: pytest --cov=src --cov-report=xml
- name: Run tests

  run: pip install -r requirements.txt
- name: Install dependencies
# Example GitHub Actions
```yaml

These tests can be integrated into CI/CD pipelines:

## CI/CD Integration

- Proper setup and teardown
- Clear test naming conventions
- Comprehensive error case coverage
- No external API calls during testing
- Tests are isolated and independent
### Best Practices

- `clear_session_store`: Ensures clean session state
- `sample_intro_file`: Creates temporary intro JSON files
- `sample_prompt_file`: Creates temporary prompt files
- `mock_azure_openai`: Mocks the Azure OpenAI client
- `mock_chat_model`: Mocks the Azure chat model
### Fixtures

- Session history is cleared between tests to ensure isolation
- File I/O operations are mocked where appropriate
- Azure OpenAI API calls are mocked to avoid actual API usage during testing
### Mocking

## Key Features

- **Integration**: End-to-end workflows across components
- **Logger**: Logging functionality
- **UI Tabs**: All three tab modules (scenario, conversation, vocab)
- **Vocabulary Agent**: Session restart, vocabulary learning workflow
- **Conversation Agent**: Basic conversation functionality
- **Scenario Agent**: Session initialization, intro message selection
- **Agent Base**: Prompt loading, chatbot creation, error handling
- **Session Management**: Session history creation, retrieval, and isolation
The test suite covers:

## Test Coverage

```
pytest -v
```bash
### Run with verbose output

```
pytest -m integration
```bash
### Run only integration tests

```
pytest -m unit
```bash
### Run only unit tests

```
pytest --cov=src --cov-report=html
```bash
### Run with coverage report

```
pytest tests/test_agent_base.py::TestAgentBase::test_init_with_prompt_only
```bash
### Run specific test

```
pytest tests/test_agent_base.py::TestAgentBase
```bash
### Run specific test class

```
pytest tests/test_agent_base.py
```bash
### Run specific test file

```
pytest
```bash
### Run all tests

## Running Tests

```
└── test_integration.py      # Integration tests
├── test_logger.py           # Tests for logging utility
├── test_vocab_tab.py        # Tests for vocab tab UI logic
├── test_conversation_tab.py # Tests for conversation tab UI logic
├── test_scenario_tab.py     # Tests for scenario tab UI logic
├── test_vocab_agent.py      # Tests for vocabulary agent
├── test_conversation_agent.py # Tests for conversation agent
├── test_scenario_agent.py   # Tests for scenario-based agents
├── test_agent_base.py       # Tests for base agent functionality
├── test_session_history.py  # Tests for session history management
├── conftest.py              # Pytest configuration and shared fixtures
tests/
```

## Test Structure

This directory contains comprehensive unit and integration tests for the Language Mentor English learning application.


