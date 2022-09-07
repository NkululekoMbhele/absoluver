import main
from parenthesis import *
from simple import *
from evaluation import *



def evaluate_tokens(tokens):
    expressions_types = [""]
    signs = ["+", "-", "*", "/" ,"=", "(", ")" ]
    variables = 0
    variables_left = 0
    variables_right = 0
    digits_left = 0
    digits_right = 0
    var_index = []
    left_expressions_count = 0
    right_expressions_count = 0
    for index, token in enumerate(tokens):
        if token not in signs and index < tokens.index('='):
            left_expressions_count += 1
        if token not in signs and index > tokens.index('='):
            right_expressions_count += 1
        if token.isdigit() and index < tokens.index('='):
            digits_left += 1
        if token.isdigit() and index > tokens.index('='):
            digits_right += 1
        if not token.isdigit() and token not in signs:
            variables += 1
            if token not in signs and index < tokens.index('='):
                variables_left += 1
            if token not in signs and index > tokens.index('='):
                variables_right += 1

            var_index.append(index)
            if index < tokens.index('='):
                var_index.append(0)
            else:
                var_index.append(1)
    print("Variables Count Left: " + str(variables_left))
    print("Variables Count Right: " + str(variables_right))
    print("Digits Count Left: " + str(digits_right))
    print("Digits Count Right: " + str(digits_right))
    print("LHS: " + str(left_expressions_count))
    print("RHS: " + str(right_expressions_count))

            