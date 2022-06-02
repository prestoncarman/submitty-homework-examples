import sys
import unittest
from unittest.mock import patch

import pytest
import submission  # Student code is in submission


class TestMock(unittest.TestCase):
    # Set up a mock for math.sqrt in the student submission.py file
    @patch("submission.math.sqrt")
    def test_sqrt_method_calls(self, mock_math):
        # Alternate return for sqrt mock method
        mock_math.return_value = 32

        # Test call using 16
        number = 16
        result = submission.find_square_root(number)

        # Assert mock was called with 16
        mock_math.assert_called_with(number)

        # Assert the method returned mock return value
        assert result == 32, "Function is not using math.sqrt() return value"


if __name__ == "__main__":
    exit_code = pytest.main(["--tb=short", "--no-header", "grade_submitty.py"])
    print(exit_code, file=sys.stderr)
    sys.exit(int(exit_code.value))
