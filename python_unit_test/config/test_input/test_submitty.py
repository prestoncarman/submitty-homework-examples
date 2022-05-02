import importlib
import sys
import unittest

import code_for_student_to_test
import pytest
import student_tests


def test_using_unittest():
    assert issubclass(student_tests.Student_Tests, unittest.TestCase)


if __name__ == "__main__":
    successful_test = True
    exit_code = pytest.main(["--tb=short", "--no-header", "test_submitty.py"])
    if int(exit_code.value) != 0:
        successful_test = False

    print("\nRunning Student Tests (Expect Success)")
    print("." * 70)

    # run expected successful test
    result = unittest.main(
        module=student_tests, exit=False, testRunner=unittest.TextTestRunner(sys.stdout)
    )

    if len(result.result.failures) != 0 or len(result.result.errors) != 0:
        print("Tests failed on expected code solution")
        successful_test = False

    print("\nRunning Student Tests (Expect Failure)")
    print("." * 70)

    # Reload the test code
    del sys.modules["code_for_student_to_test"]
    sys.modules["code_for_student_to_test"] = __import__(
        "code_for_student_to_test_failing"
    )
    importlib.reload(student_tests)

    # run expected failing test
    result = unittest.main(
        module=student_tests, exit=False, testRunner=unittest.TextTestRunner(sys.stdout)
    )

    if len(result.result.failures) == 0 and len(result.result.errors) == 0:
        print("Did not find error in code")
        successful_test = False

    if successful_test:
        print("ExitCode.OK", file=sys.stderr)
    else:
        print("ExitCode.TESTS_FAILED", file=sys.stderr)
    sys.exit(0 if successful_test else 1)
