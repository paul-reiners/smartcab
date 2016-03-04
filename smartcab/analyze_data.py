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
    columns = \
        ['trial', 'succeeded', 'deadline', 'last_step_deadline', 'num_steps', \
         'total_reward', 'max_possible_reward', 'performance']
    for column in columns:
        output_file.write(column + ',')
    output_file.write('\n') 
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
            current_line_num += 1
            line = lines[current_line_num]
            deadline = get_int_from_line('deadline', line)
            while not done:
                line = lines[current_line_num]
                succeeded = None
                if 'Primary agent could not reach destination within deadline!' in line:
                    succeeded = False
                    prev_line = lines[current_line_num - 1]
                    total_reward = get_float_from_line("total_reward", prev_line)
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
                        current_line_num += 1
                        line = lines[current_line_num]
                        last_step_deadline = get_int_from_line('deadline', line)
                    else:
                        failures += 1
                        succeeded_str = '0' 
                        last_step_deadline = 0
                    num_steps = deadline - last_step_deadline + 1
                    max_possible_reward = 2 * num_steps + 10
                    performance = total_reward / max_possible_reward
                    columns = \
                        [str(trial), succeeded_str, str(deadline), \
                         str(last_step_deadline), str(num_steps), \
                         str(total_reward), str(max_possible_reward), 
                         str(performance)]
                    output_line = ''
                    for column in columns:
                        output_line += column + ','
                    output_line += '\n'
                    output_file.write(output_line)
                    done = True
                    trial += 1
                else:
                    current_line_num += 1
    print "successes:", successes
    print "failures: ", failures
    output_file.close()
  
    
def get_int_from_line(name, line):
    val_str = get_num_str_from_line(name, line, "\d+")
    val = int(val_str)
    
    return val
  
    
def get_float_from_line(name, line):
    val_str = get_num_str_from_line(name, line, "\d+\.\d+")
    val = float(val_str)
    
    return val


def get_num_str_from_line(name, line, num_reg_ex):
    reg_ex = name + " = (" + num_reg_ex + ")"
    m = re.search(reg_ex, line)
    val_str = m.group(1)

    return val_str
        
        
if __name__ == '__main__':
    input_file_name = sys.argv[1]
    output_file_name = sys.argv[2]
    analyze_data(input_file_name, output_file_name)