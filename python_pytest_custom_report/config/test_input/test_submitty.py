import sys

import pytest
import submission


def test_hello_world(record_xml_attribute):
    record_xml_attribute("name", "Function returns 'Hello World!'")
    assert (
        submission.hello_world() == "Hello World!"
    ), "Function return does not match expected value"

def test_hello_world_length(record_xml_attribute):
    record_xml_attribute("name", "Function returns a string of 12 characters")
    assert (
        len(submission.hello_world()) == 12
    ), "Function return does not match expected string length"

def test_hello_world_first_character(record_xml_attribute):
    record_xml_attribute("name", "Function returns string that starts with 'H'")
    assert (
        submission.hello_world()[0] == "H"
    ), "Function return does not start with 'H'"


if __name__ == "__main__":
    exit_code = pytest.main(["--junitxml=pytest_results.xml", "--tb=short", "--no-header", "test_submitty.py"])
    print(exit_code, file=sys.stderr)
    sys.exit(int(exit_code.value))
