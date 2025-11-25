"""
Validation script to ensure the application still works after adding tests
This script verifies that:
1. All tests pass
2. Core functionality is intact
3. No breaking changes were introduced
"""
import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a command and return success status"""
    print(f"\n{'='*80}")
    print(f"  {description}")
    print(f"{'='*80}")

    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"✅ {description} - PASSED")
        return True
    else:
        print(f"❌ {description} - FAILED")
        print(f"Error: {result.stderr}")
        return False

def main():
    print("\n" + "="*80)
    print("  Language Mentor - Project Validation Suite")
    print("="*80)

    os.chdir(r"C:\Workspace\AILearning\AgentLearning\Language_Mentor_Learning")

    results = []

    # 1. Run unit tests
    results.append(run_command(
        "python -m pytest src/tests/ -v --tb=short -q",
        "Unit Tests Execution"
    ))

    # 2. Check code coverage
    results.append(run_command(
        "python -m pytest src/tests/ --cov=src --cov-report=term-missing --tb=short -q",
        "Code Coverage Analysis"
    ))

    # 3. Run smoke test
    results.append(run_command(
        "python src/tests/smoke_test.py",
        "Smoke Test - Core Functionality"
    ))

    # Print summary
    print("\n" + "="*80)
    print("  VALIDATION SUMMARY")
    print("="*80)

    total = len(results)
    passed = sum(results)

    print(f"\nTotal Checks: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")

    if passed == total:
        print("\n[SUCCESS] ALL VALIDATIONS PASSED - PROJECT IS HEALTHY!")
        print("\nThe unit tests have been successfully added without breaking")
        print("any existing functionality. The project is ready for use.")
    else:
        print("\n[WARNING] SOME VALIDATIONS FAILED - REVIEW REQUIRED")
        print("\nPlease review the failures above before proceeding.")

    print("="*80 + "\n")

    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())

