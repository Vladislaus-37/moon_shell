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

def get_homedir():
    if platform.platform()[1] == 'Windows':
        return os.environ.get('USERPROFILE')
    else:
        return os.environ.get('HOME')

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
    comm = mark_anal(comm).split(' ')
    cudir = os.getcwd()
    comm_dir = maindir + '/run/'

    # Check Aliases
    if comm[0] in alias_name:
        coms = (alias_commands[alias_name.index(comm[0])]+' '.join(comm[1:])).split(' & ')
        for i in coms:
            cmdanal(i)

     # Built is`s
    elif comm[0] == 'ls':
        subprocess.run(['python'] + [comm_dir + comm[0] + '.py'] + [cudir],shell=False)

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

    elif comm[0] == 'cd':
        try:
            if comm[1] == '-':
                os.chdir(last)
                last = cudir
            else:
                os.chdir(' '.join(comm[1:]))
                last = cudir
        except Exception as err:
            print([False, err])

    elif comm[0] == 'exit':
        sys.exit()

    elif comm[0] == 'pwd':
        print(cudir)

    elif comm[0] == 'sudo':
        subprocess.run(['sudo']+['python'] + [comm_dir + comm[0] + '.py'] + [cudir] + comm[1:], shell=False)

    elif comm[0] == 'echo':
        print(' '.join(comm[1:]))


    # In delevery
    elif (comm[0] + '.py') in os.listdir(maindir + '/run/'):
        subprocess.run(['python'] + [comm_dir + comm[0] + '.py'] + comm[1:], shell=False)
        os.chdir(cudir)

    # Other
    elif comm[0] != 'help':
        try:
            subprocess.run(comm, shell=False)
            os.chdir(cudir)
        except Exception as err:
            print([False, err])
    return 0

if agrm:
    for i in agrm:
        cmdanal(i)
    sys.exit()

while True:
    cow = input('$ ').rstrip(' ').strip(' ')
    cow = cow.split(' && ')
    for i in cow:
        cmdanal(i)
