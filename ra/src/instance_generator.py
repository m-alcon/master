#!/usr/bin/python3
import numpy as np

separator = ','

def write_instances(instances_adhoc,instances):
    with open('../data/instances.dat','w') as file:
        for instance in instances:
            file.write(separator.join(instance) + '\n')
    with open('../data/instances_adhoc.dat','w') as file:
        for instance in instances_adhoc:
            file.write(separator.join(instance) + '\n')

def load_instances():
    instances_adhoc = []
    with open('../data/instances_adhoc.dat','r') as file:
        for line in file.readlines():
            instances_adhoc.append([int(x) for x in line.split(separator)])
    instances = []
    with open('../data/instances.dat','r') as file:
        for line in file.readlines():
            instances.append([int(x) for x in line.split(separator)])
    return instances_adhoc, instances

def generate_adhoc_instances(n,size,low,high):
    instances_asc = []
    instances_des = []
    for _ in range(int(n/2)):
        instance = list(np.sort(np.random.randint(low,high,size=size)))
        instances_asc.append([str(x) for x in instance])
        instance = list(np.sort(np.random.randint(low,high,size=size))[::-1])
        instances_des.append([str(x) for x in instance])
    return instances_asc + instances_des

def generate_random_instances(n,size,low,high):
    instances = []
    for i in range(n):
        instance = list(np.random.randint(low,high,size=size))
        instances.append([str(x) for x in instance])
    return instances

if __name__ == '__main__':
    n = 100
    size = 50000
    division = 0.3
    rand_range = (1000,1000000)
    instances_adhoc = generate_adhoc_instances(int(n*division),size,rand_range[0],rand_range[1])
    instances = generate_random_instances(int(n*(1-division)),size,rand_range[0],rand_range[1])
    write_instances(instances_adhoc,instances)

