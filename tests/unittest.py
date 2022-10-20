import json
import sys
sys.path.insert(1, '../backend')

# Import the class
from main import Absoluver


# Opening JSON file
test_cases = open('./unittest_cases.json')
  
# returns JSON object as 
# a dictionary
data = json.load(test_cases)


def compare_results(case):

    test_result = "fail"
    code_output = ""

    if case["test_number"] == 1:
        equation = case["test_input"]
        instance = Absoluver(equation)
        instance.equation_tokenization()
        results = instance.tokens
        code_output = results
        if code_output == expected_output:
            test_result = "pass"
    elif case["test_number"] == 2:
        equation = case["test_input"]
        instance = Absoluver(equation)
        results = instance.expression_tokenization(equation)
        code_output = results
        if code_output == expected_output:
            test_result = "pass"
    elif case["test_number"] == 3:
        equation = case["test_input"]
        instance = Absoluver(equation)
        instance.run()
        variables, constants, parenthesis = instance.variables, instance.constants, instance.parenthesis_pair
        code_output = [variables, constants, parenthesis]
        if code_output == expected_output:
            test_result = "pass"
    elif case["test_number"] == 4:
        equation = case["test_input"]
        instance = Absoluver(equation)
        instance.equation_tokenization()
        instance.fix_signs()
        instance.expression_classifier_count()
        instance.check_cases()
        results = instance.equation_state
        code_output = results.replace("_", " ")
        if code_output == expected_output:
            test_result = "pass"
    elif case["test_number"] == 5:
        equation = case["test_input"]
        instance = Absoluver(equation)
        instance.equation_tokenization()
        instance.fix_signs()
        instance.expression_classifier_count()
        instance.check_cases()
        instance.simple_base_case()
        results = ' '.join(str(term) for term in instance.tokens)
        code_output = results
        if code_output == expected_output or (code_output.replace(" ", "")) == expected_output or code_output.lower() == expected_output.lower() :
            test_result = "pass"
    elif case["test_number"] == 6:
        equation = case["test_input"]
        instance = Absoluver(equation)
        instance.equation_tokenization()
        instance.fix_signs()
        instance.expression_classifier_count()
        instance.check_cases()
        instance.simple_base_case()
        instance.base_case()
        results = ' '.join(str(term) for term in instance.tokens)
        code_output = results
        if code_output == expected_output:
            test_result = "pass"
    elif case["test_number"] == 7:
        equation = case["test_input"]
        instance = Absoluver(equation)
        instance.equation_tokenization()
        instance.fix_signs()
        instance.expression_classifier_count()
        instance.check_cases()
        instance.brackets_off_simplification()
        results = ' '.join(str(term) for term in instance.tokens)
        code_output = results
        if code_output == expected_output:
            test_result = "pass"
    elif case["test_number"] == 8:
        equation = case["test_input"]
        instance = Absoluver(equation)
        instance.equation_tokenization()
        instance.fix_signs()
        instance.expression_classifier_count()
        instance.check_cases()
        instance.group_tokens()
        results = ' '.join(str(term) for term in instance.tokens)
        code_output = results
        if code_output == expected_output:
            test_result = "pass"
    elif case["test_number"] == 9:
        equation = case["test_input"]
        instance = Absoluver(equation)
        instance.equation_tokenization()
        instance.fix_signs()
        instance.expression_classifier_count()
        instance.check_cases()
        instance.terms_simplification()
        results = ' '.join(str(term) for term in instance.tokens)
        code_output = results
        if code_output == expected_output:
            test_result = "pass"
    elif case["test_number"] == 10:
        equation = case["test_input"]
        instance = Absoluver(equation)
        instance.equation_tokenization()
        instance.fix_signs()
        instance.expression_classifier_count()
        instance.check_cases()
        instance.algebraic_simplification()
        results = ' '.join(str(term) for term in instance.tokens)
        code_output = results
        if code_output == expected_output:
            test_result = "pass"
    elif case["test_number"] == 11:
        equation = case["test_input"]
        instance = Absoluver(equation)
        instance.equation_tokenization()
        instance.fix_signs()
        instance.expression_classifier_count()
        instance.check_cases()
        instance.numerical_simplification()
        results = ' '.join(str(term) for term in instance.tokens)
        code_output = results
        if code_output == expected_output:
            test_result = "pass"
    elif case["test_number"] == 12:
        equation = case["test_input"]
        instance = Absoluver(equation)
        instance.equation_tokenization()
        instance.fix_signs()
        results = ' '.join(str(term) for term in instance.tokens)
        code_output = results
        if code_output == expected_output:
            test_result = "pass"
    return test_result, code_output


print("{:<10} {:<20} {:<25} {:<25} {:<25} {:<10}".format('Test No.','Test Case','Test Input','Expected Output', 'Code Output', 'Result'))
for case in data['test_cases']:
    test_result, code_output = compare_results(case)
    print("{:<10} {:<20} {:<25} {:<25} {:<25} {:<10}".format(case["test_number"], case["test_case"], case["test_input"],case["expected_output"], code_output, test_result)) 
  
# Closing file
test_cases.close()

