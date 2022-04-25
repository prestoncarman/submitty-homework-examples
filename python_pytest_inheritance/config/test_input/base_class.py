# See solution for assignment supplied `BaseClass`
#
# This version of `BaseClass` is used for testing to allow for alternate `__str__()` text
class BaseClass:
    def __init__(self):
        self.__test = "BaseClass"

    def _change_test(self, value):
        self.__test = value

    def __str__(self):
        return self.__test
