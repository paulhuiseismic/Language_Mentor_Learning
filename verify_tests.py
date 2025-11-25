"""
Final verification script to confirm all tests work after relocation
"""
import subprocess
import sys

def run_test(description, command):
    """Run a test command and report results"""
    print(f"\n{'='*80}")
    print(f"Testing: {description}")
    print(f"{'='*80}")

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60
        )

        # Check for test results in output
        output = result.stdout + result.stderr

        if result.returncode == 0:
            print(f"[PASS] {description}")

            # Extract test count if available
            if "passed" in output:
                for line in output.split('\n'):
                    if "passed" in line:
                        print(f"  Result: {line.strip()}")
                        break
            return True
        else:
            print(f"[FAIL] {description}")
            if output:
                print(f"  Output: {output[:200]}")
            return False

    except subprocess.TimeoutExpired:
        print(f"[TIMEOUT] {description}")
        return False
    except Exception as e:
        print(f"[ERROR] {description}: {str(e)}")
        return False

def main():
    print("\n" + "="*80)
    print("COMPREHENSIVE TEST VERIFICATION")
    print("Testing relocated tests in src/tests/")
    print("="*80)

    tests = [
        ("Collect all tests", "python -m pytest src/tests/ --collect-only -q"),
        ("Run all tests", "python -m pytest src/tests/ -q"),
        ("Run with coverage", "python -m pytest src/tests/ --cov=src -q"),
        ("Run specific test file", "python -m pytest src/tests/test_session_history.py -q"),
        ("Run integration tests", "python -m pytest src/tests/test_integration.py -q"),
    ]

    results = []
    for description, command in tests:
        result = run_test(description, command)
        results.append((description, result))

    # Summary
    print("\n" + "="*80)
    print("VERIFICATION SUMMARY")
    print("="*80)

    passed = sum(1 for _, r in results if r)
    total = len(results)

    for description, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} {description}")

    print("\n" + "-"*80)
    print(f"Results: {passed}/{total} tests passed")

    if passed == total:
        print("\n[SUCCESS] All verification tests passed!")
        print("Tests are working correctly in src/tests/")
        return 0
    else:
        print(f"\n[WARNING] {total - passed} verification test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())

