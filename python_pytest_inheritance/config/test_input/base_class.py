class BaseClass:
    def __init__(self):
        self.__test = "BaseClass"

    def _change_test(self, value):
        self.__test = value

    def __str__(self):
        return self.__test

    # Version of __str__() supplied with assignment
    # def __str__(self):
    #     return "BaseClass"
