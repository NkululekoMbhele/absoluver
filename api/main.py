import json
from flask_cors import CORS, cross_origin
from flask import Flask, request
import re, string
import nltk
from nltk.tokenize import word_tokenize

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'



@app.route('/', methods=['GET', 'POST'])
def index():
    solution_steps = []
    data = request.data
    equation = request.args.get('equation')
    tokens = get_expression_array(equation)
    step, sample_tokens, new_tokens = simple_expression(tokens)
    solution_steps.append({
        'step': step, 'sample': ' '.join(str(token) for token in sample_tokens), 'new_equation': ' '.join(str(token) for token in new_tokens)
    })
    step2, sample_tokens2, new_tokens2 = divide_expression(tokens)
    solution_steps.append({
        'step': step2, 'sample': ' '.join(str(token) for token in sample_tokens2), 'new_equation': ' '.join(str(token) for token in new_tokens2)
    })
    print(equation)

    return json.dumps({'steps': solution_steps})

@app.route('/test', methods=['GET', 'POST'])
def test():
    instance = Absoluver("2x + 3 = 4")
    print(instance.equation_tokenization())
    return json.dumps({'steps': instance.equation_tokenization()})


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

        # Solution Steps
        self.solution_steps = []
        self.tokens = []

    # Create tokens(string array) from the equation e.g "2x + 3 = 1" --> ["2x", "+", "3", "=", "1"]
    def equation_tokenization(self):
        trimmed = self.equation.replace(" ", "")
        spaced_equation = re.sub("[\(\+\-\)=]",  lambda operator: " " + operator[0] + " ", trimmed)
        tokenized_equation =  word_tokenize(spaced_equation)
        self.tokens = tokenized_equation
        return tokenized_equation

    # Fix signs error and misplacements e.g [12, "-", "-8"] --> ["12", "+", "8"]
    def fix_signs(self, tokens):
        signs = ["("]
        for index, token in enumerate(tokens):
            if token == self.minus_sign and index == 0 and tokens[index + 1] != self.close_bracket:
                tokens[index + 1] = token + tokens[index + 1]
                tokens.pop(index)
            if token == self.plus_sign and str(tokens[index + 1])[0] == self.minus_sign:
                tokens[index] = self.minus_sign
                tokens[index+1] = str(tokens[index + 1])[1:]
            if token == self.minus_sign and str(tokens[index + 1])[0] == self.minus_sign:
                tokens[index] = self.plus_sign
                tokens[index+1] = str(tokens[index + 1])[1:]
        return tokens
    
    # def equation_classifier(self):

    # Simple Base  Case: ax + b = c  ---> ax = d
    def simple_base_case(self, tokens):
        signs = ["+", "-", "*", "/" ,"=" ]
        new_tokens = []
        sample_tokens = []
        step = ""
        value_change = ""
        factor = ""
        factor2 = ""
        operator = ""
        for index, value in enumerate(tokens):
            if value not in self.all_operators and index < tokens.index(self.equal_sign) and value.isdigit():
                factor = value
                operator = tokens[index-1]
            elif value not in self.all_operators and index > tokens.index(self.equal_sign) and value.isdigit():
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

        position = tokens.index(self.equal_sign)
        change = get_expression_array(value_change)
        sample_tokens = tokens[0:position] + change + tokens[position:] + change
        return step, sample_tokens, new_tokens

    # Base Case: ax = b --> x = b
    def base_case(self, tokens):
        new_tokens = []
        sample_tokens = []
        step = ""
        value_change = ""
        factor = ""
        factor2 = ""
        for index, value in enumerate(tokens):
            if not str(value).isdigit() and value not in self.all_operators and index < tokens.index('='):
                temp = ""
                for i in value:
                    if not i.isdigit():
                        new_tokens.append(i)
                    if i.isalpha():
                        temp = value
                        temp = ''.join(j for j in temp if j.isdigit())
                factor = temp
            if value not in self.all_operators and index > tokens.index('='):
                factor2 = value

        # print(f"{factor2} = {factor}")
        step = f"Divide both sides by {factor}"
        new_tokens.append("=")
        answer = int(factor2) / int(factor)
        new_tokens.append(round(answer, 2))

        position = tokens.index("=")
        change = get_expression_array("/" + factor)
        sample_tokens = tokens[0:position] + change + tokens[position:] + change

        return step, sample_tokens, new_tokens

    # Arrange terms: ax + c = bx + d  --->  ax - bx = d - c
    def terms_arrangement(self, tokens):
        pass
    
    # Remove brackets: a(bx + c) = d  ---> abx + ac = d
    def brackets_off_simplification(self, tokens):
        pass
    
    # Numerical simplify: ax + b = d + c - e  --> ax + b = f
    def numerical_simplification(self, tokens):
        pass
    
    # Algebraic simplification: ax + bx  + c = e  ---> dx + c = e
    def algebraic_simplification(self, tokens):
        pass

    # run the application and solve the equation
    def run(self):
        pass
    
    
if __name__ == '__main__':
    print("Starting")
    instance = Absoluver("2x + 3 = 4")
    print(instance.equation_tokenization())
    app.run()