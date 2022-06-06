"""
This file presents an example of a python custom validator connected with a pytest gradeable for use in your Submitty assignment.
Building on the Submitty example: https://github.com/Submitty/Submitty/tree/main/more_autograding_examples/python_custom_validation

While the example assignment is printing "Hello World!", the custom validation could be used for any pytest XML output file.

To test that the pytest XML output, the grade_submitty.py creates a pytest_results.xml file to be processed by the custom validator.

To read this file, begin at the bottom with do_the_grading, then progress to
grade_a_single_file. If you are interested, you may also examine the return_result
functions and the get_actual_files and get_pytest_results helper function or you may just copy them.

If you are interested in parsing command line arguments, examine the parse_args function.
"""

import argparse
import json
import os
import sys
import traceback
import xml.etree.ElementTree as ET

"""
This is the agreed upon name for the input data to the custom validator.
This is identical to the validation blob for this validator, plus the
value 'testcase_prefix', which denotes the testcase that is to be processed.
"""
GLOBAL_INPUT_JSON_PATH = "custom_validator_input.json"


# def parse_args():
#     """
#     A simple argument parsing function.

#     This function is not necessary, but can be used as a template to help process command line arguments.
#     """
#     parser = argparse.ArgumentParser()
#     parser.add_argument(
#         "-n",
#         "--numbers",
#         required=True,
#         help="The number of numbers we expect",
#         type=int,
#     )
#     return parser.parse_args()


class ValidationResults:
    def __init__(self):
        self.score = 1
        self.data = []

    def set_score(self, score):
        """
        Change the score
        """
        self.score = score

    def add_message(self, message, status):
        """
        Add a message to the list.
        """
        # Status can be 'information', 'failure', 'warning' or 'success'.
        self.data.append(
            {
                "message": message,
                "status": status,
            }
        )

    def get_success_result(self):
        """
        Build result object
        """
        result = {
            "status": "success",
            "data": {
                "score": self.score,
            },
        }
        if len(self.data) == 1:
            # Only one message to add
            result["data"]["message"] = self.data[0]["message"]
            result["data"]["status"] = self.data[0]["status"]
        else:
            # Add all messages
            result["data"]["message"] = self.data
        return result

    def write_file_success(self):
        result = self.get_success_result()
        self.write_file(result)

    def write_file(self, result):
        # Dump the results to validation_results.json as expected by Submitty.
        with open("validation_results.json", "w") as outfile:
            json.dump(result, outfile, indent=4)

    def write_file_error(self, error_message):
        result = {
            "status": "fail",
            "message": error_message,
        }
        self.write_file(result)


"""
Helper functions for returning a score to the student.
"""


def log_line(line):
    """
    Write a line to an instructor log file.
    """
    mode = "a" if os.path.exists("validation_logfile.txt") else "w"

    with open("validation_logfile.txt", mode) as outfile:
        outfile.write(line + "\n")


def return_result(score, message, status):
    """
    Return a non-error result to the student.
    """
    vr = ValidationResults()
    vr.set_score(score)
    vr.add_message(message, status)
    vr.write_file_success()
    # End the program, because we have returned a result.
    sys.exit(0)


def return_error(error_message):
    """
    This function should be used to return an error if the validator crashes.

    If this function is called, the student will receive a score of zero.
    """
    vr = ValidationResults()
    vr.write_file_error(error_message)
    # End the program, because we have returned a result.
    sys.exit(0)


# def get_actual_files():
#     """
#     A helper function written to load in actual files.

#     To find actual files, we look for all of the files listed in the
#     'actual_file' section of this validator.
#     """
#     try:
#         # Open the custom_validator_input.json that we specified in our config.
#         with open(GLOBAL_INPUT_JSON_PATH) as json_file:
#             testcase = json.load(json_file)
#             # Grab the folder housing the files.
#             prefix = testcase["testcase_prefix"]
#     except Exception:
#         return_error("Could not open custom_validator_input.json")

#     # There can be either one actual file (a string) or a list of actual files.

#     # If there is only one actual file (a string)
#     if isinstance(testcase["actual_file"], str):
#         # The actual file is the prefix (test##) + the filename
#         #  (e.g. test01/my_file.txt)
#         actual_file = [
#             os.path.join(prefix, testcase["actual_file"]),
#         ]
#         # Add the actual file to the actual file list.
#         actual_files = list(actual_file)
#     else:
#         # If there are many actual files (a list of them), iterate over them and
#         # append them all to the actual file list.
#         actual_files = list()
#         for file in testcase["actual_file"]:
#             # The actual file is the prefix (test##) + the filename
#             #  (e.g. test01/my_file.txt)
#             actual_files.append(os.path.join(prefix, file))
#     # Return a list of all the actual files.
#     return actual_files


# def grade_a_single_file(file, number_of_numbers):
#     """
#     For a file and a number of numbers, see if they sum correctly.
#     """
#     try:
#         with open(file) as f:
#             # Read in all of the lines of the file (there is one number on each line)
#             numbers = f.readlines()
#         # Remove newlines/spaces from all lines of the file.
#         numbers = [x.strip() for x in numbers]
#         # The last line of the file is of the form "total = #" so we split with space as our delimiter.
#         numbers[-1] = numbers[-1].split()

