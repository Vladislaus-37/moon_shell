import sys

try:
    agrm = sys.argv[1:]

    with open(agrm[1], 'a'):
        pass

    with open(agrm[0], 'b+r') as file1:
        x = file1.read()
    with open(agrm[1], 'b+w') as file2:
        file2.write(x)
except Exception as err:
    print([False, err])
