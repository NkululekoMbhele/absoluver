# Author: Nkululeko Mbhele
# Date: 10 September 2022
import re, string
import nltk
from nltk.tokenize import word_tokenize
signs = ["+", "-", "*", "/"]

def get_expression_array(equation):
    trimmed = equation.replace(" ", "")
    spaced_equation = re.sub("[\(\+\-\)=]",  lambda operator: " " + operator[0] + " ", trimmed)
    tokenized_equation =  word_tokenize(spaced_equation)
    return tokenized_equation

def fix_signs(tokens):
    operator_sign = ["+", "-"]
    signs = ["("]
    for index, token in enumerate(tokens):
        if token == "-" and index == 0 and tokens[index + 1] != "(":
            tokens[index + 1] = token + tokens[index + 1]
            tokens.pop(index)
        if token == "+" and str(tokens[index + 1])[0] == "-":
            tokens[index] = "-"
            tokens[index+1] = str(tokens[index + 1])[1:]
        if token == "-" and str(tokens[index + 1])[0] == "-":
            tokens[index] = "+"
            tokens[index+1] = str(tokens[index + 1])[1:]
    return tokens

def simplification(tokens):
    signs = ["+", "-", "*", "/" ,"=", "(", ")" ]
    new_tokens = []
    factor = ""
    factor2 = ""
    operator = ""
    for index, value in enumerate(tokens):
        if value not in signs and index < tokens.index('=') and value.isdigit():
            factor = value
            operator = tokens[index-1]
        elif value not in signs and index > tokens.index('=') and value.isdigit():
            factor2 = value
        elif value not in signs:
            new_tokens.append(value)
    
    new_answer = 0
    if operator == '+':
        new_answer = int(factor2) - int(factor)
    if operator == '-':
        new_answer = int(factor2) + int(factor)
    new_tokens.append("=")
    new_tokens.append(new_answer)
    return new_tokens

def divide_simplification(tokens):
    factor = ""
    new_tokens = []
    factor2 = ""
    for index, value in enumerate(tokens):
        if not str(value).isdigit() and value not in signs and index < tokens.index('='):
            temp = ""
            for i in value:
                print(i)
                if not i.isdigit():
                    new_tokens.append(i)
                if i.isalpha():
                    temp = value
                    temp = ''.join(j for j in temp if j.isdigit())
                    print("temp: " + temp)
            factor = temp
        if str(value).isdigit() and value not in signs:
            factor2 = value

    print(f"{factor2} = {factor}")
    new_tokens.append("=")
    answer = factor2 / int(factor)
    new_tokens.append(round(answer, 2))
    return new_tokens

def parenthesis_simplification(tokens):
    # Check type of parenthesis structure
    # simple = (2x + 1) | distribution = 2(2x + 1) | 2+(2x + 1) (2 + 5) 2(2x + 3x)
    print(tokens)
    # simple 
    new_tokens = []
    for index, value in enumerate(tokens):
        if value == "(":
            tokens.remove(value)
        if value == ")":
            tokens.remove(value)
    return tokens

#Steps
def simple_expression(tokens):
    signs = ["+", "-", "*", "/" ,"=" ]
    new_tokens = []
    sample_tokens = []
    step = ""
    value_change = ""
    factor = ""
    factor2 = ""
    operator = ""
    for index, value in enumerate(tokens):
        if value not in signs and index < tokens.index('=') and value.isdigit():
            factor = value
            operator = tokens[index-1]
        elif value not in signs and index > tokens.index('=') and value.isdigit():
            factor2 = value
        elif value not in signs:
            new_tokens.append(value)
    
    new_answer = 0
    if operator == '+':
        new_answer = int(factor2) - int(factor)
        value_change = "-" + factor
        step = f"Substract {factor} from both sides"
    if operator == '-':
        new_answer = int(factor2) + int(factor)
        value_change = "+" + factor
        step = f"Add {factor} on both sides"
    new_tokens.append("=")
    new_tokens.append(new_answer)

    position = tokens.index("=")
    change = get_expression_array(value_change)
    sample_tokens = tokens[0:position] + change + tokens[position:] + change
    print(step)
    print(sample_tokens)
    return step, sample_tokens, new_tokens

