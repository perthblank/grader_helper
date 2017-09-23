import os
from os import listdir
from os.path import isfile, join
from subprocess import Popen, PIPE, TimeoutExpired
import filecmp
import re

from util import *

_cpp = re.compile("\.cpp$")

err_count = 0

checkFolder(sample_out_path)
checkFolder(src_out_path)

input_file_names = list(getFiles(input_path))
sample_out_files = [join(sample_out_path, f) for f in map(lambda f: f+".out", input_file_names)]

src_files = list(filter(lambda f:f!=sample_src, getFilesWithPath(src_path)))
input_files = getFilesWithPath(input_path)

print("Compile Sample")
if do_compile(sample_src):
    print("Cannot compile sample")
    exit(0)
print("Run Sample")
for i in range(0, len(input_files)):
    print(" .. case " + input_file_names[i])
    do_run(input_files[i], sample_out_files[i])


indent_str = "  .."
case_len = str(len(input_file_names))
with open(result_file, 'w') as result_h:
    for f in src_files:
        if not _cpp.search(f):
            continue

        result_h.write('\n')
        result_h.write('---------------------------------------')
        result_h.write('\n')

        print("running " + f)

        name = re.search('[\w_]+\.cpp$', f).group(0)
        result_h.write('[File] ' + f + '\n')


        if do_compile(f) != 0:
            result_h.write(indent_str + '[Compile Err] ' + f + '\n')
            err_count += 1
            continue

        err = False
        passd = 0
        for i in range(0, len(input_files)):
            result_h.write('\n')
            case_name = input_file_names[i]
            out_file = join(src_out_path, name+"-"+case_name+".out")
            print(" .. case " + input_file_names[i])
            r = do_run(input_files[i], out_file)

            if r == TLE:
                result_h.write(indent_str + '[TLE] ' + case_name + '\n')
                err = True 
                continue
            elif r:
                result_h.write(indent_str + '[Execute Err] ' + case_name  + '\n')
                err = True 
                continue

            if(not filecmp.cmp(sample_out_files[i], out_file)):
                result_h.write(indent_str + '[Output Err] ' +  case_name + '\n')
                result_h.write(indent_str + '\n')
                r = Popen(['diff',sample_out_files[i] , out_file], stdout=PIPE)
                r.wait()
                diffout, errout = r.communicate()
                result_h.write(indent_str + diffout.decode("utf-8") )
                result_h.write(indent_str + '\n')
                err = True 
                continue
            
            passd += 1
            result_h.write(indent_str + '[Pass] ' + case_name + '\n')

        
        result_h.write('\n')
        result_h.write("passed " + str(passd) + "/" + case_len  + '\n')
        if(err):
            err_count += 1

    result_h.write('\nErrors ' + str(err_count) + '\n')
    
