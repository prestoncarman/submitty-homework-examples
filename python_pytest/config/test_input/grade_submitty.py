import sys

import pytest
import submission


def test_hello_world():
    assert (
        submission.hello_world() == "Hello World!"
    ), "Function return does not match expected"


if __name__ == "__main__":
    exit_code = pytest.main(["--tb=short", "--no-header", "grade_submitty.py"])
    print(exit_code, file=sys.stderr)
    sys.exit(int(exit_code.value))
