import sys

import pytest
import submission


def test_hello_world(record_xml_attribute):
    record_xml_attribute("name", "Function prints 'Hello World!'")
    assert (
        submission.hello_world() == "Hello World!"
    ), "Function return does not match expected"


if __name__ == "__main__":
    exit_code = pytest.main(["--junitxml=bad.xml", "--tb=short", "--no-header", "test_submitty.py"])
    print(exit_code, file=sys.stderr)
    sys.exit(int(exit_code.value))
