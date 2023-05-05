import os
from unittest.mock import patch

import grader


def test_log_line():
    message = "Sample log message"
    grader.log_line(message)

    with open("validation_logfile.txt") as logfile:
        assert logfile.read() == message + "\n"

    # Test clean up
    if os.path.exists("validation_logfile.txt"):
        os.remove("validation_logfile.txt")


@patch("sys.exit")
def test_return_result_success(mock_sys_exit):
    grader.return_result(1, "done", "success")
    with open("validation_results.json") as actual_file:
        with open(
            "python_pytest_custom_report/config/custom_validation_code/sample_result_1.json"
        ) as expected_file:
            assert actual_file.read() == expected_file.read()

    # Test clean up
    if os.path.exists("validation_results.json"):
        os.remove("validation_results.json")

    mock_sys_exit.assert_called_with(0)


@patch("sys.exit")
def test_return_result_failure(mock_sys_exit):
    grader.return_result(0, "done", "failure")
    with open("validation_results.json") as actual_file:
        with open(
            "python_pytest_custom_report/config/custom_validation_code/sample_result_3.json"
        ) as expected_file:
            assert actual_file.read() == expected_file.read()

    # Test clean up
    if os.path.exists("validation_results.json"):
        os.remove("validation_results.json")

    mock_sys_exit.assert_called_with(0)


@patch("sys.exit")
def test_return_error(mock_sys_exit):
    grader.return_error("done")
    with open("validation_results.json") as actual_file:
        with open(
            "python_pytest_custom_report/config/custom_validation_code/sample_validation_failure.json"
        ) as expected_file:
            assert actual_file.read() == expected_file.read()

    # Test clean up
    if os.path.exists("validation_results.json"):
        os.remove("validation_results.json")

    mock_sys_exit.assert_called_with(0)


def test_parse_pytest_xml_fail():
    expected = [
        {"name": "Function returns 'Hello World!'", "result": "failure"},
        {"name": "Function returns a string of 12 characters", "result": "failure"},
        {"name": "Function returns string that starts with 'H'", "result": "failure"},
    ]
    actual = grader.parse_pytest_xml(
        ["python_pytest_custom_report/config/custom_validation_code/sample_failure.xml"]
    )
    assert actual == expected


def test_parse_pytest_xml_pass():
    expected = [
        {"name": "Function returns 'Hello World!'", "result": "success"},
        {"name": "Function returns a string of 12 characters", "result": "success"},
        {"name": "Function returns string that starts with 'H'", "result": "success"},
    ]
    actual = grader.parse_pytest_xml(
        ["python_pytest_custom_report/config/custom_validation_code/sample_success.xml"]
    )
    assert actual == expected


def test_print_result_fail():
    actual = grader.get_pytest_results([{"name": "Test 1", "result": "failure"}])
    assert (
        actual == "Tests\n----------------------------------------\n1. FAIL   Test 1\n"
    ), "Single failed test does not return expected output"


def test_print_result_pass():
    pytest_object = [{"name": "Test 1", "result": "success"}]
    actual = grader.get_pytest_results(pytest_object)
    assert (
        actual == "Tests\n----------------------------------------\n1. PASS   Test 1\n"
    ), "Single successful test does not return expected output"


def test_submitty_config():
    actual = grader.get_actual_files(
        "python_pytest_custom_report/config/custom_validation_code/custom_validator_input.json"
    )
    print(actual)
    assert actual == [
        "STDOUT.txt",
        "pytest_results.xml",
    ], "Parsing custom_validator_input.json does not return expected output"


def test_submitty_result_pass():
    tests = [{"name": "My test 1 name", "result": "success"}]
    grader.grade_pytest_results(tests)

    with open("validation_results.json") as actual_file:
        with open(
            "python_pytest_custom_report/config/custom_validation_code/sample_validation_success.json"
        ) as expected_file:
            assert actual_file.read() == expected_file.read()

    # Test clean up
    if os.path.exists("validation_results.json"):
        os.remove("validation_results.json")
    pass


def test_submitty_result_pass_multiple():
    tests = [
        {"name": "My test 1 name", "result": "success"},
        {"name": "My test 2 name", "result": "success"},
    ]
    grader.grade_pytest_results(tests)

    with open("validation_results.json") as actual_file:
        with open(
            "python_pytest_custom_report/config/custom_validation_code/sample_validation_success_multiple.json"
        ) as expected_file:
            assert actual_file.read() == expected_file.read()

    # Test clean up
    if os.path.exists("validation_results.json"):
        os.remove("validation_results.json")
    pass


@patch("sys.exit")
def test_grade_pytest_results(mock_sys_exit):
    pytest_object = [{"name": "Test 1", "result": "success"}]

    grader.grade_pytest_results(pytest_object)
    with open("validation_results.json") as actual_file:
        with open(
            "python_pytest_custom_report/config/custom_validation_code/sample_result_2.json"
        ) as expected_file:
            assert actual_file.read() == expected_file.read()

    # Test clean up
    if os.path.exists("validation_results.json"):
        os.remove("validation_results.json")

    # mock_sys_exit.assert_called_with(0)
