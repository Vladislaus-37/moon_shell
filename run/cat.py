import sys
import os

try:
    file_path = sys.argv[1]
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        print(content)
except Exception as err:
    print([False, err])