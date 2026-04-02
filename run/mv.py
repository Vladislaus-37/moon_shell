import sys
import os

try:
    agrm = sys.argv[1:]
    os.rename(agrm[0], agrm[1])
except Exception as err:
    print([False, err])