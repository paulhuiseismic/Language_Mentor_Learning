# Quick Reference - Running Tests

## 🚀 Quick Start

```bash
# Navigate to project directory
cd C:\Workspace\AILearning\AgentLearning\Language_Mentor_Learning

# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# View coverage report
start htmlcov/index.html
```

## 📋 Common Commands

### Run All Tests
```bash
pytest
```

### Run Specific Test File
```bash
pytest tests/test_agent_base.py
```

### Run Specific Test Class
```bash
pytest tests/test_agent_base.py::TestAgentBase
```

### Run Specific Test
```bash
pytest tests/test_agent_base.py::TestAgentBase::test_init_with_prompt_only
```

### Run with Verbose Output
```bash
pytest -v
```

### Run Quietly
```bash
pytest -q
```

### Run with Coverage
```bash
pytest --cov=src
```

### Run with HTML Coverage Report
```bash
pytest --cov=src --cov-report=html
```

### Run and Stop on First Failure
```bash
pytest -x
```

### Run Last Failed Tests Only
```bash
pytest --lf
```

## 🔧 Utility Scripts

### Comprehensive Validation
```bash
python validate_project.py
```

### Smoke Test
```bash
python tests/smoke_test.py
```

### Test Runner
```bash
python run_tests.py
```

## 📊 Expected Results

```
57 passed in ~8 seconds
Code Coverage: 83%
```

## ✅ Success Indicators

- All tests show `PASSED` in green
- No errors or failures reported
- Coverage above 80%
- Execution time under 10 seconds

## ❌ Troubleshooting

### If tests fail:
1. Check that you're in the correct directory
2. Ensure virtual environment is activated
3. Verify all dependencies are installed: `pip install -r requirements.txt`
4. Check that Python version is 3.8+

### If import errors occur:
1. Ensure you're running from project root
2. Check PYTHONPATH includes src directory
3. Verify virtual environment is activated

### If coverage is low:
- This is normal for UI components (main.py, tabs/)
- Core logic has 100% coverage
- Overall target is 80%+ (currently at 83%)

## 📖 Documentation

- **Test Guide**: `src/tests/README.md`
- **Test Summary**: `TEST_SUMMARY.md`
- **Implementation**: `IMPLEMENTATION_SUMMARY.md`
- **Project README**: `README.md`
- **Relocation Summary**: `TESTS_RELOCATION_SUMMARY.md`

## 🎯 Test Categories

- **Unit Tests**: Test individual components
- **Integration Tests**: Test component interactions
- **Smoke Tests**: Quick functionality validation

## 💡 Tips

- Run `pytest -v` for detailed output
- Use `pytest -k <keyword>` to run tests matching a keyword
- Use `pytest --markers` to see available test markers
- Check `htmlcov/index.html` for visual coverage report

---
**Quick Help**: Run `pytest --help` for all options

