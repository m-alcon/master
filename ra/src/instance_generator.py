#!/usr/bin/python3
import numpy as np

separator = ','

def write_instances(instances):
    with open('../data/instances.dat','w') as file:
        for instance in instances:
            file.write(separator.join(instance) + '\n')

def load_instances():
    instances = []
    with open('../data/instances.dat','r') as file:
        for line in file.readlines():
            instances.append([int(x) for x in line.split(separator)])
    return instances

def generate_adhoc_instances():
    return []

def generate_random_instances(n,size,low,high):
    instances = []
    for i in range(n):
        instance = list(np.random.randint(low,high,size=size))
        instances.append([str(x) for x in instance])
    return instances

if __name__ == '__main__':
    n = 100
    size = 50000
    rand_range = (1000,1000000)
    instances = generate_adhoc_instances()
    instances += generate_random_instances(n,size,rand_range[0],rand_range[1]) 
    write_instances(instances)
    

