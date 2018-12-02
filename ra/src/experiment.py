#!/usr/bin/python3
import numpy as np
import time

import algorithms as alg
from instance_generator import load_instances

class Experiment(object):

    instances = load_instances()

    def __init__(self):
        self.times = {
            'qselect':  [],
            'rmedian':  [],
            'quicksort':[],
            'mergesort':[]
        }

    def run_sort(self,instance,algorithm):
        start_time = time.process_time()
        algorithm(instance)
        total_time = time.process_time() - start_time
        return total_time
    
    def run_select(self,k,instance,algorithm):
        start_time = time.process_time()
        algorithm(k,instance)
        total_time = time.process_time() - start_time
        return total_time

    def run(self):
        for instance in self.instances:
            k = np.random.randint(len(instance))
            self.times['qselect'].append(self.run_select(k,instance,alg.qselect))
            self.times['rmedian'].append(self.run_select(k,instance,alg.rmedian))
            self.times['quicksort'].append(self.run_sort(instance,alg.quick_sort))
            self.times['mergesort'].append(self.run_sort(instance,alg.merge_sort))

if __name__ == '__main__':
    experiment = Experiment()
    experiment.run()
    print(experiment.times)

