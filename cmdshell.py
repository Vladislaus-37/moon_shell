import subprocess
import os
import sys
import platform

maindir = os.getcwd()
last = maindir
agrm = sys.argv[1:]
alias_name = []
alias_commands = []
mark_name = ['@pwd@', '@..@', '@home@']
mark_comms = ['os.getcwd()', 'os.getcwd()[:os.getcwd().rfind("/")+1]', 'get_homedir()']

def is_admin() -> bool:
    try:
        return os.getuid() == 0
    except AttributeError:
        import ctypes
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except (AttributeError, OSError):
            return False

def get_homedir():
    if platform.platform()[1] == 'Windows':
        return os.environ.get('USERPROFILE')
    else:
        return os.environ.get('HOME')

def get_me():
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    return script_dir

with open(os.path.join(get_me(), 'current_user_data.txt'), 'w', encoding='utf-8') as file:
    file.write(f"{get_homedir()}\n{get_homedir()}\n{get_homedir()}")

if platform.platform()[1] == 'Windows':
    py_name='python'
else:
    py_name='python3'

def add_alias(name, command):
    global alias_name, alias_commands
    alias_name += [name]
    alias_commands += [command]
    return 0

def add_mark(name, value):
    global mark_name, mark_comms
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

def cmdanal(comm):
    global last
    with open (f"{get_me()}/current_user_data.txt", 'r', encoding='utf-8') as file:
        data = file.readlines()[0].rstrip('\n')
        os.chdir(data)
    comm = mark_anal(comm).split(' ')
    cudir = os.getcwd()
    comm_dir = maindir + '/run/'


    # Check Aliases
    if comm[0] in alias_name:
        coms = (alias_commands[alias_name.index(comm[0])]+' '.join(comm[1:])).split(' & ')
        for i in coms:
            cmdanal(i)

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

    elif comm[0] == 'export':
        try:
            edit_mark(comm[1], ' '.join(comm[2:]))
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

    with open (f"{get_me()}/current_user_data.txt", 'r', encoding='utf-8') as file:
        data = file.readlines()[0].rstrip('\n')
        os.chdir(data)  
    
if agrm:
    for i in agrm:
        cmdanal(i)
    sys.exit()

while True:
    if is_admin():
        cow = input('root>$ ').rstrip(' ').strip(' ')
    else:
        cow = input('$ ').rstrip(' ').strip(' ')
    cow = cow.split(' && ')
    for i in cow:
        cmdanal(i)
