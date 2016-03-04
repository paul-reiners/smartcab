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
    output_file.write('succeeded\n') 
    with open(input_file_name) as input_file:
        lines = input_file.readlines()
        trial_start_lines = []
        for i in range(len(lines)):
            line = lines[i]
            if 'Simulator.run()' in line:
                trial_start_lines.append(i)
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
                    reg_ex = "total_reward = (\d+\.\d+)"
                    m = re.search(reg_ex, next_line)
                    total_reward_str = m.group(1)
                    total_reward = float(total_reward_str)
                    if total_reward >= 0.0:
                        succeeded = True
                    else:
                        succeeded = False
                if not succeeded is None:
                    if succeeded:
                        successes += 1
                        output_file.write('1\n') 
                    else:
                        failures += 1
                        output_file.write('0\n') 
                    done = True
                else:
                    current_line_num += 1
    print "successes:", successes
    print "failures: ", failures
    output_file.close()
        
if __name__ == '__main__':
    input_file_name = sys.argv[1]
    output_file_name = sys.argv[2]
    analyze_data(input_file_name, output_file_name)