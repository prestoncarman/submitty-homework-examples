import sys

import base_class
import derived_class
import pytest


def test_inheritance():
    assert issubclass(
        derived_class.DerivedClass, base_class.BaseClass
    ), "DerivedClass does not inherit BaseClass"


def test_extends__str__():
    test_object = derived_class.DerivedClass()
    result = test_object.__str__()

    assert (
        result == "DerivedClass(BaseClass)"
    ), "DerivedClass __str__() does not return the expected value"


def test_alternate_base_extends__str__():
    test_object = derived_class.DerivedClass()

    # Swap out base class behavior
    test_object._change_test("BaseClassAlternate")

    result = test_object.__str__()

    assert (
        result == "DerivedClass(BaseClassAlternate)"
    ), "DerivedClass __str__() does not used the BaseClass's __str__() to create expected value"


if __name__ == "__main__":
    exit_code = pytest.main(["--tb=short", "--no-header", "grade_submitty.py"])
    print(exit_code, file=sys.stderr)
    sys.exit(int(exit_code.value))
