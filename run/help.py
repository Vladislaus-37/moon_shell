import sys
import os
import locale

lang, encoding = locale.getlocale()
if lang[:lang.find('_')] == 'Russian':
    os.chdir('./help/ru')
else:
    os.chdir('./help/en')

agrm = sys.argv[1:]

try:
    if not agrm:
        with open('main.txt', 'r', encoding='utf-8') as file:
            print(file.read())
    else:
        with open(f'{agrm[0]}.txt', 'r', encoding='utf-8') as file:
            print(file.read())
except FileNotFoundError:
    print([False, 'Custom or existen`t command'])
except Exception as err:
    print([False, err])