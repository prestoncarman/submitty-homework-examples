import grader


def test_print_result_fail(capsys):
    grader.print_result([{"name": "Test 1", "result": False}])

    captured = capsys.readouterr()
    assert (
        captured.out
        == "Tests\n----------------------------------------\n1. FAIL   Test 1\n"
    ), "Single failed test does not prints expected output"


def test_print_result_pass(capsys):
    grader.print_result([{"name": "Test 1", "result": True}])

    captured = capsys.readouterr()
    assert (
        captured.out
        == "Tests\n----------------------------------------\n1. PASS   Test 1\n"
    ), "Single successful test does not prints expected output"
