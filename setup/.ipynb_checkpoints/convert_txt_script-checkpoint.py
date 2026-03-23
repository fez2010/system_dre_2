import os
from pathlib import Path

with open('./outputs/txts/script.txt','r')  as f :
    lines = f.readlines()
    code_bash = []
    code_py = []
    for line in lines:
        if line[0] == '!':
            code_bash.append(line[1:])
        else:
            code_py.append(line)
    # Generate py script from input raw
    Path("./outputs/py/").mkdir(parents=True, exist_ok=True)
    with open('./outputs/py/script.py', 'w') as f:
        f.write('\n'.join(code_py))
    
    Path("./outputs/sh/").mkdir(parents=True, exist_ok=True)
    with open('./outputs/sh/script.sh', 'w') as f:
        f.write('\n'.join(['#!usr/bin/bash\n']+code_bash))