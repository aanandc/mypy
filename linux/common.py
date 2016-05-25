
import os,sys
import subprocess as sub
import platform
import shlex




def isWindows():
    if platform.system() is "Windows":
        return True
    else:
        return False

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def procrun(cmd):
    val = shlex.split(cmd.encode('ascii'))
    pipe = sub.Popen(val,stdout=sub.PIPE)
    if pipe.wait() != 0:
        raise sub.CalledProcessError(pipe.returncode, sub.list2cmdline(val))
    val = pipe.communicate()[0]
    return val


def redstr(string):
    return colorstr(bcolors.FAIL,string)

def colorstr(color,string):
    return color + string + bcolors.ENDC

def greenstr(string):
    return colorstr(bcolors.OKGREEN,string)

def runit2(string):
    val = shlex.split(string.encode('ascii'))
    return sub.check_output(val)

def runit(string,printit=False):
    if printit:
        print string
    cmd = os.popen(string)
    val = cmd.read()
    cmd.close()
    return val

def common_stub(main,helpprint):
    args=sys.argv
    if len(args)==1:
        helpprint()
        return
    main()


def changedir(dirname):
    os.chdir(dirname)


def readfile(filename):
    f=open(filename,'r')
    lines = f.readlines()
#Now we have all the lines , start processing
    f.close()
    return lines

def gethome():
    home=sys.argv[0]
    ch='/'
    index=home.rfind(ch)
    home=home[0:index]
    return home
