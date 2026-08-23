import subprocess
import os
import sys
import platform

maindir = os.getcwd()
last = maindir
agrm = sys.argv[1:]
alias_name = []
alias_commands = []
mark_name = []
mark_comms = []

def is_admin() -> bool:
    is_wine = False
    try:
        import ctypes
        if hasattr(ctypes.cdll.ntdll, 'wine_get_version'):
            is_wine = True
    except (AttributeError, OSError):
        pass
    try:
        return os.getuid() == 0
    except AttributeError:
        if is_wine:
            return False
        import ctypes
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except (AttributeError, OSError):
            return False

def get_homedir():
    is_wine = 'WINEHOMEDIR' in os.environ
    if is_wine:
        try:
            script_path = get_me() 
            if script_path and len(script_path) > 2 and script_path[1] == ':':
                drive_letter = script_path[0]
                return f"{drive_letter}:\\home\\vladislaus"
        except Exception:
            pass
        wine_home = os.environ.get('WINEHOMEDIR')
        if wine_home:
            return wine_home
    if platform.system() == 'Windows':
        return os.environ.get('USERPROFILE')
    else:
        return os.environ.get('HOME')

def get_me():
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    return script_dir

data_path = os.path.join(get_me(), 'current_user_data.txt')
try:
    with open(data_path, 'w', encoding='utf-8') as file:
        file.write(f"{os.getcwd()}\n{get_homedir()}\n")
except Exception as e:
    print([False, e])

def find_python_executable() -> str:
    if sys.executable and os.path.exists(sys.executable):
        return sys.executable

    if os.name == 'nt': 
        exe_name = 'python.exe'
    else:
        exe_name = 'python3'
    system_path = shutil.which(exe_name) or shutil.which('python')
    if system_path:
        return system_path

    if os.name == 'nt':
        appdata_python = os.path.expandvars(r"%USERPROFILE%\AppData\Local\Programs\Python\Python313\python.exe")
        if os.path.exists(appdata_python):
            return appdata_python
        if os.path.exists(r"C:\Python313\python.exe"):
            return r"C:\Python313\python.exe"

    return 'python'

py_name = find_python_executable()
print(f"[DEBUG] Имя интерпретатора определено как: {py_name}")

def msh_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                for part in line.split(" && "):
                    cmd(part.strip())
    except Exception as e:
        print([False, e])

def add_alias(name, command):
    global alias_name, alias_commands
    alias_name += [name]
    alias_commands += [command]
    return 0

def add_mark(name, value):
    global mark_name, mark_comms
    try:
        eval(value)
    except Exception as e:
        print([False, e, "REMINDER: Required python3 expression"])
        return 1
    mark_name.append(f'@{name}@')
    mark_comms.append(str(value))
    return 0

def edit_mark(name, value):
    global mark_comms
    mark_comms[mark_name.index(f'@{name}@')] = str(value)
    return 0

def mark_anal(command):
    for i in mark_name:
        command = command.replace(i, str(eval(mark_comms[mark_name.index(i)])))
    return command

def cmd(comm):
    global last
    data_path = f"{get_me()}/current_user_data.txt"
    try:
        with open(data_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            if lines:
                data = lines[0].rstrip('\n')
                os.chdir(data)

    except Exception as e:
        print([False, e])

    comm = mark_anal(comm).split(' ')
    cudir = os.getcwd()
    comm_dir = maindir + '/run/'


    # Check Aliases
    if comm[0] in alias_name:
        coms = (alias_commands[alias_name.index(comm[0])]+' '.join(comm[1:])).split(' & ')
        for i in coms:
            for j in i.split(" && "):
                cmdanal(j)

     # Built in commands

    elif comm[0] == 'mark':
        try:
            if comm[1] == 'add':
                add_mark(comm[2], ' '.join(comm[3:]))
            elif comm[1] == 'edit':
                edit_mark(comm[2], ' '.join(comm[3:]))
            elif comm[1] == 'list':
                for i in mark_name:
                    cm = mark_comms[mark_name.index(i)]
                    print(f'{i} : {cm}')

        except Exception as err:
             print([False, err])

    elif comm[0] == 'alias':
        try:
            add_alias(comm[1], ' '.join(comm[2:]))
        except Exception as err:
            print([False, err])

    elif comm[0] == 'exit':
        sys.exit()

    elif comm[0] == 'root':
        subprocess.run(['sudo']+ [py_name] + [f'{get_me()}/cmdshell.py'], shell=False)
        sys.exit()

    elif comm[0] == '':
        pass

    # In delevery
    elif (comm[0] + '.py') in os.listdir(maindir + '/run/'):
        subprocess.run([py_name] + [comm_dir + comm[0] + '.py'] + comm[1:], shell=False)

    # Other
    elif comm[0] != 'help':
        try:
            subprocess.run(comm, shell=False)
            os.chdir(cudir)
        except Exception as err:
            print([False, err])
    return 0 

msh_file(f"{maindir}/.mshrc")

if agrm:
    for i in agrm:
        for j in i.split(" && "):
            cmd(j)
    sys.exit()

while True:
    if is_admin():
        cow = input('root>$ ').rstrip(' ').strip(' ')
    else:    
        with open (f"{get_me()}/current_user_data.txt", 'r', encoding="utf-8") as file:
            data = file.readlines()[0].rstrip('\n')
            os.chdir(data)
        print(mark_anal("@ps1@"), end="")
        cow = input().rstrip(' ').strip(' ')
    cow = cow.split(' && ')
    for i in cow:
        cmd(i)
