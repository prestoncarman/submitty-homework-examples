import sys

import pytest

sys.modules["pet"] = __import__("pet_alternate")

import dog  # noqa: E402


def test__str__first_input():
    test_name = "Snow"
    answer = "Calling Snow, my pet and its a dog"
    dog_object = dog.Dog(test_name)
    result = dog_object.__str__()

    assert result == answer


def test__str__second_input():
    test_name = "Flake"
    answer = "Calling Flake, my pet and its a dog"
    dog_object = dog.Dog(test_name)
    result = dog_object.__str__()

    assert result == answer


exit_code = pytest.main(["--tb=short", "--no-header", "submitty_extends_test.py"])
print(exit_code, file=sys.stderr)
