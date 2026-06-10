import sys
try:
    expression = ' '.join(sys.argv[1:])
    result = eval(expression)
    print(result)
except Exception as err:
    print([False, err])