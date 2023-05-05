import sys
import unittest

import code_for_student
import pytest
import student_tests


def test_using_unittest():
    assert issubclass(student_tests.Student_Tests, unittest.TestCase)


def main():
    failure_count = 0
    exit_code = pytest.main(["--tb=short", "--no-header", "grade_submitty.py"])
    if int(exit_code.value) != 0:
        failure_count += 1

    print("\nRunning Student Tests (Expect Success)")
    print("." * 70)

    code_for_student.set_return_value("Hello World!")

    # run expected successful test
    result = unittest.main(
        module=student_tests, exit=False, testRunner=unittest.TextTestRunner(sys.stdout)
    )

    if len(result.result.failures) != 0 or len(result.result.errors) != 0:
        print("Tests failed on expected code solution")
        failure_count += 1

    print("\nRunning Student Tests (Expect Failure)")
    print("." * 70)

    # Reload the test code
    code_for_student.set_return_value("Goodbye!")

    # run expected failing test
    result = unittest.main(
        module=student_tests, exit=False, testRunner=unittest.TextTestRunner(sys.stdout)
    )

    if len(result.result.failures) == 0 and len(result.result.errors) == 0:
        print("Did not find error in code")
        failure_count += 1

    if failure_count == 0:
        print("Test suite passed")
        print("ExitCode.OK", file=sys.stderr)
    else:
        print("Test suite failed (failures={})".format(failure_count))
        print("ExitCode.TESTS_FAILED", file=sys.stderr)
    sys.exit(failure_count)


if __name__ == "__main__":
    main()
