import sys
import os

agrm = sys.argv[1:]

try:
    for i in os.listdir(' '.join(agrm)):
        if os.path.isdir(' '.join(agrm) + '/' + i):
            print(f'DIR   {i}')
        elif os.path.isfile(' '.join(agrm) + '/' + i):
            print(f'FILE  {i}')
        else:
            print(f'????  {i}')
except Exception as err:
    print([False, err])