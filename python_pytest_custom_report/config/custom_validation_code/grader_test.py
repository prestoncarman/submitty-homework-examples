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
def test_return_result(mock_sys_exit):
    expected_json = '{\n    "status": "success",\n    "data": {\n        "score": 1,\n        "message": "done",\n        "status": "success"\n    }\n}'

    grader.return_result(1, "done", "success")
    with open("validation_results.json") as jsonfile:
        assert jsonfile.read() == expected_json

    # Test clean up
    if os.path.exists("validation_results.json"):
        os.remove("validation_results.json")

    mock_sys_exit.assert_called_with(0)


@patch("sys.exit")
def test_return_error(mock_sys_exit):
    expected_json = '{\n    "status": "fail",\n    "message": "done"\n}'

    grader.return_error("done")
    with open("validation_results.json") as jsonfile:
        assert jsonfile.read() == expected_json

    # Test clean up
    if os.path.exists("validation_results.json"):
        os.remove("validation_results.json")

    mock_sys_exit.assert_called_with(0)


def test_parse_pytest_xml_fail():
    expected = [
        {"name": "Function returns 'Hello World!'", "result": False},
        {"name": "Function returns a string of 12 characters", "result": False},
        {"name": "Function returns string that starts with 'H'", "result": False},
    ]
    actual = grader.parse_pytest_xml(
        "python_pytest_custom_report/config/custom_validation_code/sample_failure.xml"
    )
    assert actual == expected


def test_parse_pytest_xml_pass():
    expected = [
        {"name": "Function returns 'Hello World!'", "result": True},
        {"name": "Function returns a string of 12 characters", "result": True},
        {"name": "Function returns string that starts with 'H'", "result": True},
    ]
    actual = grader.parse_pytest_xml(
        "python_pytest_custom_report/config/custom_validation_code/sample_success.xml"
    )
    assert actual == expected


def test_print_result_fail():
    actual = grader.get_pytest_results([{"name": "Test 1", "result": False}])
    assert (
        actual == "Tests\n----------------------------------------\n1. FAIL   Test 1\n"
    ), "Single failed test does not return expected output"


def test_print_result_pass():
    pytest_object = [{"name": "Test 1", "result": True}]
    actual = grader.get_pytest_results(pytest_object)
    assert (
        actual == "Tests\n----------------------------------------\n1. PASS   Test 1\n"
    ), "Single successful test does not return expected output"


@patch("sys.exit")
def test_grade_pytest_results(mock_sys_exit):
    pytest_object = [{"name": "Test 1", "result": True}]
    expected_json = '{\n    "status": "success",\n    "data": {\n        "score": 1,\n        "message": "Test 1",\n        "status": "success"\n    }\n}'

    grader.grade_pytest_results(pytest_object)
    with open("validation_results.json") as jsonfile:
        assert jsonfile.read() == expected_json

    # Test clean up
    if os.path.exists("validation_results.json"):
        os.remove("validation_results.json")

    # mock_sys_exit.assert_called_with(0)
