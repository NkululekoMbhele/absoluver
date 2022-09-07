# Author: Nkululeko Mbhele
# Date: 05 September 2022
import re
from parenthesis import *
from simple import *
from evaluation import *

signs = ["+", "-", "*", "/"]

def get_expression_array(equation):
    signs = ["+", "-", "*", "/" ,"=", "(", ")"]
    position = 0
    array = []
    for i, char in enumerate(equation):
        if not (char.isdigit() or char.isalpha()):
            if len(equation[position:i]) != 0 or len(char) != 0:
                array.append(equation[position:i])
                array.append(char)
            position = i + 1
            if not any(x in equation[position:len(equation)] for x in signs):
                if len(equation[position:i]) != 0 or len(char) != 0:
                    array.append(equation[position:len(equation)])
    while("" in array):
        array.remove("")
    return array



equation = "2x + 9 = 8"
trimmed = equation.replace(" ", "")


tokens = get_expression_array(trimmed)
# print(parenthesis_simplification(tokens))

step, sample_tokens, new_tokens = simple_expression(tokens)



print(divide_expression(new_tokens))


# print(step1)
# print(divide_simplification(step1))
# evaluate_tokens(get_expression_array(trimmed))