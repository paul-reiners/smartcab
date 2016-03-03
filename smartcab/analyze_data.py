#!/usr/bin/python

'''
Created on Mar 3, 2016

@author: Paul Reiners
'''

import sys

def analyze_data(file_name):
    successes = 0
    failures = 0
    succeeded = []
    with open(file_name) as f:
        lines = f.readlines()
        for i in range(0, len(lines)):
            line = lines[i]
            if 'Primary agent could not reach destination within deadline!' in line:
                failures += 1
                succeeded.append(False)
            elif 'Primary agent has reached destination!' in line:
                next_line = lines[i + 1]
                parts = next_line.split();
                reward = float(parts[len(parts) - 1])
                if reward >= 0.0:
                    successes += 1
                    succeeded.append(True)
                else:
                    failures += 1
                    succeeded.append(False)
    print "successes:", successes
    print "failures: ", failures
    num_successes_at_end = 0
    for result in reversed(succeeded):
        if result:
            num_successes_at_end += 1
        else:
            break
    print "consecutive final successes", num_successes_at_end 
        
if __name__ == '__main__':
    file_name = sys.argv[1]
    analyze_data(file_name)