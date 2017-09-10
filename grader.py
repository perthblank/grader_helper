import os
from os import listdir
from os.path import isfile, join
from subprocess import Popen, PIPE, TimeoutExpired
import re
import filecmp

root_path = 'test/'
answer_src = 'sample.cpp'
result_file = 'res.txt'
TLE_time = 2
output_dir = 'output/'
_cpp = re.compile("\.cpp$")
input_file = 'input.txt'

compiler_cmd = 'g++'
exe_name = 'a.out'
answer_output = 'standard.out'

_TLE = 100

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

files = [join(root_path, f) for f in listdir(root_path) if isfile(join(root_path, f)) and f!=answer_src]
err_count = 0

def _compile(f):
    try:
        r = Popen([compiler_cmd, f, '-o', exe_name])
    except:
        return 1
    r.wait()
    return r.returncode

def _run(out_f):
    try:
        with open(out_f, 'w') as out_h: 
            with open(input_file, 'r') as input_h:
                r = Popen(['./' + exe_name], stdin=input_h, stdout=out_h)
                r.wait(timeout=TLE_time)
    except TimeoutExpired:
        r.kill()
        return _TLE
    except:
        return 1
    return r.returncode


print("Compile Sample")
if _compile(answer_src):
    print("Cannot compile sample")
    exit(0)
print("Run Sample")
_run(answer_output)

with open(result_file, 'w') as result_h:
    for f in files:
        if not _cpp.search(f):
            continue

        print("running " + f)

        name = re.search('[\w_]+\.cpp$', f).group(0)
        output_file = join(output_dir, name+".out")

        if _compile(f) != 0:
            result_h.write('[Compile Err] ' + f + '\n')
            err_count += 1
            continue

        r = _run(output_file)
        if r == _TLE:
            result_h.write('[TLE] ' + f + '\n')
            err_count += 1
            continue
        elif r:
            result_h.write('[Execute Err] ' + f + '\n')
            err_count += 1
            continue

        if(not filecmp.cmp(answer_output, output_file)):
            result_h.write('[Output Err] ' + f + '\n')
            result_h.write('\n')
            r = Popen(['diff', answer_output, output_file], stdout=PIPE)
            r.wait()
            diffout, err = r.communicate()
            result_h.write(diffout.decode("utf-8") )
            result_h.write('\n')
            err_count += 1
            continue

        result_h.write('[Pass] ' + f + '\n')

    result_h.write('\nErrors ' + str(err_count) + '\n')
    
