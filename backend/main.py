import json
from flask_cors import CORS, cross_origin
from flask import Flask, request
import re
import nltk
from nltk.tokenize import word_tokenize
import sys

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/', methods=['GET', 'POST'])
def index():
    solution_steps = []
    data = request.data
    equation = request.args.get('equation') or ''
    if len(equation) == 0:
        return json.dumps({"error": "No Equation found"})
    instance = Absoluver(equation)
    instance.run()
    solution_steps = instance.solution_steps
    return json.dumps({'steps': solution_steps, 'variable': instance.variable, 'equation': equation})



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
            if token == self.minus_sign and self.tokens[i-1] == self.equal_sign and self.tokens[i+1] not in self.all_signs:
                self.tokens[i+1] = self.minus_sign + str(self.tokens[i+1])
                self.tokens.pop(i)
        if no_sign_issue:
            for index, token in enumerate(self.tokens):
                if index < len(self.tokens)-1 and token not in self.all_operators and self.tokens[index+1] not in self.all_operators:
                    anser = 0

    # final case the equation is solved --> ["x", "=", a] 
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
                    if temp == self.minus_sign:
                        temp = temp + "1"
                    new_tokens.append(self.variable)
                factor = temp
            if value not in self.all_operators and index > self.tokens.index('='):
                factor2 = value

        step = f"Divide both sides by {factor}"
        new_tokens.append(self.equal_sign)
        if int(factor2) % int(factor) == 0:
            answer = eval(f"{factor2} // {factor}")
        else:
            answer = (f"{factor2}/{factor}")
        new_tokens.append(answer)

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
            "change": " ".join(change),
            "step_equation":  ' '.join(str(term) for term in sample_tokens),
            "new_equation": ' '.join(str(term) for term in new_tokens)
        }
        self.solution_steps.append(solution)
        self.tokens = new_tokens
        self.step_count += 1
        return step, sample_tokens, new_tokens

    # Simplify expression with 2 variables on the left side and two constants on the right ax + bx = c + d ---> ex = f
    def simplification_base_case(self):
        copy_tokens = self.tokens
        old_tokens = self.tokens
        step = ""
        add_tokens_left = []
        add_tokens_right = []
        left_indeces = [0, 0]
        right_indeces = [0, 0]
        # algebraic_simplification

        if self.variables == [1, 0] and self.constants == [0, 2] and len(self.tokens[0]) == 1:
            index = self.tokens.index(self.equal_sign)
            expression = " ".join(self.tokens[index+1:])
            new_answer = eval(expression)
            self.tokens = self.tokens[:index+1] + [str(new_answer)]
            self.equation_state = "solution_case"
            step = "Simplify the right hand side"
        elif self.variables == [1, 0] and self.constants == [0, 2] and len(self.tokens[0]) == 2:
            index = self.tokens.index(self.equal_sign)
            expression = " ".join(self.tokens[index+1:])
            new_answer = eval(expression)
            self.tokens = self.tokens[:index+1] + [str(new_answer)]
            self.equation_state = "base_case"
            step = "Simplify the right hand side"
        else:
            for index, term in enumerate(copy_tokens):
                if  index < copy_tokens.index(self.equal_sign) and bool(re.search("[a-z]", term)) or term in self.all_operators:
                    check_state_one = not bool(re.search("[a-z]", copy_tokens[index - 1])) and not bool(re.search("[a-z]", copy_tokens[index + 1])) 
                    check_state_two = bool(re.search("[a-z]", copy_tokens[index - 1])) and not bool(re.search("[a-z]", copy_tokens[index + 1]))
                    if bool(re.search("[a-z]", term)):
                        add_tokens_left.append(term)
                        if left_indeces[0] == 0:
                            left_indeces[0] = index
                        else:
                            left_indeces[1] = index
                    if not (check_state_one or check_state_two) and term != self.equal_sign and index < copy_tokens.index(self.equal_sign):
                        add_tokens_left.append(term)
                        if left_indeces[0] == 0:
                            left_indeces[0] = index
                        else:
                            left_indeces[1] = index
                if  index > copy_tokens.index(self.equal_sign) and not bool(re.search("[a-z]", term)) or term in self.all_operators:
                    if not bool(re.search("[a-z]", term)) and term not in self.all_operators:
                        add_tokens_right.append(term)
                        if right_indeces[0] == 0:
                            right_indeces[0] = index
                        else:
                            right_indeces[1] = index
                    if term in self.all_operators:
                        check_state_one = bool(re.search("[a-z]", copy_tokens[index - 1])) and bool(re.search("[a-z]", copy_tokens[index + 1])) 
                        check_state_two = not bool(re.search("[a-z]", copy_tokens[index - 1])) and bool(re.search("[a-z]", copy_tokens[index + 1]))
                        if not (check_state_one or check_state_two) and term != self.equal_sign and index > copy_tokens.index(self.equal_sign):
                            add_tokens_right.append(term)
                            if right_indeces[0] == 0:
                                right_indeces[0] = index
                            else:
                                right_indeces[1] = index
                    
            left_expression = ' '.join(add_tokens_left).replace(self.variable, "")
            left_answer = str(eval(f"{str(left_expression)}")) + self.variable

            right_expression = ' '.join(add_tokens_right)
            right_answer = str(eval(f"{str(right_expression)}"))
            copy_tokens = copy_tokens[:right_indeces[0]] + [str(right_answer)]
            copy_tokens = [str(left_answer)] + copy_tokens[left_indeces[1]+1:]
            self.tokens = copy_tokens
            self.fix_signs()
            step = f"Simplify right hand side terms and left hand side"

        # Create a dictionary format for the solution in order to be parsed
        solution = {
            "equation": ' '.join(str(term) for term in old_tokens),
            "step_count": str(self.step_count),
            "step": step,
            "change": "",
            "step_equation":  ' '.join(str(term) for term in self.tokens),
            "new_equation": ' '.join(str(term) for term in self.tokens)
        }
        self.solution_steps.append(solution)
        self.step_count += 1
    
    # Arrange terms: ax + c = bx + d  --->  ax - bx = d - c
    def terms_arrangement(self):
        new_terms = self.tokens
        old_tokens = self.tokens
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

        if len(right_transpose) == 1 and left_transpose[0][0] != self.minus_sign:
            right_transpose = [self.minus_sign] + right_transpose
        elif len(right_transpose) == 1 and left_transpose[0][0] == self.minus_sign:
            right_transpose = [self.plus_sign] + right_transpose

        # change signs left change
        if left_transpose[0] == self.minus_sign:
            left_transpose[0] = self.plus_sign
        elif left_transpose[0] == self.plus_sign:
            left_transpose[0] = self.minus_sign

        # change signs right change normal format
        if right_transpose[0] == self.minus_sign:
            right_transpose[0] = self.plus_sign
        elif right_transpose[0] == self.plus_sign:
            right_transpose[0] = self.minus_sign
        
        # change signs right change when sign embedded on the term
        if len(right_transpose) == 1 and right_transpose[0][0] == self.minus_sign:
            right_transpose[0] = right_transpose[0][1:]
            right_transpose.insert(0, self.plus_sign)
        new_terms = new_terms + left_transpose
        new_terms = new_terms[:new_terms.index(self.equal_sign)] + right_transpose + new_terms[new_terms.index(self.equal_sign):]
        self.tokens = new_terms
        self.fix_signs()
        
        step = f"Transpose contants to the right and algebraic terms to the left"

        # Create a dictionary format for the solution in order to be parsed
        solution = {
            "equation": ' '.join(str(term) for term in old_tokens),
            "step_count": str(self.step_count),
            "step": step,
            "change": "",
            "step_equation":  ' '.join(str(term) for term in self.tokens),
            "new_equation": ' '.join(str(term) for term in self.tokens)
        }
        self.solution_steps.append(solution)
        self.step_count += 1

    # groups tokens expression either constants and expressions together 
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

    # Helper method for simplification of algebraic terms
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

    # remove parenthesis from
    def parenthesis(self):
        start_pos = 0
        end_pos = 0
        eval_tokens = []
        coefficient = ""
        replace_position = []
        for i, term in enumerate(self.tokens):
            if term == self.open_bracket:
                start_pos = i
                if i == 0:
                    coefficient = "1"
                elif i == 1:
                    coefficient = self.tokens[i-1]
                elif self.tokens[i-1] in self.all_operators:
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
        old_tokens = self.tokens
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
                new_tokens.append(str(eval(f"{coefficient} * {value}")))
            else:
                new_tokens.append(value)
        # Replace old tokens with new ones
        # for value in tokens:
        if position[0] == 0:
            self.tokens[position[0]:position[1]] = new_tokens
        else:
            self.tokens[position[0]-1:position[1]] = new_tokens


        step = f"Distribution"
        self.fix_signs()

        # Create a dictionary format for the solution in order to be parsed
        solution = {
            "equation": ' '.join(str(term) for term in old_tokens),
            "step_count": str(self.step_count),
            "step": step,
            "change": "(" + " ".join(eval_tokens) + ")",
            "step_equation":  ' '.join(str(term) for term in new_tokens),
            "new_equation": ' '.join(str(term) for term in self.tokens)
        }
        self.solution_steps.append(solution)
        self.step_count += 1
    
    # Numerical simplify: ax + b = d + c - e  --> ax + b = f
    def numerical_simplification(self):
        copy_tokens = self.tokens
        old_tokens = self.tokens
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
            if self.constants[1] > 1 and not bool(re.search("[a-z]", term)) and index > copy_tokens.index(self.equal_sign):
                if term in self.all_operators and bool(re.search("[a-z]", copy_tokens[index - 1])) and bool(re.search("[a-z]", copy_tokens[index + 1])):
                    continue
                else:
                    if right_indeces[0] == 0:
                        right_indeces[0] = index
                    else:
                        right_indeces[1] = index
                    add_tokens_right.append(term)
        left_answer = eval(f"{' '.join(add_tokens_left)}")
        if self.constants[1] > 1:
            right_answer = eval(f"{' '.join(add_tokens_right)}")
            copy_tokens = copy_tokens[:right_indeces[0]] + [str(right_answer)] + copy_tokens[right_indeces[1]+1:]
        if str(left_answer)[0] == self.minus_sign:
            copy_tokens = copy_tokens[:left_indeces[0]] + [str(left_answer)] + copy_tokens[left_indeces[1]+1:]
        else:
            copy_tokens = copy_tokens[:left_indeces[0]] + [self.plus_sign, str(left_answer)] + copy_tokens[left_indeces[1]+1:]

        self.tokens = copy_tokens
        self.fix_signs()
        step = f"Simplify constants values"

        # Create a dictionary format for the solution in order to be parsed
        solution = {
            "equation": ' '.join(str(term) for term in old_tokens),
            "step_count": str(self.step_count),
            "step": step,
            "change": "",
            "step_equation":  ' '.join(str(term) for term in self.tokens),
            "new_equation": ' '.join(str(term) for term in self.tokens)
        }
        self.solution_steps.append(solution)
        self.step_count += 1
            
    # Group same type of terms together
    def group_tokens(self):
        # left hand side grouping
        old_tokens = self.tokens
        insert_index = 0
        for i in range(0, len(self.tokens[:self.tokens.index('=')-1])+1):
            if re.search("[a-zA-Z]", str(self.tokens[i])) and self.tokens[i] not in self.all_operators:
                if insert_index == 0:
                    if self.tokens[i-1] == '-':
                        term = '-' + self.tokens[i]
                    else:
                        term = self.tokens[i]
                    if self.tokens[0][0] != '-':
                        self.tokens = [term, "+"] + self.tokens
                    else:
                        self.tokens = [term] + self.tokens
                    insert_index = 1
                    self.tokens.pop(i+1)
                    self.tokens.pop(i+1)
                else:
                    if self.tokens[i-1] == '-':
                        term = ['-', self.tokens[i]]
                    else:
                        term = ['+', self.tokens[i]]
                    self.tokens = self.tokens[:insert_index] + term + self.tokens[insert_index:]
                    self.tokens.pop(i+1)
                    self.tokens.pop(i+1)
                    insert_index += 2
        # Right hand side grouping  
        top_index = self.tokens.index(self.equal_sign) + 1
        insert_index = 0
        if self.variables[1] + self.constants[1] >= 3:
            for i in range(len(self.tokens)-1, self.tokens.index(self.equal_sign)-1, -1):
                if not re.search("[a-zA-Z]", str(self.tokens[i])) and self.tokens[i] not in self.all_operators:
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
        step = f"Arrange and group like terms together"
        self.fix_signs()

        # Create a dictionary format for the solution in order to be parsed
        solution = {
            "equation": ' '.join(str(term) for term in old_tokens),
            "step_count": str(self.step_count),
            "step": step,
            "change": "",
            "step_equation":  ' '.join(str(term) for term in self.tokens),
            "new_equation": ' '.join(str(term) for term in self.tokens)
        }
        self.solution_steps.append(solution)
        self.step_count += 1
            
    # Algebraic simplification: ax + bx  + c = e  ---> dx + c = e
    def algebraic_simplification(self):
        # Algebraic simplification on both sides
        copy_tokens = self.tokens 
        old_tokens = self.tokens 
        add_tokens_left = []
        add_tokens_right = []
        left_indeces = [0, 0]
        right_indeces = [0, 0]
        self.expression_classifier_count()
        right_terms = []
        left_terms = []
        right_terms_indeces = []
        left_terms_indeces = []

        for index, term in enumerate(self.tokens):
            if  index < self.tokens.index(self.equal_sign):
                if bool(re.search("[a-z]", term)):
                    left_terms.append(term)
                    left_terms_indeces.append(index)
                elif term in self.all_operators and bool(re.search("[a-z]", self.tokens[index-1])) and bool(re.search("[a-z]", self.tokens[index+1])) or not bool(re.search("[a-z]", self.tokens[index-1])) and bool(re.search("[a-z]", self.tokens[index+1])):
                    left_terms.append(term)
                    left_terms_indeces.append(index)
            if  index > self.tokens.index(self.equal_sign):
                if bool(re.search("[a-z]", term)):
                    right_terms.append(term)
                    right_terms_indeces.append(index)
                elif term in self.all_operators and bool(re.search("[a-z]", self.tokens[index-1])) and bool(re.search("[a-z]", self.tokens[index+1])):
                    right_terms.append(term)
                    right_terms_indeces.append(index)
                elif term in self.all_operators and not bool(re.search("[a-z]", self.tokens[index-1])) and bool(re.search("[a-z]", self.tokens[index+1])):
                    right_terms.append(term)
                    right_terms_indeces.append(index)


        if (self.variable) in right_terms:
            index = right_terms.index(self.variable)
            right_terms[index] = "1" + self.variable
        elif (self.variable) in left_terms:
            index = left_terms.index(self.variable)
            left_terms[index] = "1" + self.variable
        if len(left_terms) > 2:
            left_expression = ' '.join(left_terms).replace(self.variable, "")
            left_answer = str(eval(f"{str(left_expression)}"))  + self.variable
            copy_tokens = [str(left_answer)] + copy_tokens[left_indeces[1]+1:]

        if len(right_terms) > 2:
            right_expression = ' '.join(right_terms).replace(self.variable, "")
            right_answer = str(eval(f"{str(right_expression)}")) + self.variable
            copy_tokens = copy_tokens[:right_terms_indeces[0]] + [str(right_answer)] + copy_tokens[right_terms_indeces[-1]+1:]
        
        self.tokens = copy_tokens
        self.fix_signs()
        
        step = f"Simplify algebraic terms"

        # Create a dictionary format for the solution in order to be parsed
        # solution = {
        #     "equation": ' '.join(str(term) for term in old_tokens),
        #     "step_count": str(self.step_count),
        #     "step": step,
        #     "change": "",
        #     "step_equation":  ' '.join(str(term) for term in self.tokens),
        #     "new_equation": ' '.join(str(term) for term in self.tokens)
        # }
        # self.solution_steps.append(solution)
        # self.step_count += 1

    # count terms - variables and constants and the count of expressions
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
        self.expression_classifier_count()
        if self.parenthesis_pair[0] > 0 or self.parenthesis_pair[1] > 0:
            self.equation_state = "brackets_off_simplification"
        elif self.variables == [1, 0] and self.constants == [0, 1] and self.parenthesis_pair == [0, 0] and len(self.tokens[0]) != 1:
            self.equation_state = "base_case"
        elif self.variables == [1, 0] and self.constants == [0, 1] and self.parenthesis_pair == [0, 0] and self.tokens[0] == self.variable and len(self.tokens[0])==1:
            self.equation_state = "solution_case"
        elif self.variables == [1, 0] and self.constants == [1, 1] and self.parenthesis_pair == [0, 0]:
            self.equation_state = "simple_base_case"
        elif self.variables == [2, 0] and self.constants == [0, 2] and self.parenthesis_pair == [0, 0]:
            self.equation_state = "simplification_base_case"
        elif self.variables == [1, 0] and self.constants == [0, 2] and self.parenthesis_pair == [0, 0]:
            self.equation_state = "simplification_base_case"
        elif self.variables == [1, 1] and self.constants == [1, 1] and self.parenthesis_pair == [0, 0]:
            self.equation_state = "terms_arrangement"
        elif self.variables >= [2, 2] and self.constants >= [2, 2] and self.parenthesis_pair == [0, 0]:
            self.equation_state = "terms_simplification"
        elif self.variables == [1, 1] and self.constants == [2, 1] and self.parenthesis_pair == [0, 0]:
            self.equation_state = "terms_simplification"
        elif self.variables > [1, 1] and self.constants > [1, 0] and self.parenthesis_pair == [0, 0]:
            self.equation_state = "terms_simplification"
        elif self.variables >= [1, 0] and self.constants >= [1, 1] and self.parenthesis_pair == [0, 0]:
            self.equation_state = "terms_simplification"

    def terms_simplification(self):
        self.group_tokens()
        if self.variables == [1, 1] and self.constants == [2, 1]:
            self.equation_state = "terms_simplification"
            self.numerical_simplification()
        if self.variables == [1, 0] and self.constants == [2, 1]:
            self.numerical_simplification()
        else:
            self.numerical_simplification()
            self.algebraic_simplification()
        

    # run the application and solve the equation
    def run(self):
        self.equation_tokenization()
        self.fix_signs()
        while len(self.final_solution) == 0:
            self.expression_classifier_count()
            self.check_cases()
            if self.equation_state == "brackets_off_simplification":
                self.brackets_off_simplification()
            elif self.equation_state == "terms_simplification":
                self.terms_simplification()
            elif self.equation_state == "terms_arrangement":
                self.terms_arrangement()
            elif self.equation_state == "simplification_base_case":
                self.simplification_base_case()
            elif self.equation_state == "simple_base_case":
                self.simple_base_case()
            elif self.equation_state == "base_case":
                self.base_case()
            elif self.equation_state == "solution_case":
                self.solution_case()
            else:
                self.error_message = "Expression cannot be classified"


if __name__ == '__main__':
    # Run the program
    app.run(host='0.0.0.0', port=8080, debug=True)
    

