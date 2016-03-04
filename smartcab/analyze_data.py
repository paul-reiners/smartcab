#!/usr/bin/python

'''
Created on Mar 3, 2016

@author: Paul Reiners
'''

import sys
import re

def analyze_data(input_file_name, output_file_name):
    successes = 0
    failures = 0
    output_file = open(output_file_name,'w')
    output_file.write('trial,succeeded\n') 
    with open(input_file_name) as input_file:
        lines = input_file.readlines()
        trial_start_lines = []
        for i in range(len(lines)):
            line = lines[i]
            if 'Simulator.run()' in line:
                trial_start_lines.append(i)
        trial = 0
        for trial_start_line in trial_start_lines:
            done = False
            current_line_num = trial_start_line
            while not done:
                line = lines[current_line_num]
                succeeded = None
                if 'Primary agent could not reach destination within deadline!' in line:
                    succeeded = False
                elif 'Primary agent has reached destination!' in line:
                    next_line = lines[current_line_num + 1]
                    total_reward = get_float_from_line("total_reward", next_line)
                    if total_reward >= 0.0:
                        succeeded = True
                    else:
                        succeeded = False
                if not succeeded is None:
                    if succeeded:
                        successes += 1
                        succeeded_str = '1' 
                    else:
                        failures += 1
                        succeeded_str = '0' 
                    output_file.write(str(trial) + ',' + succeeded_str + '\n')
                    done = True
                    trial += 1
                else:
                    current_line_num += 1
    print "successes:", successes
    print "failures: ", failures
    output_file.close()
  
    
def get_int_from_line(name, line):
    val_str = get_num_str_from_line(name, line)
    val = int(val_str)
    
    return val
  
    
def get_float_from_line(name, line):
    val_str = get_num_str_from_line(name, line)
    val = float(val_str)
    
    return val


def get_num_str_from_line(name, line):
    reg_ex = name + " = (\d+\.\d+)"
    m = re.search(reg_ex, line)
    val_str = m.group(1)

    return val_str
        
        
if __name__ == '__main__':
    input_file_name = sys.argv[1]
    output_file_name = sys.argv[2]
    analyze_data(input_file_name, output_file_name)