def divide_expression(tokens):
    signs = ["+", "-", "*", "/" ,"=" ]
    new_tokens = []
    sample_tokens = []
    step = ""
    value_change = ""
    factor = ""
    factor2 = ""
    for index, value in enumerate(tokens):
        if not str(value).isdigit() and value not in signs and index < tokens.index('='):
            temp = ""
            for i in value:
                if not i.isdigit():
                    new_tokens.append(i)
                if i.isalpha():
                    temp = value
                    temp = ''.join(j for j in temp if j.isdigit())
            factor = temp
        if value not in signs and index > tokens.index('='):
            factor2 = value

    print(f"{factor2} = {factor}")
    step = f"Divide both sides by {factor}"
    new_tokens.append("=")
    answer = int(factor2) / int(factor)
    new_tokens.append(round(answer, 2))

    position = tokens.index("=")
    change = get_expression_array("/" + factor)
    sample_tokens = tokens[0:position] + change + tokens[position:] + change

    return step, sample_tokens, new_tokens

def check_if_simplified_digits(tokens):
    simplified = False
    signs = ["+", "-", "*", "/"]
    details = ""
    for index, token in enumerate(tokens):
        if token in signs:
            if tokens[index-1].isdigit() and tokens[index+1].isdigit():
                simplified = False
            else:
                simplified = True
    return simplified

def upper_level_simplication(tokens):
    new_tokens = tokens
    signs_base = ["+", "-", "*", "/"]
    tokens_update = []
    used_tokens = []
    factor = 0
    factor2 = 0
    signs = ["+", "-", "*", "/"]
    # while not check_if_simplified_digits(tokens):
    for index, token in enumerate(tokens):
        if token in signs_base:
            if tokens[index-1].isdigit() and tokens[index+1].isdigit():
                if (token == "+"):
                    answer = int(tokens[index-1]) + int(tokens[index+1])
                    tokens_update.append(answer)
                    used_tokens.append(index-1)
                    used_tokens.append(index+1)
                    tokens[index] = answer
                elif (token == "-"):
                    answer = int(tokens[index-1]) - int(tokens[index+1])
                    tokens_update.append(answer)
                    used_tokens.append(index-1)
                    used_tokens.append(index+1)
                    tokens[index] = answer
        if token not in used_tokens:
            tokens_update.append(token)
    for i in used_tokens:
        tokens.pop(i);
        for j in range(len(used_tokens)):
            used_tokens[j] = used_tokens[j] - 1
    print(tokens)
    return used_tokens

# Expression Classifier
def expression_classifier(tokens):
    # Types
    # Base -> ax = c -> 0
    # Base2 -> ax + b = c -> 1
    # Sides -> ax + b = cx + d -> 2
    # Parenthesis -> a(bx + c) = d -> 3
    # Multi -> ax + b + c = c + d + e -> 4
    types = ["base", "base2", "sides", "parenthesis", "multi"]
    signs = ["+", "-", "*", "/" ,"=", "(", ")" ]
    case = 0
    # Base Test 
    variables = [0, 0]
    constants = [0, 0]
    parenthesis_pair = [0, 0]
    for index, value in enumerate(tokens):
        # left side
        if (index < tokens.index("=")) and value not in signs:
            #check if its a signs
            print("Left")
            #check if constant
            if str(value).isdigit():
                constants[0] += 1
            if str(value)[-1].isalpha():
                variables[0] += 1
        # right side
        if (index > tokens.index("=")) and value not in signs:
            print("Right")
            if str(value).isdigit():
                constants[1] += 1
            if value[-1].isalpha():
                variables[1] += 1
        pair = False
        pair_count = 0
        if (index < tokens.index("=")):
            if (value == "("):
                pair_count += 1
            if (value == ")"):
                pair_count += 1
                if (pair_count == 1):
                    parenthesis_pair[0] += 1
                    pair_count = 0
        if (index > tokens.index("=")):
            if (value == "("):
                pair_count += 1
            if (value == ")"):
                pair_count += 1
                if (pair_count == 1):
                    parenthesis_pair[1] += 1
                    pair_count = 0
    # base case
    if (variables[0] == 1 and variables[1] == 0 and constants[0] == 0 and constants[1] == 1 and parenthesis_pair[0] == 0 and parenthesis_pair[1] == 0):
        print("base case")
        return 0
    # base 2
    elif (variables[0] == 1 and variables[1] == 0 and constants[0] == 1 and constants[1] == 1 and parenthesis_pair[0] == 0 and parenthesis_pair[1] == 0):
        print("base case 2")
        return 1
    # Sides
    elif (variables[0] == 1 and variables[1] == 1 and constants[0] == 1 and constants[1] == 1 and parenthesis_pair[0] == 0 and parenthesis_pair[1] == 0):
        print("sides case")
        return 2
    # Parenthesis
    elif (variables[0] == 1 and variables[1] == 0 and constants[0] == 1 and constants[1] == 1 and parenthesis_pair[0] == 1 and parenthesis_pair[1] == 0):
        print("parenthesis case")
        return 3
    # Multi          
    else:
        print("multi case")
        return 4
    

