import subprocess
import os
import sys

maindir = os.getcwd()
last = maindir
agrm = sys.argv[1:]

def cmdanal(comm):
    global last
    comm = comm.split(' ')
    cudir = os.getcwd()
    os.chdir(maindir + '/run/')

    # Built is`s
    if comm[0] == 'ls':
        subprocess.run(['python'] + [comm[0] + '.py'] + [cudir], shell=False)
        os.chdir(cudir)
    elif comm[0] == 'cd':
        if comm[1] == '-':
            os.chdir(last)
            last = cudir
        else:
            os.chdir(' '.join(comm[1:]))
            last = cudir
    elif comm[0] == 'exit':
        sys.exit()
    elif comm[0] == 'pwd':
        print(cudir)
    
    # In delevery
    elif (comm[0] + '.py') in os.listdir(maindir + '/run/'):
        subprocess.run('python ' + comm[0] + '.py ' + ' '.join(comm[1:]), shell=False)
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
    cmdanal(cow)