import json
import requests
  
# Opening JSON file
test_cases = open('./integration_tests.json')
  
# returns JSON object as 
# a dictionary
data = json.load(test_cases)
  
# Iterating through the json
# list
print("{:<10} {:<20} {:<25} {:<25} {:<25} {:<10}".format('Test No.','Test Case','Test Input','Expected Output', 'Code Output', 'Result'))
for case in data['test_cases']:
    equation = case["test_input"]
    get_url = f"http://localhost:5000?equation={equation}"
    results = requests.get(get_url)
    code_output = results.json()["steps"][-1]['new_equation']
    test_result = "fail"
    if code_output == case["expected_output"]:
        print("pass")
        test_result = "pass"

    print("{:<10} {:<20} {:<25} {:<25} {:<25} {:<10}".format(case["test_number"], case["test_case"], case["test_input"],case["expected_output"], code_output, test_result)) 
  
# Closing file
test_cases.close()