from main import get_expression_array
from parenthesis import *
from simple import *
from evaluation import *

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

