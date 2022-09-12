# App Name: Linear Equation Basic Math Solver
# Author: Nkululeko Mbhele
# Date Created: 12 September 2022

#Module imports  
import re, string
import nltk
from nltk.tokenize import word_tokenize

class Absoluver():
    def __init__(self, equation):
        #operations instances
        self.all_signs = ["+", "-", "*", "/", "(", ")"]
        self.all_operations = ["+", "-", "*", "/"]
        self.plus_sign = ["+"]
        self.minus_sign = ["-"]
        self.times_sign = ["*"]
        self.divide_sign = ["/"]
        self.open_bracket = ["("]
        self.close_bracket = [")"]

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
    #     pass


if __name__ == "__main__":
    instance = Absoluver("2x + 3 = 4")
    print(instance.equation_tokenization())

        