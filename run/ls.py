import sys
import os

def get_me():
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    return script_dir

if '-a' in sys.argv:
    all_content = True
else:
    all_content = False


root_dir = os.path.dirname(get_me())
with open(os.path.join(root_dir, 'current_user_data.txt'), 'r', encoding='utf-8') as file:
    agrm = file.readlines()[0].rstrip('\n')
try:
    for i in os.listdir(agrm):
        if i[0] != "." or all_content:
            if os.path.isdir(os.path.join(agrm, i)):
                print(f'DIR   {i}')
            elif os.path.isfile(os.path.join(agrm, i)):
                print(f'FILE  {i}')
            else:
                print(f'????  {i}')
except Exception as err:
    print([False, err])