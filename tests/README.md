# Unittest and Integration Test Guide

## Available Tests Scripts

* integration_test.py
    -To run the integration tests cases which are writeen in integration_test.json
* unittest.py
    -To run the unit tests cases which are writeen in unittest_test.json


<!-- # How tests are implemented? -->

<!-- ## Unit Tests  -->




## How to run tests?

To run the integration tests

Run
bash`
python integration_test.py
`

To run the unit tests

Run
bash`
python unittest.py
`


### Unit Tests

|Test Number   | Test Case  |  Input | Expected Output  |
| --- | --- | --- | --- | ---|
|  1  | Tokenisation instance equation  | 7x - 2 = 21  | ['7x', '-', '2', '=', '21'] |
|  2  | Tokenisation function  |  2x - 2  | ['2x', '-', '2'] |
|  3  | Expression term count  | 7x - 2 = 21  | [1, 0], [1, 1], [0, 0] |
|  4  | Check cases  | 7x - 2 = 21  | simple base case |
|  5  | Simple Base Case Method  | 7x - 2 = 21  | 7x = 23 |
|  6  | Base case coefficient  | 7x = 23 | x = 23/7 |
|  7  | Bracket off function  | 2(4x + 3) + 6 = 24 - 4x | 8x + 6 +6 = 24 - 4x |
|  8  | Term grouping  |  2x + 3 + 4x = 24 - 6x   | 2x + 4x + 3 = 24 - 6x |
|  9  | Expression simplification  | 8x + 6 + 6 = 24 - 4x + 2x   | 8x + 12 = 24 - 2x |
|  10 | Algebraic Simplification  | 8x + 6x + 2 = 24 - 4x   | 14x + 2 = 24 - 4x |
|  11 | Numerical Simplification  | 8x + 6 + 8 + 6 = 20  | 8x + 20 = 20 |
|  12 | Fix a broken expression  | 8x - + 2 = 24 - 4  | 8x - 2 = 24 - 4 |

### Integration Tests Cases

| Test Number | Test Case | Input Equation | Expected Output |  
| --- | --- | --- | --- |
| 1 | simple | -x = 4 | x=-4 |
| 2 | simple | x - 2 = 6 | x=8 |
| 3 | simple | x = 6 + 5 | x=11 |
| 4 | simple | -2x - 2 = 8 | x=-5 |
| 5 | simple | 4x - 14 = 10 | x=6 |
| 6 | basic | 2y - 2 + 5 = 4 | y=1/2 |
| 7 | basic | 6 + 10x - 2 = 34 | x=3 |
| 8 | basic | 6x + 2 + 26 = 4x + x | x=-28 |
| 9 | basic | 15x - 5 = 0 | x=1/3 |
| 10 | basic | 7x - 2 = 21 | x=23/7 |
| 11 | expanded | 5x - 2 + 2x = 21 + 6x |x=23 |
| 12 | expanded | 6 + 2y + 3 = 7 + 4y + 3 |x=-1/2 |
| 13 | expanded | -10x + 5 + 2x = -2x - 3x + 1 |x=4/3 |
| 14 | expanded | -x + 3x + x = 5 + 2x |x=5 |
| 15 | expanded | 2(x + 3) = 4 |x=-1 |
| 16 | complex | -2(2x + 10) + 6 = 10 | x=-6 |
| 17 | complex | -5(x - 2) - 5 = 10(x + 3) | x=-7/3 |
| 18 | complex | 7x + 2(3x + 4x - 2) = 10(4 + x) |  x=7/8 |
| 19 | complex | 5x + 4(4x - 8x + 2) = 21x+6 | x=1/16 |
| 20 | complex | 2(4x + 3) + 6 = 24 -4x | x=1 |
