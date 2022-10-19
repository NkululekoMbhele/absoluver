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

