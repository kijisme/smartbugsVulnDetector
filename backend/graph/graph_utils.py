import re

''' 获得当前文件的solc版本'''
def get_solc_version(sol_file_path):

    pattern =  re.compile(r'\d.\d.\d+')

    with open(sol_file_path, 'r') as f:
        line = f.readline()
        while line:
            if 'pragma solidity' in line:
                if len(pattern.findall(line)) > 0:
                    return pattern.findall(line)[0]
                else:
                    return None
            line = f.readline()

    return None