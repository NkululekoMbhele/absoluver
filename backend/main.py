import json
from flask_cors import CORS, cross_origin
from flask import Flask, request
import re
import nltk
from nltk.tokenize import word_tokenize
import sympy
from sympy.core.assumptions import assumptions
from sympy import Symbol
import sympy as sym


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/', methods=['GET', 'POST'])
def index():
    solution_steps = []
    data = request.data
    equation = request.args.get('equation')
    print(equation)
    instance = Absoluver(equation)
    instance.run()
    solution_steps = instance.solution_steps
    return json.dumps({'steps': solution_steps, 'variable': instance.variable, 'equation': equation})

@app.route('/test', methods=['GET', 'POST'])
def test():
    instance = Absoluver("2x + 3 = 4")
    print(instance.equation_tokenization())
    return json.dumps({steps : instance.equation_tokenization()})


class Absoluver():
    def __init__(self, equation):
        #operations instances
        self.all_signs = ["+", "-", "*", "/", "(", ")"]
        self.all_operators = ["+", "-", "*", "/", "="]
        self.plus_sign = "+"
        self.minus_sign = "-"
        self.times_sign = "*"
        self.divide_sign = "/"
        self.open_bracket = "("
        self.close_bracket = ")"
        self.equal_sign = "="

        #Equation initialisation
        self.equation = equation

        # Expression state
        self.variables = [0, 0]
        self.constants = [0, 0]
        self.parenthesis_pair = [0, 0]

        # Solution Steps
        # Format: 
        # {
        #   "equation": "2x + 1 = 2",
        #   "step_count": "1",
        #   "step": "Substract 1 from both sides",
        #   "step_equation": "2x + 1 - 1 = 2 - 1",
        #   "new_equation": "2x = 1",
        #   ""
        # } ...
        self.solution_steps = []
        self.step_count = 1

        # x, y, z etc
        self.variable = ""

        # States: []
        # solution_case = x = b 
        # base_case -> ax = c -> 0 if variables = 1 and 0 and constants 1
        # simple_base -> ax + b = c -> 1 if variables = 1
        # two_sided_variables -> ax + b = cx + d -> 2 if variables both > 1
        # brackets_off_simplification -> a(bx + c) = d -> 3 --> if parenthesis_count > 1
        # numerical_simplification -> ax + b + c = c + d + e -> ax + b = c --> constants > 1
        # algebraic_simplification -> ax + bx + c = e -> ax + c = e  --> variables > 1
        # terms_arrangement -> ax + b = cx + d ---> ax - cx = d - b
        self.equation_state = ""

        # Format: '{ "varible" : "answer",}'
        self.final_solution = ""

        # Continously updated
        self.tokens = []

        # Error handling
        self.error_message = ""

    # Fix expression 
    def expression_tokenization(self, expression):
        trimmed = expression.replace(" ", "")
        spaced_equation = ""
        for index, value in enumerate(expression):
            if value in self.all_operators:
                spaced_equation += value
                spaced_equation += " "
            else:
                spaced_equation += value
        tokenized_equation =  word_tokenize(spaced_equation)
        return tokenized_equation

    # Create tokens(string array) from the equation e.g "2x + 3 = 1" --> ["2x", "+", "3", "=", "1"]
    def equation_tokenization(self):
        trimmed = self.equation.replace(" ", "")
        spaced_equation = re.sub("[\(\+\-\)=]",  lambda operator: " " + operator[0] + " ", trimmed)
        tokenized_equation =  word_tokenize(spaced_equation)
        if tokenized_equation[0] == self.minus_sign and tokenized_equation[1] not in self.all_operators:
            tokenized_equation[1] = self.minus_sign + tokenized_equation[1]
            tokenized_equation.pop(0)
        if tokenized_equation[tokenized_equation.index(self.equal_sign)+1] == self.minus_sign and tokenized_equation[tokenized_equation.index(self.equal_sign)+2] not in self.all_operators:
            tokenized_equation[tokenized_equation.index(self.equal_sign)+2] = self.minus_sign + tokenized_equation[tokenized_equation.index(self.equal_sign)+2]
            tokenized_equation.pop(tokenized_equation.index(self.equal_sign)+1)
        self.tokens = tokenized_equation
        return tokenized_equation

    # Fix signs error and misplacements e.g [12, "-", "-8"] --> ["12", "+", "8"] or [12, "+", "-8"] --> ["12", "-", "8"]
    def fix_signs(self):
        # fix double signs
        print("Fix")
        for index, token in enumerate(self.tokens):
            if str(token)[0] == self.minus_sign and index != 0 and token not in self.all_signs:
                if self.tokens[index - 1] == self.equal_sign:
                    continue
                elif self.tokens[index - 1] == self.plus_sign:
                    self.tokens[index] = str(token)[1:]
                    self.tokens[index - 1] = self.minus_sign
                elif self.tokens[index - 1] == self.minus_sign:
                    self.tokens[index] = str(token)[1:]
                    self.tokens[index - 1] = self.plus_sign
                elif self.tokens[index - 1] not in self.all_signs:
                    self.tokens[index] = str(token)[1:]
                    self.tokens.insert(index, str(token)[0])
        
        # fix no signs ['2y', '-7', '=', '6'] ---> ['2y', '-', '7', '=', '6']
        # check if the equation need sign fix
        no_sign_issue = False
        for i, token in enumerate(self.tokens): 
            if i < len(self.tokens)-1 and token not in self.all_operators and self.tokens[i+1] not in self.all_operators:
                no_sign_issue = True


        # join signs
        for i, token in enumerate(self.tokens): 
            if token == self.plus_sign and self.tokens[i-1] == self.equal_sign:
                print(token)
            if token == self.minus_sign and self.tokens[i-1] == self.equal_sign and self.tokens[i+1] not in self.all_signs:
                print(token)
                self.tokens[i+1] = self.minus_sign + str(self.tokens[i+1])
                self.tokens.pop(i)
        if no_sign_issue:
            for index, token in enumerate(self.tokens):
                if index < len(self.tokens)-1 and token not in self.all_operators and self.tokens[index+1] not in self.all_operators:
                    print(token)

                # if token.isdigit() or token not in self.all_operators and index < len(self.tokens) - 2:
                #     if self.tokens[index+1] not in self.all_operators and self.tokens[index+1][0] == self.minus_sign:
                #         print("Hello")
                #         self.tokens.insert(index, self.minus_sign)
                #     else:
                #         self.tokens.insert(index, self.plus_sign)
        # return self.tokens
    
    # Simple Base  Case: ax + b = c  ---> ax = d
    def simple_base_case(self):
        new_tokens = []
        sample_tokens = []
        step = ""
        value_change = ""
        factor = ""
        factor2 = ""
        operator = ""
        for index, value in enumerate(self.tokens):
            if value not in self.all_operators and index < self.tokens.index(self.equal_sign) and value.isdigit():
                factor = value
                operator = self.tokens[index-1]
            elif value not in self.all_operators and index > self.tokens.index(self.equal_sign) and value.isdigit():
                factor2 = value
            elif value not in self.all_operators:
                new_tokens.append(value)
        
        new_answer = 0
        if operator == self.plus_sign:
            new_answer = int(factor2) - int(factor)
            value_change = "-" + factor
            step = f"Substract {factor} from both sides"
        if operator == self.minus_sign:
            new_answer = int(factor2) + int(factor)
            value_change = self.plus_sign + factor
            step = f"Add {factor} on both sides"
        new_tokens.append(self.equal_sign)
        new_tokens.append(new_answer)

        position = self.tokens.index(self.equal_sign)
        # Make the expression change into tokens +2 --> ["+", "2"]
        change = self.expression_tokenization(value_change)
        sample_tokens = self.tokens[0:position] + change + self.tokens[position:] + change

        # Create a dictionary format for the solution in order to be parsed
        solution = {
            "equation": ' '.join(str(term) for term in self.tokens),
            "step_count": str(self.step_count),
            "step": step,
            "step_equation":  ' '.join(str(term) for term in sample_tokens),
            "new_equation": ' '.join(str(term) for term in new_tokens)
        }
        self.solution_steps.append(solution)
        self.tokens = new_tokens
        self.step_count += 1
        return step, sample_tokens, new_tokens

    def solution_case(self):
        if self.variable == self.tokens[0] and self.constants == [0, 1]:
            self.final_solution = {self.variable : str(self.tokens[-1])}
        step = "Solution"
        solution = {
            "equation": ' '.join(str(term) for term in self.tokens),
            "step_count": str(self.step_count),
            "step": step,
            "step_equation":  ' '.join(str(term) for term in self.tokens),
            "new_equation": ' '.join(str(term) for term in self.tokens)
        }
        self.solution_steps.append(solution)
    # Base Case: ax = b --> x = b
    def base_case(self):
        new_tokens = []
        sample_tokens = []
        step = ""
        value_change = ""
        factor = ""
        factor2 = ""
        for index, value in enumerate(self.tokens):
            if not str(value).isdigit() and value not in self.all_operators and index < self.tokens.index(self.equal_sign):
                temp = ""
                if value[-1] == self.variable:
                    temp = value[:-1]
                    new_tokens.append(self.variable)
                factor = temp
            if value not in self.all_operators and index > self.tokens.index('='):
                factor2 = value

        step = f"Divide both sides by {factor}"
        new_tokens.append(self.equal_sign)
        answer = eval(f"{factor2} / {factor}")
        new_tokens.append(round(answer, 2))

        # Get the position of the equal sign
        position = self.tokens.index(self.equal_sign)
        change = self.expression_tokenization(self.divide_sign + factor)
        # Make a step equation
        sample_tokens = self.tokens[0:position] + change + self.tokens[position:] + change
        solution = {
            "equation": ' '.join(str(term) for term in self.tokens),
            "step_count": str(self.step_count),
            "step": step,
            "step_equation":  ' '.join(str(term) for term in sample_tokens),
            "new_equation": ' '.join(str(term) for term in new_tokens)
        }
        self.solution_steps.append(solution)
        self.tokens = new_tokens
        self.step_count += 1
        return step, sample_tokens, new_tokens

    # Arrange terms: ax + c = bx + d  --->  ax - bx = d - c
    def terms_arrangement(self):
        new_terms = self.tokens
        right_transpose = []
        right_transpose_indeces = []
        left_transpose = []
        left_transpose_indeces = []
        popped = 0

        # Traverse through each token
        for index, term in enumerate(self.tokens):
            # Left hand side check
            if term[-1] != self.variable and term not in self.all_operators and index < self.tokens.index(self.equal_sign):
                if self.tokens[index - 1] in self.all_operators:
                    left_transpose.append(self.tokens[index-1])
                    left_transpose_indeces.append(index-1)
                left_transpose.append(self.tokens[index])
                left_transpose_indeces.append(index)
            #right hand side check
            if term[-1] == self.variable and term not in self.all_operators and index > self.tokens.index(self.equal_sign):
                if self.tokens[index - 1] in self.all_operators and self.tokens[index -1] != self.equal_sign:
                    right_transpose.append(self.tokens[index-1])
                    right_transpose_indeces.append(index - 1)
                right_transpose.append(self.tokens[index])
                right_transpose_indeces.append(index)
        # insert changes
        print(new_terms)
        if len(right_transpose_indeces) > 1:
            new_terms.pop(right_transpose_indeces[1])
            new_terms.pop(right_transpose_indeces[0])
        else:
            new_terms.pop(right_transpose_indeces[0])
        if len(left_transpose_indeces) > 1:
            new_terms.pop(left_transpose_indeces[1])
            new_terms.pop(left_transpose_indeces[0])
        else:
            new_terms.pop(left_transpose_indeces[0])


        # change signs left change
        if left_transpose[0] == self.minus_sign:
            left_transpose[0] = self.plus_sign
        elif left_transpose[0] == self.plus_sign:
            left_transpose[0] = self.minus_sign
        
        # change signs right change
        if len(right_transpose) == 1 and right_transpose[0][0] == self.minus_sign:
            right_transpose[0] = right_transpose[0][1:]
            right_transpose.insert(0, self.plus_sign)

        print(left_transpose)
        print(right_transpose)
        new_terms = new_terms + left_transpose
        new_terms = new_terms[:new_terms.index(self.equal_sign)] + right_transpose + new_terms[new_terms.index(self.equal_sign):]
        print(new_terms)
        self.tokens = new_terms
        self.fix_signs()

    
    def group_tokens_helper(self, tokens):
        insert_index = 0
        top_index = len(tokens)-1
        for i in range(top_index, -1, -1):
            if not re.search("[a-zA-Z]", tokens[i]) and tokens[i] not in self.all_operators:
                if insert_index == 0:
                    tokens = tokens[:top_index+1] + [tokens[i-1], tokens[i]] + tokens[top_index+1:]
                    insert_index = top_index-2
                    tokens.pop(i-1)
                    tokens.pop(i-1)
                else:
                    tokens = tokens[:insert_index+1] + [tokens[i-1], tokens[i]] + tokens[insert_index+1:]
                    insert_index -= 2
                    tokens.pop(i-1)
                    tokens.pop(i-1)
        return tokens

    def expression_simplifier_helper(self, expression):
        simplified = []
        # simplify constants
        for index, term in enumerate(expression):
            if term == self.minus_sign or term == self.plus_sign:
                if expression[index-1][-1] != self.variable and expression[index+1][-1] != self.variable:
                    if expression[index-2] == self.minus_sign:
                        new_answer = eval(f"{self.minus_sign}{expression[index-1]} {term} {expression[index+1]}")
                    else:
                        new_answer = eval(f"{expression[index-1]} {term} {expression[index+1]}")
                    if (str(new_answer)[0] == self.minus_sign):
                        expression[index-2:index+2] = [self.minus_sign, str(new_answer)[1:]]
                    else:
                        expression[index-2:index+2] = [self.plus_sign, str(new_answer)]

        #simplify algebraic expressions
        for index, term in enumerate(expression):
            if term == self.minus_sign or term == self.plus_sign:
                if  re.search("[a-zA-Z]", expression[index-1]) and re.search("[a-zA-Z]", expression[index+1]):
                    new_answer = eval(f"{expression[index-1].rstrip(expression[index-1][-1])} {term} {expression[index+1].rstrip(expression[index+1][-1])}")
                    if (str(new_answer)[0] == self.minus_sign):
                        new_answer = f"{new_answer}{self.variable}"
                        expression[index-1:index+2] = [str(new_answer)]
                    else:
                        new_answer = f"{new_answer}{self.variable}"
                        expression[index-1:index+2] = [str(new_answer)]
        return expression

    # Remove brackets: a(bx + c) = d  ---> abx + ac = d
    def brackets_off(self):
        elements = re.findall("\((.*?)\)", "".join(self.tokens))
        coefficients = re.search("(", "".join(self.tokens))

    def parenthesis(self):
        start_pos = 0
        end_pos = 0
        eval_tokens = []
        coefficient = ""
        replace_position = []
        for i, term in enumerate(self.tokens):
            if term == self.open_bracket:
                start_pos = i
                if self.tokens[i-1] in self.all_operators:
                    coefficient = str("".join(self.tokens[i-1:i])) + "1"
                else:
                    coefficient = self.tokens[i-2:i]
            elif term == self.close_bracket:
                end_pos = i
        eval_tokens = self.tokens[start_pos+1:end_pos]
        replace_position = [start_pos, end_pos+1]
        eval_tokens = self.group_tokens_helper(eval_tokens)
        self.expression_simplifier_helper(eval_tokens)
        return eval_tokens, coefficient, replace_position
    # Remove brackets: a(bx + c) = d  ---> abx + ac = d
    def brackets_off_simplification(self):
        signs = ["+", "-", "*", "/"]
        eval_tokens, coefficient, position = self.parenthesis()
        is_variable = False
        variable = ""
        new_tokens = []
        for i, value in enumerate(eval_tokens):
            if value not in signs and not value.isdigit():
                for char in value:
                    if char.isalpha():
                        is_variable = True
                        variable = char
                        new_value = value.replace(variable, "")
                        new_variable_coeffient = eval(f"{coefficient} * {new_value}")
                        new_tokens.append(f"{new_variable_coeffient}{variable}")

            elif str(value).isdigit():
                new_tokens.append(eval(f"{coefficient} * {value}"))
            else:
                new_tokens.append(value)
        # Replace old tokens with new ones
        # for value in tokens:
        if position[0] == 0:
            self.tokens[position[0]:position[1]] = new_tokens
        else:
            self.tokens[position[0]-1:position[1]] = new_tokens
        print(self.tokens)
        # solution = '{"equation": '+ self.tokens +', "step_count":'+ self.step_count +', "step": '+ step +', "step_equation": '+ sample_tokens+', "new_equation":'+ new_tokens+'}'
        # self.solution_steps.append(solution)
    
    # Numerical simplify: ax + b = d + c - e  --> ax + b = f
    def numerical_simplification(self):
        copy_tokens = self.tokens
        add_tokens_left = []
        add_tokens_right = []
        left_indeces = [0, 0]
        right_indeces = [0, 0]
        for index, term in enumerate(copy_tokens):
            if not bool(re.search("[a-z]", term)) and index < copy_tokens.index(self.equal_sign):
                if term in self.all_operators and bool(re.search("[a-z]", copy_tokens[index - 1])) and bool(re.search("[a-z]", copy_tokens[index + 1])):
                    continue
                else:
                    if left_indeces[0] == 0:
                        left_indeces[0] = index
                    else:
                        left_indeces[1] = index
                    add_tokens_left.append(term)
            if not bool(re.search("[a-z]", term)) and index > copy_tokens.index(self.equal_sign):
                if term in self.all_operators and bool(re.search("[a-z]", copy_tokens[index - 1])) and bool(re.search("[a-z]", copy_tokens[index + 1])):
                    continue
                else:
                    if right_indeces[0] == 0:
                        right_indeces[0] = index
                    else:
                        right_indeces[1] = index
                    add_tokens_right.append(term)
        left_answer = eval(f"{' '.join(add_tokens_left)}")
        right_answer = eval(f"{' '.join(add_tokens_right)}")
        copy_tokens = copy_tokens[:right_indeces[0]] + [str(right_answer)] + copy_tokens[right_indeces[1]+1:]
        copy_tokens = copy_tokens[:left_indeces[0]] + [str(left_answer)] + copy_tokens[left_indeces[1]+1:]
        self.tokens = copy_tokens
        self.fix_signs()
     
        
    def group_tokens(self):
        insert_index = 0
        top_index = self.tokens.index(self.equal_sign)-1
        for i in range(len(self.tokens[:self.tokens.index(self.equal_sign)-1]), -1, -1):
            if not re.search("[a-zA-Z]", self.tokens[i]) and self.tokens[i] not in self.all_operators:
                if insert_index == 0:
                    self.tokens = self.tokens[:top_index+1] + [self.tokens[i-1], self.tokens[i]] + self.tokens[top_index+1:]
                    insert_index = top_index-2
                    self.tokens.pop(i-1)
                    self.tokens.pop(i-1)
                else:
                    self.tokens = self.tokens[:insert_index+1] + [self.tokens[i-1], self.tokens[i]] + self.tokens[insert_index+1:]
                    insert_index -= 2
                    self.tokens.pop(i-1)
                    self.tokens.pop(i-1)
                
        top_index = self.tokens.index(self.equal_sign) + 1
        insert_index = 0
        for i in range(len(self.tokens)-1, self.tokens.index(self.equal_sign)-1, -1):
            if not re.search("[a-zA-Z]", self.tokens[i]) and self.tokens[i] not in self.all_operators:
                if insert_index == 0:
                    self.tokens = self.tokens[:top_index] + self.tokens[top_index:] + [self.tokens[i-1], self.tokens[i]]
                    insert_index = len(self.tokens)
                    self.tokens.pop(i-1)
                    self.tokens.pop(i-1)
                else:
                    self.tokens = self.tokens[:insert_index+1] + [self.tokens[i-1], self.tokens[i]] +  self.tokens[insert_index+1:]
                    insert_index -= 2
                    self.tokens.pop(i-1)
                    self.tokens.pop(i-1)     
        print(self.tokens)
            
    # Algebraic simplification: ax + bx  + c = e  ---> dx + c = e
    def algebraic_simplification(self):
        # Algebraic simplification on both sides
        copy_tokens = self.tokens
        add_tokens_left = []
        add_tokens_right = []
        left_indeces = [0, 0]
        right_indeces = [0, 0]
        for index, term in enumerate(copy_tokens):
            if not bool(re.search("[a-z]", term)) and index < copy_tokens.index(self.equal_sign):
                if term in self.all_operators and bool(re.search("[a-z]", copy_tokens[index - 1])) and bool(re.search("[a-z]", copy_tokens[index + 1])):
                    continue
                else:
                    if left_indeces[0] == 0:
                        left_indeces[0] = index
                    else:
                        left_indeces[1] = index
                    add_tokens_left.append(term)
            if not bool(re.search("[a-z]", term)) and index > copy_tokens.index(self.equal_sign):
                if term in self.all_operators and bool(re.search("[a-z]", copy_tokens[index - 1])) and bool(re.search("[a-z]", copy_tokens[index + 1])):
                    continue
                else:
                    if right_indeces[0] == 0:
                        right_indeces[0] = index
                    else:
                        right_indeces[1] = index
                    add_tokens_right.append(term)
        left_answer = eval(f"{' '.join(add_tokens_left)}")
        right_answer = eval(f"{' '.join(add_tokens_right)}")
        copy_tokens = copy_tokens[:right_indeces[0]] + [str(right_answer)] + copy_tokens[right_indeces[1]+1:]
        copy_tokens = copy_tokens[:left_indeces[0]] + [str(left_answer)] + copy_tokens[left_indeces[1]+1:]
        self.tokens = copy_tokens
        self.fix_signs()
        for index, term in enumerate(self.tokens):
            if term == self.minus_sign or term == self.plus_sign:
                if  re.search("[a-zA-Z]", self.tokens[index-1]) and re.search("[a-zA-Z]", self.tokens[index+1]):
                    new_answer = eval(f"{self.tokens[index-1].rstrip(self.tokens[index-1][-1])} {term} {self.tokens[index+1].rstrip(self.tokens[index+1][-1])}")
                    if (str(new_answer)[0] == self.minus_sign):
                        new_answer = f"{new_answer}{self.variable}"
                        self.tokens[index-1:index+2] = [str(new_answer)]
                    else:
                        new_answer = f"{new_answer}{self.variable}"
                        self.tokens[index-1:index+2] = [self.plus_sign, str(new_answer)]
        for index, term in enumerate(self.tokens):
            if term == self.minus_sign or term == self.plus_sign:
                if  re.search("[a-zA-Z]", self.tokens[index-1]) and re.search("[a-zA-Z]", self.tokens[index+1]):
                    new_answer = eval(f"{self.tokens[index-1].rstrip(self.tokens[index-1][-1])} {term} {self.tokens[index+1].rstrip(self.tokens[index+1][-1])}")
                    if (str(new_answer)[0] == self.minus_sign):
                        new_answer = f"{new_answer}{self.variable}"
                        self.tokens[index-1:index+2] = [str(new_answer)]
                    else:
                        new_answer = f"{new_answer}{self.variable}"
                        self.tokens[index-1:index+2] = [self.plus_sign, str(new_answer)]
    # Extract the coefficient
    def parenthesis_identifier(self):
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

    def expression_classifier_count(self):
        # Reset The Count for the new expression classifier count
        self.variables = [0, 0]
        self.constants = [0, 0]
        self.parenthesis_pair = [0, 0]

        # Types
        # Base -> ax = c -> 0
        # Base2 -> ax + b = c -> 1
        # Sides -> ax + b = cx + d -> 2
        # Parenthesis -> a(bx + c) = d -> 3
        # Multi -> ax + b + c = c + d + e -> 4
        # Base Test 
        for index, value in enumerate(self.tokens):
            # left side
            if (index < self.tokens.index(self.equal_sign)) and str(value) not in self.all_signs:
                #check if its a signs
                #check if constant
                if not bool(re.search('[a-z]', str(value))) and str(value) not in self.all_signs:
                    self.constants[0] += 1
                if bool(re.search('[a-z]', str(value))):
                    self.variables[0] += 1
                    self.variable = str(value)[-1]
            # right side
            if (index > self.tokens.index(self.equal_sign)) and str(value) not in self.all_signs:
                if not bool(re.search('[a-z]', str(value))) and str(value) not in self.all_signs:
                    self.constants[1] += 1
                if bool(re.search('[a-zA-Z]', str(value))):
                    self.variables[1] += 1
            pair = False
            pair_count = 0
            if (index < self.tokens.index(self.equal_sign)):
                if (str(value) == self.open_bracket):
                    pair_count += 1
                if (str(value) == self.close_bracket):
                    pair_count += 1
                    if (pair_count == 1):
                        self.parenthesis_pair[0] += 1
                        pair_count = 0
            if (index > self.tokens.index(self.equal_sign)):
                if (str(value) == self.open_bracket):
                    pair_count += 1
                if (str(value) == self.close_bracket):
                    pair_count += 1
                    if (pair_count == 1):
                        self.parenthesis_pair[1] += 1
                        pair_count = 0
    
    # Check equation cases
    def check_cases(self):
        if self.parenthesis_pair[0] > 0 and self.parenthesis_pair[1] > 0:
            self.equation_state = "brackets_off_simplification"
        elif self.variables == [1, 0] and self.constants == [0, 1] and self.parenthesis_pair == [0, 0] and len(self.tokens[0]) != 1:
            self.equation_state = "base_case"
        elif self.variables == [1, 0] and self.constants == [0, 1] and self.parenthesis_pair == [0, 0] and self.tokens[0] == self.variable:
            self.equation_state = "solution_case"
        elif self.variables == [1, 0] and self.constants == [1, 1] and self.parenthesis_pair == [0, 0]:
            self.equation_state = "simple_base_case"
        elif self.variables == [1, 1] and self.constants == [1, 1] and self.parenthesis_pair == [0, 0]:
            self.equation_state = "terms_arrangement"
        elif self.variables > [1, 1] and self.constants == [1, 1] and self.parenthesis_pair == [0, 0]:
            self.equation_state = "algebraic_simplification"
        elif self.variables >= [1, 1] and self.constants > [1, 1] and self.parenthesis_pair == [0, 0]:
            self.equation_state = "numerical_simplification"

    # run the application and solve the equation
    def run(self):
        self.equation_tokenization()
        self.fix_signs()
        while len(self.final_solution) == 0:
            self.expression_classifier_count()
            self.check_cases()
            if self.equation_state == "solution_case":
                self.solution_case()
            elif self.equation_state == "base_case":
                self.base_case()
            elif self.equation_state == "simple_base_case":
                self.simple_base_case()
            elif self.equation_state == "terms_arrangement":
                self.terms_arrangement()
            elif self.equation_state == "algebraic_simplification":
                self.algebraic_simplification()
            elif self.equation_state == "numerical_simplification":
                self.numerical_simplification()
            elif self.equation_state == "brackets_off_simplification":
                self.numerical_simplification()
            else:
                self.error_message = "Expression cannot be classified"

        # print(instance.equation_tokenization())
        print("Hooray Solved")
        print(self.solution_steps)

if __name__ == '__main__':
    instance = Absoluver("-7x - 2 + 5 - (2x + 6 + 2x)= -21x -6 + 2 + 2x")
    instance.equation_tokenization()
    instance.expression_classifier_count()
    instance.check_cases()
    instance.parenthesis()
    instance.brackets_off_simplification()
    instance.fix_signs()
    instance.group_tokens()
    instance.numerical_simplification()
    print(instance.tokens)
    # instance.algebraic_simplification()
    # instance.terms_arrangement()
    # instance.expression_classifier_count()
    # print(instance.tokens)
    # print(instance.variables)
    # instance.check_cases()
    # instance.numerical_simplification()
    # print(instance.tokens)
    # instance.algebraic_simplification()
    # print(instance.tokens)
    # print(instance.variables)
    # print(instance.equation_state)
    # print(instance.tokens)