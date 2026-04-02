import os
import sys

try:
    agrm = sys.argv[1:]
    if os.path.isfile(' '.join(agrm)):
        os.remove(' '.join(agrm))
    elif os.path.isdir(' '.join(agrm)):
        os.rmdir(' '.join(agrm))
except Exception as err:
    print([False, err])