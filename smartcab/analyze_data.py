#!/usr/bin/python

'''
Created on Mar 3, 2016

@author: Paul Reiners
'''

import sys
import re
import matplotlib.pyplot as plt
import numpy as np
import pandas 

FLOAT_REG_EX = "[-+]?[0-9]*\.?[0-9]+"

def analyze_data(input_file_name, output_file_name):
    successes = 0
    failures = 0
    output_file = open(output_file_name,'w')
    columns = \
        ['trial', 'succeeded', 'deadline', 'last_step_deadline', 'num_steps', \
         'total_reward', 'max_possible_reward', 'performance', 'reward = -1', \
         'reward = 0.5', 'reward = 1', 'reward = 2']
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
        performance_over_time = []
        for trial_start_line in trial_start_lines:
            done = False
            current_line_num = trial_start_line
            current_line_num += 1
            line = lines[current_line_num]
            deadline = get_int_from_line('deadline', line)
            reward_counts = {"-1": 0, "0.5": 0, "1": 0, "2": 0}
            while not done:
                line = lines[current_line_num]
                succeeded = None
                if 'Primary agent could not reach destination within deadline!' in line:
                    succeeded = False
                    prev_line = lines[current_line_num - 1]
                    total_reward = get_float_from_line("total_reward", prev_line)
                elif 'Primary agent has reached destination!' in line:
                    prev_line = lines[current_line_num - 1]
                    if 'RoutePlanner.route_to()' in prev_line:
                        total_reward = 0
                        reward = "0"
                    else:
                        total_reward = get_float_from_line("total_reward", prev_line)
                    total_reward += 10
                    if total_reward >= 0.0:
                        succeeded = True
                    else:
                        succeeded = False
                elif 'LearningAgent.update()' in line:
                    reward = get_num_str_from_line("reward", line, FLOAT_REG_EX)
                    reward_counts[reward] = reward_counts[reward] + 1
                if not succeeded is None:
                    if succeeded:
                        successes += 1
                        succeeded_str = '1' 
                        prev_line = lines[current_line_num - 1]
                        if 'RoutePlanner.route_to()' in prev_line:
                            last_step_deadline = deadline
                        else:
                            last_step_deadline = get_int_from_line('deadline', prev_line)
                    else:
                        failures += 1
                        succeeded_str = '0' 
                        last_step_deadline = 0
                    num_steps = deadline - last_step_deadline + 1
                    max_possible_reward = 2 * num_steps + 10
                    performance = total_reward / max_possible_reward
                    performance_over_time.append(performance)
                    num_steps_f = float(num_steps)
                    columns = \
                        [str(trial), succeeded_str, str(deadline), \
                         str(last_step_deadline), str(num_steps), \
                         str(total_reward), str(max_possible_reward), 
                         str(performance), 
                         str(reward_counts["-1"] / num_steps_f), \
                         str(reward_counts["0.5"] / num_steps_f), \
                         str(reward_counts["1"] / num_steps_f), \
                         str(reward_counts["2"] / num_steps_f)]
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
    
    plt.plot(performance_over_time)
    plt.ylabel('performance')
    plt.show()
    
    data = pandas.read_csv(output_file_name)
    rewardMinusOne, = plt.plot(data['reward = -1'], label='reward = -1')
    rewardOneHalf, = plt.plot(data['reward = 0.5'], label='reward = 0.5')
    rewardOne, = plt.plot(data['reward = 1'], label='reward = 1')
    rewardTwo, = plt.plot(data['reward = 2'], label='reward = 2')
    plt.legend(handles=[rewardMinusOne, rewardOneHalf, rewardOne, rewardTwo])
    plt.title("Reward versus trial")
    plt.xlabel("trial")
    plt.ylabel("fraction of moves reward occurred")
    plt.show()

    
def get_int_from_line(name, line):
    val_str = get_num_str_from_line(name, line, "\d+")
    val = int(val_str)
    
    return val
  
    
def get_float_from_line(name, line):
    val_str = get_num_str_from_line(name, line, FLOAT_REG_EX)
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