def parenthesis(tokens):
    coefficient = 1
    expression = 0
    start_pos = 0
    end_pos = 0
    for i, token in enumerate(tokens):
        if (token == "("):
            if i > 0:
                coefficient = tokens[i-1]
            if i == 0:
                start_pos = 0
            else:
                start_pos = i
        if (token == ")"):
            end_pos = i
            break
    return tokens[start_pos:end_pos+1], coefficient, (start_pos, end_pos+1)

def evaluate_parenthesis(tokens):
    signs = ["+", "-", "*", "/"]
    eval_tokens, coefficient, position = parenthesis(tokens)
    if coefficient in signs:
        coefficient = '1'
    eval_tokens.remove("(")
    eval_tokens.remove(")")
    is_variable = False
    variable = ""
    new_tokens = []
    for i, value in enumerate(eval_tokens):
        if value not in signs and not value.isdigit():
            for char in value:
                if char.isalpha():
                    new_value = value.replace(char, "")
                    new_variable_coeffient = eval(f"{coefficient} * {new_value}")
                    new_tokens.append(f"{new_variable_coeffient}{char}")

        elif str(value).isdigit():
            new_tokens.append(eval(f"{coefficient} * {value}"))
        else:
            new_tokens.append(value)
    # Replace old tokens with new ones
    # for value in tokens:
    if position[0] == 0:
        tokens[position[0]:position[1]] = new_tokens
    else:
        tokens[position[0]-1:position[1]] = new_tokens

    print(new_tokens)
    print("Here")
    print(tokens)
    evaluated_tokens = fix_signs(tokens)
    print(evaluated_tokens)
    string = ''.join(str(item) for item in evaluated_tokens)
    parenthesis_check = re.findall(r'\((.*?)\)', string)
    if (len(parenthesis_check) != 0):
        evaluate_parenthesis(evaluated_tokens)
    else:
        return evaluated_tokens

    

def numerical_eval(tokens):
    signs = ["+", "-", "*", "/"]
    start_pos = 0
    string = ""
    for index, token in enumerate(tokens):
         # left side
        if (index < tokens.index("=")) and value not in signs:
            #check if its a signs
            print("Left")
            #check if constant
            if str(value).isdigit():
                constants[0] += 1
        # right side
    print(string)

if __name__ == "__main__":
    equation = "-6(5x + 2) = 6 + 1+ 5"
    tokens = get_expression_array(equation)
    fixed_tokens = fix_signs(tokens)
    # print(tokens)
    print(fixed_tokens)
    string = ''.join(fixed_tokens)
    parenthesis_check = re.findall(r'\((.*?)\)', string)
    if (len(parenthesis_check) != 0):
        print(parenthesis_check[0])
    print(evaluate_parenthesis(tokens))
    # numerical_eval(tokens)

    
