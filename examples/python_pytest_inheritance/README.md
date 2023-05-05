# Python Pytest Inheritance Example

The test check for correctly implementing a `DerivedClass` that should extend the `BaseClass`'s special method `__str__`.

## Tests

* Check inherits `BaseClass`
* Check returned string of `__str__()`
* Check returned string of `__str__()` using an alternate method string

## Solutions

Provided two possible solutions, one using `super().__str__()` and one using our mangled variable name ("cheating").
The cheating method could be prevented by using an alternate `BaseClass` implementation for testing.
