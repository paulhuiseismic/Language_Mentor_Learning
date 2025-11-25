#!/usr/bin/env python3
"""
Test runner script for Language Mentor application
"""
import sys
import subprocess
from pathlib import Path


def main():
    """Run the test suite with coverage"""

    # Get the project root
    project_root = Path(__file__).parent

    print("=" * 80)
    print("Running Language Mentor Test Suite")
    print("=" * 80)
    print()

    # Install test dependencies if needed
    print("Checking test dependencies...")
    try:
        import pytest
        import pytest_cov
        import pytest_mock
        print("✓ Test dependencies are installed")
    except ImportError:
        print("Installing test dependencies...")
        subprocess.run([
            sys.executable, "-m", "pip", "install",
            "pytest", "pytest-cov", "pytest-mock"
        ], check=True)

    print()
    print("Running tests...")
    print("-" * 80)

    # Run pytest with coverage
    result = subprocess.run([
        sys.executable, "-m", "pytest",
        "src/tests/",
        "-v",
        "--cov=src",
        "--cov-report=term-missing",
        "--cov-report=html",
        "--tb=short"
    ], cwd=project_root)

    print()
    print("=" * 80)

    if result.returncode == 0:
        print("✓ All tests passed!")
        print()
        print("Coverage report generated in htmlcov/index.html")
    else:
        print("✗ Some tests failed")
        print()
        print("Please review the failures above")

    print("=" * 80)

    return result.returncode


if __name__ == "__main__":
    sys.exit(main())

