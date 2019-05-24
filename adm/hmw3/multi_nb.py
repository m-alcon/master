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

    def fit(self, data, classes=[]):
        self.classes = list(classes)

        for obs in data:
            if not classes and not obs[0] in self.classes:
                self.classes.append(obs[0])
            for item1 in obs:
                self.global_freq[item1] = self.global_freq.get(item1, 0) + 1
                self.cond_freq[item1] = self.cond_freq.get(item1, {})
                for item2 in obs:
                    if item1 != item2:
                        self.cond_freq[item1][item2] = self.cond_freq[item1].get(item2, 0) + 1
        for item1 in self.global_freq:
            for item2 in self.global_freq:
                if item1 != item2 and not item2 in self.cond_freq[item1]:
                    self.cond_freq[item1][item2] = 0

        for class_y in self.classes:
            self.global_probs[class_y] = self.global_freq[class_y]/len(data)
            print("Pr(%s) = %d/%d"%(class_y,self.global_freq[class_y],len(data)))
            #print('P(%s) = %0.5f'%(class_y,self.global_probs[class_y]))
            total_class_items = sum(self.cond_freq[class_y].values())
            total_obs = len(self.global_freq.keys())-len(self.classes)
            for item_xi,freq_xi_y in self.cond_freq[class_y].items():
                if not item_xi in self.classes:
                    self.cond_probs[(item_xi,class_y)] = (freq_xi_y + 1)/(total_class_items + total_obs)
                    print("Pr(%s|%s) = (%d + %d)/(%d + %d)"%(item_xi,class_y,freq_xi_y,1,total_class_items,total_obs))

        pprint(self.global_freq)
        pprint(self.cond_freq)
        pprint(self.cond_probs)

    def predict(self, features):
        predictions = {}
        mult = lambda x,y: x*y
        for c in self.classes:
            p = reduce(mult,[self.cond_probs[(f,c)] for f in features])
            print(sum([-np.log2(self.cond_probs[(f,c)]) for f in features]))
            predictions[c] = p-np.log2(self.global_probs[c])
            
        pprint(predictions)

    def fit_and_predict(self, data, features, classes=[]):
        self.fit(data,classes)
        self.predict(features)

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
    #mnb.predict(['a', 'a', 'f', 'a', 'e'])
    mnb.predict(['freshmeat', 'dairy', 'confectionery'])



