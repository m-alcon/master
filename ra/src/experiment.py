#!/usr/bin/python3
import numpy as np
import time

import algorithms as alg
from instance_generator import load_instances

class Experiment(object):

    instances_adhoc, instances = load_instances()

    def __init__(self):
        self.times = {
            'qselect':  [],
            'rmedian':  [],
            'quicksort':[],
            'mergesort':[]
        }
        self.times_adhoc = {
            'qselect':  [],
            'rmedian':  [],
            'quicksort':[],
            'mergesort':[]
        }
        self.problems = 0

    def run_without_idx(self,idx,instance,algorithm):
        start_time = time.process_time()
        res = algorithm(instance)
        if type(res) == list:
            res = res[idx]
        total_time = time.process_time() - start_time
        return res, total_time

    def run_with_idx(self,idx,instance,algorithm):
        idx = np.ceil(len(instance)/2 + 1)
        start_time = time.process_time()
        res = algorithm(idx,instance)
        total_time = time.process_time() - start_time
        return res, total_time

    def run(self):
        for instance in self.instances_adhoc:
            idx = np.random.randint(len(instance))
            m1,t1 = self.run_with_idx(idx,instance,alg.qselect)
            m2,t2 = self.run_without_idx(idx,instance,alg.rmedian)
            m3,t3 = self.run_without_idx(idx,instance,alg.quick_sort)
            m4,t4 = self.run_without_idx(idx,instance,alg.merge_sort)
            if m2 == False and not (m1 == m2 == m3 == m4):
                self.problems += 1
            self.times_adhoc['qselect'].append(t1)
            self.times_adhoc['rmedian'].append(t2)
            self.times_adhoc['quicksort'].append(t3)
            self.times_adhoc['mergesort'].append(t4)
        for instance in self.instances:
            idx = np.random.randint(len(instance))
            m1,t1 = self.run_with_idx(idx,instance,alg.qselect)
            m2,t2 = self.run_without_idx(idx,instance,alg.rmedian)
            m3,t3 = self.run_without_idx(idx,instance,alg.quick_sort)
            m4,t4 = self.run_without_idx(idx,instance,alg.merge_sort)
            if m2 == False and not (m1 == m2 == m3 == m4):
                self.problems += 1
            self.times['qselect'].append(t1)
            self.times['rmedian'].append(t2)
            self.times['quicksort'].append(t3)
            self.times['mergesort'].append(t4)

if __name__ == '__main__':
    experiment = Experiment()
    experiment.run()
    adhoc_div= int(len(experiment.instances_adhoc)/2)
    for k,v in experiment.times_adhoc.items():
        print('Ascending instances:')
        print('%s: min=%0.8f max=%0.8f mean=%0.8f'%(k,np.min(v[:adhoc_div]),np.max(v[:adhoc_div]),np.mean(v[:adhoc_div])))
        print('Descending instances:')
        print('%s: min=%0.8f max=%0.8f mean=%0.8f'%(k,np.min(v[adhoc_div:]),np.max(v[adhoc_div:]),np.mean(v[adhoc_div:])))
    print('Random instances:')
    for k,v in experiment.times.items():
        print('%s: min=%0.8f max=%0.8f mean=%0.8f'%(k,np.min(v),np.max(v),np.mean(v)))
    print('problems:',experiment.problems)

