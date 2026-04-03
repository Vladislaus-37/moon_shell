import sys, platform

def win(text):
    import os
    try:
        file_path = "to_print.txt"
        file_make = open(file_path, 'a')
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text)
        os.startfile(file_path, "print")
    except Exception as err:
        print([False, err])
    return 0

def unix(text, printer):
    try:
        with open(printer, "wb") as f:
            f.write(text.encode("utf-8"))
    except Exception as err:
        print([False, err])
    return 0

agrm = sys.argv[1:]
if list(platform.platform())[1] == 'Windows':
    win(' '.join(agrm))
else:
    unix(' '.join(agrm[:-1]), agrm[-1])