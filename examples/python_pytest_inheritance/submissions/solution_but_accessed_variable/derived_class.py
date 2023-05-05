import base_class


class DerivedClass(base_class.BaseClass):
    def __str__(self):
        # Value using mangled name instead of super().__str__()
        # Submitter must know the internal BaseClass variable name
        return "DerivedClass({})".format(self._BaseClass__test)


if __name__ == "__main__":
    test = DerivedClass()
    print(test)
