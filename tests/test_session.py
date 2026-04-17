import pytest
import pandas as pd

def sum_xy(x, y):
    sum= x + y
    return sum

def test_sum_xy():
    test_output = sum_xy(x=1, y=2)
    assert test_output == 3

# Write a function that finds the product product of two numbers (*)
# Write a test to check that it works

def product_xy(x, y):
    product = x * y
    return product

def test_product_xy():
    test_output = product_xy(x = 2, y=5)
    assert test_output == 10

def sum_prod(x, y):
    return sum_xy(x, y), product_xy(x, y)

def test_sum_prod():
    sum, prod = sum_prod(3, 5)
    assert sum == 8
    assert prod == 15

test_df = pd.DataFrame(
    [
        {"ChildId": "child1", "Age": 6},
        {"ChildId": "child3", "Age": 10},
        {"ChildId": "child2", "Age": 4},
        {"ChildId": "child4", "Age": 1},
    ]
)