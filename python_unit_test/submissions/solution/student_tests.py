import unittest

import code_for_student_to_test


class Student_Tests(unittest.TestCase):
    def test_output(self):
        result = code_for_student_to_test.hello_world()
        self.assertEqual(result, "Hello World!")


if __name__ == "__main__":
    unittest.main()
