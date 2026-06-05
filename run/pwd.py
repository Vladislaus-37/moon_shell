import sys
import os

def get_me():
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    return script_dir

root_dir = os.path.dirname(get_me())
with open(os.path.join(root_dir, 'current_user_data.txt'), 'r', encoding='utf-8') as file:
    agrm = file.readlines()[0].rstrip('\n')

print(agrm)