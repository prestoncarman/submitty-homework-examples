import unittest

import code_for_student


class Student_Tests(unittest.TestCase):
    def test_output(self):
        result = code_for_student.hello_world()
        self.assertEqual(result, "Hello World!")


if __name__ == "__main__":
    unittest.main()
