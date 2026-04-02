import os
import sys
try:
    agrm = sys.argv[1:]
    os.mkdir(' '.join(agrm))
except Exception as err:
    print([False, err])