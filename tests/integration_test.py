import json
import sys
import re
sys.path.insert(1, '../backend')

from main import Absoluver

# Opening JSON file with test cases
test_cases = open('./integration_test_cases.json')
  
# returns JSON object as 
# a dictionary
data = json.load(test_cases)
  
# Iterating through the json


def compare_results(code_output, expected_output):
    pass


print("{:<10} {:<20} {:<25} {:<25} {:<25} {:<10}".format('Test No.','Test Case','Test Input','Expected Output', 'Code Output', 'Result'))
for case in data['test_cases']:
    equation = case["test_input"]
    instance = Absoluver(equation)
    instance.run()
    results = instance.solution_steps
    code_output = results[-1]['new_equation']
    test_result = "fail"
    if code_output == case["expected_output"]:
        print("pass")
        test_result = "pass"

    print("{:<10} {:<20} {:<25} {:<25} {:<25} {:<10}".format(case["test_number"], case["test_case"], case["test_input"],case["expected_output"], code_output, test_result)) 
  
# Closing file
test_cases.close()