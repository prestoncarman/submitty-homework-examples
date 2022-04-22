class DerivedClass():
    def __str__(self):
        return "DerivedClass(BaseClass)"


if __name__ == "__main__":
    test = DerivedClass()
    print(test)
