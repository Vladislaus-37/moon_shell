import sys

try:
    agrm = sys.argv[1:]
    with open(agrm[0], 'a', encoding='utf-8') as file:
        try:
            file.write(' '.join(agrm[1:])+'\n')
        except:
            pass
except Exception as err:
    print([False, err])
