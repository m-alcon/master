import argparse
from functools import reduce
import numpy as np
from pprint import pprint

def print_title(char,title,title_length=80):
    bar_size = int(np.ceil(float(title_length - len(title) - 2)/2))
    if bar_size < 1:
        print(title)
    else:
        bar = char*bar_size
        print('%s %s %s'%(bar,title,bar))

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
            total_class_items = sum(self.cond_freq[class_y].values())
            total_obs = len(self.global_freq.keys())-len(self.classes)
            for item_xi,freq_xi_y in self.cond_freq[class_y].items():
                if not item_xi in self.classes:
                    self.cond_probs[(item_xi,class_y)] = (freq_xi_y + 1)/(total_class_items + total_obs)

    def predict(self, observations, log2=True, verbose=False):
        mult = lambda x,y: x*y
        res_predictions = []
        for o in observations:
            predictions = {}
            for c in self.classes:
                if log2:
                    p = np.log2(self.global_probs[c])+sum([np.log2(self.cond_probs[(f,c)]) for f in o])
                else:
                    p = self.global_probs[c]*reduce(mult,[self.cond_probs[(f,c)] for f in o])
                predictions[c] = p
            if verbose:
                print('Probabilities for observation %s'%str(o))
                for k,v in predictions.items():
                    print('\tPr( %s ) = %0.5f'%(k,v))
            res_predictions.append(max(predictions, key=predictions.get))
        return res_predictions

    def print_probabilities(self):
        for (t,c),p in self.cond_probs.items():
            print('Pr( %s | %s ) = %0.5f'%(t,c,p))


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

    # Correctness experiment
    print_title('=','CORRECTNESS')
    data = read_file('data/toy.txt')
    mnb = MultinomialNB()
    mnb.fit(data)
    mnb.print_probabilities()
    print_title('-','Prediction probabilities')
    pred = mnb.predict([['a', 'a', 'f', 'a', 'e']], log2=False ,verbose=True)
    print('Class predicted: %s'%pred[0])


    # Behavior in realistic case experiment
    print_title('=','BEHAVIOR')
    data = read_file('data/markbask.txt')
    np.random.seed(10)
    np.random.shuffle(data)
    division = int(np.ceil(len(data)*0.8))
    train, test = data[:division], data[division:]
    print_title('*','Gender')
    ## Gender
    mnb = MultinomialNB()
    mnb.fit(train)
    mnb.print_probabilities()
    y = [t[0] for t in test]
    X = [t[1:] for t in test]
    print_title('-','Prediction probabilities (log2)')
    pred = mnb.predict(X, verbose=True)
    errors = 0
    for i in range(len(pred)):
        if pred[i] != y[i]:
            errors += 1
    print('Accuracy: %0.5f'%(1- errors/len(pred)))
    print_title('*','House owner')
    ## House owner or not
    mnb = MultinomialNB()
    mnb.fit(train,classes=['Homeowner','DoNotOwnHome'])
    mnb.print_probabilities()
    y = [t[1] for t in test]
    X = [[t[0]]+t[2:] for t in test]
    print_title('-','Prediction probabilities (log2)')
    pred = mnb.predict(X, verbose=True)
    errors = 0
    for i in range(len(pred)):
        if pred[i] != y[i]:
            errors += 1
    print('Accuracy: %0.5f'%(1- errors/len(pred)))


