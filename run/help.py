import sys
import os
import locale

def get_me():
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    return script_dir

lang, encoding = locale.getlocale()
if lang[:lang.find('_')] == 'Russian':
    os.chdir(f'{get_me()}/help/ru/')
else:
    os.chdir(f'{get_me()}/help/en/')

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
