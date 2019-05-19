import argparse
from functools import reduce
import numpy as np
from pprint import pprint

class MultinomialNB(object):

    def __init__(self, alpha=0.5):
        self.global_freq = {}
        self.global_probs = {}
        self.cond_freq = {}
        self.cond_probs = {}
        self.alpha = alpha

    def fit(self, data):
        for obs in data:
            for item1 in obs:
                self.global_freq[item1] = self.global_freq.get(item1, 0) + 1
                self.cond_freq[item1] = self.cond_freq.get(item1, {})
                for item2 in obs:
                    if item1 != item2:
                        self.cond_freq[item1][item2] = self.cond_freq[item1].get(item2, 0) + 1

        total_obs = sum(self.global_freq.values())
        for class_y,v in self.cond_freq.items():
            self.global_probs[class_y] = self.global_freq[class_y]/total_obs
            #print('P(%s) = %0.5f'%(class_y,self.global_probs[class_y]))
            for item_xi,freq_xi_y in v.items():
                self.cond_probs[(item_xi,class_y)] = freq_xi_y/self.global_freq[class_y]


        # pprint(self.global_freq)
        # pprint(self.cond_freq)
        # pprint(self.cond_probs)

    def predict(self, classes, features):
        predictions = {}
        mult = lambda x,y: x*y
        for c in classes:
            p = reduce(mult,[self.cond_probs[(f,c)] for f in features])
            z = sum([self.global_probs[c]*self.cond_probs[(f,c)] for f in features])
            predictions[c] = (1/z)*self.global_probs[c]*p
            #print(sum([-np.log10(self.cond_probs[(c,f)]) for f in features]))
        pprint(predictions)

def read_file(path):
    data = []
    with open(path, 'r') as file:
        for line in file.readlines():
            data.append(line.split())
    return data

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='Path of the data file')
    args = parser.parse_args()

    data = read_file(args.path)

    mnb = MultinomialNB()
    mnb.fit(data)
    mnb.predict(['Male','Female'],['freshmeat', 'dairy', 'confectionery'])