#         # Make sure that the last line had 'total' in it.
#         if "total" not in numbers[-1]:
#             return_result(
#                 score=0, message="ERROR: total is not included", status="failure"
#             )

#         # The last line was of the form "total = #". We split earlier, and now we
#         # remove everything but the number.
#         numbers[-1] = numbers[-1][-1]
#         # Convert all of the numbers we read in from string to int.
#         numbers = [int(x) for x in numbers]

#         # Make sure that the 0 to n-1th numbers sum to the nth number.
#         if sum(numbers[:-1]) != numbers[-1]:
#             # If they do not, return zero credit with an error message.
#             return_result(
#                 score=0,
#                 message="ERROR: The numbers do not sum correctly",
#                 status="failure",
#             )
#         elif len(numbers[:-1]) != number_of_numbers:
#             # If they do sum correctly, make sure that we have the desired number of numbers.
#             return_result(
#                 score=0,
#                 message="ERROR: Incorrect number of numbers ({0} instead of {1})".format(
#                     len(numbers[:-1]), number_of_numbers
#                 ),
#                 status="failure",
#             )
#     except Exception:
#         return_result(
#             score=0, message="ERROR: Could not open output file.", status="failure"
#         )
#     # If no exception occurred and the numbers sum, return them so that we can do one last processing step.
#     return numbers


def parse_pytest_xml(xmlfile):
    tree = ET.parse(xmlfile)
    root = tree.getroot()

    tests = []
    for testsuites_element in root:
        for testsuite_element in testsuites_element:

            test = {"name": testsuite_element.attrib["name"], "result": True}
            for child in testsuite_element:
                if child.tag == "failure":
                    test["result"] = False
            tests.append(test)

    return tests


def get_pytest_results(tests):
    test_num = 0
    failures = 0
    results = f'Tests\n{"-" * 40}\n'
    for test in tests:
        test_num += 1
        pass_fail = "PASS" if test["result"] else "FAIL"
        failures += 0 if test["result"] else 1
        results += "{}. {}   {}\n".format(test_num, pass_fail, test["name"])
    return results


def grade_pytest_results(tests):
    test_num = 0
    failures = 0
    results = f'Tests\n{"-" * 40}\n'
    for test in tests:
        test_num += 1
        pass_fail = "PASS" if test["result"] else "FAIL"
        failures += 0 if test["result"] else 1
        results += "{}. {}   {}\n".format(test_num, pass_fail, test["name"])
    score = 0 if failures > 0 else 1
    status = "failure" if failures > 0 else "success"
    return_result(score, results, status)


def grade_pytest_results(tests):
    test_num = 0
    failures = 0
    vr = ValidationResults()

    # results = f'Tests\n{"-" * 40}\n'
    for test in tests:
        test_num += 1
        status = "success" if test["result"] else "failure"
        failures += 0 if test["result"] else 1
        # results += "{}. {}   {}\n".format(test_num, pass_fail, test["name"])
        vr.add_message(test["name"], status)
    score = 0 if failures > 0 else 1
    vr.set_score(score)
    vr.write_file_success()


def do_the_grading():
    """
    Process a number of runs of the student program to make sure that
      1) All runs resulted in a correct output.
      2) All runs were different (and therefore were likely random).
    """

    # try:
    #     # Parse command line arguments. In this assignment, this is how we learn
    #     # how many numbers the student was supposed to sum together.
    #     args = parse_args()
    # except Exception:
    #     # If we can't parse the command line arguments, we must have done something
    #     # wrong, so we'll return a failure message.
    #     return_error(message="ERROR: Incorrect arguments to custom validator")
    # number_of_numbers = args.numbers

    tests = parse_pytest_xml("pytest_results.xml")
    grade_pytest_results(tests)

    # # Grab all of the files we are supposed to check.
    # actual_files = get_actual_files()

    # # This variable will hold the numbers summed in the previous file. That way,
    # # we will be able to check that they are different in the next run.
    # prev_data = None

    # # For every student file
    # for file in actual_files:
    #     log_line("Processing " + file)

    #     # Make sure that the output in the file sums correctly
    #     data = grade_a_single_file(file, number_of_numbers)
    #     # If we are on the first file, save the this output so that we can check that the next
    #     # run is different (random).
    #     if prev_data is None:
    #         prev_data = data
    #     else:
    #         # If two runs of the student program yield the same random output, then the program
    #         # is probably not actually random, so return partial credit
    #         if data == prev_data:
    #             return_result(
    #                 score=0.6, message="ERROR: Program is not random.", status="failure"
    #             )
    # # If we make it all the way to the end, the student had the correct output and it was random,
    # # so return full credit.
    # return_result(
    #     score=1.0, message="Success: numbers summed correctly.", status="success"
    # )


if __name__ == "__main__":
    log_line(
        "In this new version of the grader, we can now write to a logfile! This is helpful for debugging!"
    )
    do_the_grading()
