#!/usr/bin/python3
import time
import numpy as np
import matplotlib.pyplot as plt

import algorithms as alg
from instance_generator import load_instances

class Experiment(object):

    instances_adhoc, instances, instances_complexity = load_instances()

    def __init__(self):
        self.times = {
            'qselect':  [],
            'rmedian':  [],
            'rmedian_qselect':  [],
            'quicksort':[],
            'mergesort':[]
        }
        self.times_adhoc = {
            'qselect':  [],
            'rmedian':  [],
            'rmedian_qselect':  [],
            'quicksort':[],
            'mergesort':[]
        }
        self.times_complexity = {
            'qselect':  [],
            'rmedian':  [],
            'rmedian_qselect':  [],
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
            m5,t5 = self.run_without_idx(idx,instance,alg.rmedian_qselect)
            if m2 == False and not (m1 == m2 == m3 == m4 == m5):
                self.problems += 1
            self.times_adhoc['qselect'].append(t1)
            self.times_adhoc['rmedian'].append(t2)
            self.times_adhoc['quicksort'].append(t3)
            self.times_adhoc['mergesort'].append(t4)
            self.times_adhoc['rmedian_qselect'].append(t5)
        for instance in self.instances:
            idx = np.random.randint(len(instance))
            m1,t1 = self.run_with_idx(idx,instance,alg.qselect)
            m2,t2 = self.run_without_idx(idx,instance,alg.rmedian)
            m3,t3 = self.run_without_idx(idx,instance,alg.quick_sort)
            m4,t4 = self.run_without_idx(idx,instance,alg.merge_sort)
            m5,t5 = self.run_without_idx(idx,instance,alg.rmedian_qselect)
            if m2 == False and not (m1 == m2 == m3 == m4 == m5):
                self.problems += 1
            self.times['qselect'].append(t1)
            self.times['rmedian'].append(t2)
            self.times['quicksort'].append(t3)
            self.times['mergesort'].append(t4)
            self.times['rmedian_qselect'].append(t5)

    def print_results(self):
        adhoc_div = int(len(self.instances_adhoc)/2)
        asc_str,des_str = '',''
        for k,v in self.times_adhoc.items():
            asc_str += '%s: min=%0.8f max=%0.8f mean=%0.8f total=%0.8f\n'%(k,np.min(v[:adhoc_div]),np.max(v[:adhoc_div]),np.mean(v[:adhoc_div]),np.sum(v[:adhoc_div]))
            des_str += '%s: min=%0.8f max=%0.8f mean=%0.8f total=%0.8f\n'%(k,np.min(v[adhoc_div:]),np.max(v[adhoc_div:]),np.mean(v[adhoc_div:]),np.sum(v[adhoc_div:]))
        print('Ascending instances:')
        print(asc_str)
        print('Descending instances:')
        print(des_str)
        print('Random instances:')
        for k,v in self.times.items():
            print('%s: min=%0.8f max=%0.8f mean=%0.8f total=%0.8f'%(k,np.min(v),np.max(v),np.mean(v),np.sum(v)))
        print('problems:',self.problems)

    def print_results_latex(self):
        adhoc_div = int(len(self.instances_adhoc)/2)
        asc_str,des_str = '',''
        for k,v in self.times_adhoc.items():
            asc_str += '%s & %0.8f & %0.8f & %0.8f & %0.8f \\\\\n'%(k,np.min(v[:adhoc_div]),np.max(v[:adhoc_div]),np.mean(v[:adhoc_div]),np.sum(v[:adhoc_div]))
            des_str += '%s & %0.8f & %0.8f & %0.8f & %0.8f \\\\\n'%(k,np.min(v[adhoc_div:]),np.max(v[adhoc_div:]),np.mean(v[adhoc_div:]),np.sum(v[adhoc_div:]))
        print('\nAscending instances:')
        print(asc_str)
        print('Descending instances:')
        print(des_str)
        print('Random instances:')
        for k,v in self.times.items():
            print('%s & %0.8f & %0.8f & %0.8f & %0.8f \\\\'%(k,np.min(v),np.max(v),np.mean(v),np.sum(v)))

    def save_plots(self):
        fig, ax = plt.subplots()
        ax.plot(list(range(len(self.times_adhoc['quicksort']))), self.times_adhoc['quicksort'], color='green', marker='o', label='quicksort')
        ax.plot(list(range(len(self.times_adhoc['mergesort']))), self.times_adhoc['mergesort'], color='yellow', marker='o', label='mergesort')
        ax.plot(list(range(len(self.times_adhoc['qselect']))), self.times_adhoc['qselect'], color='blue', marker='o', label='qselect')
        ax.plot(list(range(len(self.times_adhoc['rmedian']))), self.times_adhoc['rmedian'], color='red', marker='o', label='rmedian')
        ax.plot(list(range(len(self.times_adhoc['rmedian_qselect']))), self.times_adhoc['rmedian_qselect'], color='orange', marker='o', label='rmedian_qselect')
        ax.set(ylabel='Time (s)', xlabel='Instance index')
        legend = ax.legend(loc='best', shadow=False, fontsize=10)
        fig.savefig('../img/experiment_adhoc.png')

        fig, ax = plt.subplots()
        ax.plot(list(range(len(self.times['quicksort']))), self.times['quicksort'], color='green', marker='o', label='quicksort')
        ax.plot(list(range(len(self.times['mergesort']))), self.times['mergesort'], color='yellow', marker='o', label='mergesort')
        ax.plot(list(range(len(self.times['qselect']))), self.times['qselect'], color='blue', marker='o', label='qselect')
        ax.plot(list(range(len(self.times['rmedian']))), self.times['rmedian'], color='red', marker='o', label='rmedian')
        ax.plot(list(range(len(self.times['rmedian_qselect']))), self.times['rmedian_qselect'], color='orange', marker='o', label='rmedian_qselect')
        ax.set(ylabel='Time (s)', xlabel='Instance index')
        legend = ax.legend(loc='best', shadow=False, fontsize=10)
        fig.savefig('../img/experiment_basic.png')

    def run_and_save_complexity(self):
        for instance in self.instances_complexity:
            idx = np.random.randint(len(instance))
            m1,t1 = self.run_with_idx(idx,instance,alg.qselect)
            m2,t2 = self.run_without_idx(idx,instance,alg.rmedian)
            m3,t3 = self.run_without_idx(idx,instance,alg.quick_sort)
            m4,t4 = self.run_without_idx(idx,instance,alg.merge_sort)
            m5,t5 = self.run_without_idx(idx,instance,alg.rmedian_qselect)
            if m2 == False and not (m1 == m2 == m3 == m4 == m5):
                self.problems += 1
            self.times_complexity['qselect'].append(t1)
            self.times_complexity['rmedian'].append(t2)
            self.times_complexity['quicksort'].append(t3)
            self.times_complexity['mergesort'].append(t4)
            self.times_complexity['rmedian_qselect'].append(t5)

        n_array = [(i+1)*1000for i in range(100)]
        fig, ax = plt.subplots()
        ax.plot(n_array, self.times_complexity['quicksort'], color='green', marker=',', label='quicksort')
        ax.plot(n_array, self.times_complexity['mergesort'], color='yellow', marker=',', label='mergesort')
        ax.plot(n_array, self.times_complexity['qselect'], color='blue', marker=',', label='qselect')
        ax.plot(n_array, self.times_complexity['rmedian'], color='red', marker=',', label='rmedian')
        ax.plot(n_array, self.times_complexity['rmedian_qselect'], color='orange', marker=',', label='rmedian_qselect')
        ax.set(ylabel='Time (s)', xlabel='n (size of array)')
        legend = ax.legend(loc='best', shadow=False, fontsize=10)
        fig.savefig('../img/experiment_complexity.png')


if __name__ == '__main__':
    experiment = Experiment()
    experiment.run()
    experiment.print_results()
    experiment.print_results_latex()
    experiment.save_plots()
    experiment.run_and_save_complexity()

