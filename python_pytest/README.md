# CPTR 142: Objective #1 (1 point)

## Problem Overview

Your task in this homework assignment is to write a function returns the `Candy` object.

## Solution Specifications

Your solution to this problem must meet the following criteria.

1. You must define a function `candy_info` in the file `candy_function.py` that takes a three parameters.

    * a string for the name of the candy

    * an int for the number of grams of sugar

    * a float for the price of the candy

1. The function must return the Candy object.

1. The file `candy_function.py` should not contain a main program, it should only contain your function. To test your function, add code to the `candy_test.py` file. Note that code in `candy_test.py` and `candy.py` will not be graded.

1. Below is an example of a call to the `candy_info` function which you could implement in `candy_test.py` to test your function.

    Python Code:
    ```python
    import candy_function

    my_candy = candy_function.candy_info("SUGAR DADDY MILK CARAMEL POPS", 24, 10.45)
    print(my_candy.name)
    print(my_candy.sugar)
    print(my_candy.price)
    ```

    Output:
    ```html
    SUGAR DADDY MILK CARAMEL POPS
    24
    10.45
    ```

## Grade Specification

You will earn **one point** for completion of this homework problem once your solution passes all Submitty tests (indicated by all green bars).
