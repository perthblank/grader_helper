import os
from os import listdir
from os.path import isfile, join
from subprocess import Popen, PIPE, TimeoutExpired
from configs import *

compiler_cmd = 'g++'
exe_name = 'a.exe'

TLE = 100

def checkFolder(path):
    if not os.path.exists(path):
        os.makedirs(path)

def getFiles(path):
    return [f for f in listdir(path) if isfile(join(path, f))] 

def getFilesWithPath(path):
    return [join(path, f) for f in getFiles(path)] 

def do_compile(f):
    try:
        r = Popen([compiler_cmd, f, '-o', exe_name])
    except:
        return 1
    r.wait()
    return r.returncode

def do_run(input_f, out_f):
    try:
        with open(out_f, 'w') as out_h: 
            with open(input_f, 'r') as input_h:
                r = Popen(['./' + exe_name], stdin=input_h, stdout=out_h)
                r.wait(timeout=TLE_time)
    except TimeoutExpired:
        r.kill()
        return TLE
    except:

        return 1
    return r.returncode


