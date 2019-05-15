import argparse
import numpy as np
from pprint import pprint

class MultinomialNB(object):

    def __init__(self):
        self.total_freq = {}
        self.conditional_freq = {}
        self.probs = {}
    
    def fit(self, data):
        for obs in data:
            for item1 in obs:
                self.total_freq[item1] = self.total_freq.get(item1, 0) + 1
                self.conditional_freq[item1] = self.conditional_freq.get(item1, {})
                for item2 in obs:
                    if item1 != item2:
                        self.conditional_freq[item1][item2] = self.conditional_freq[item1].get(item2, 0) + 1

        for class_y,v in self.conditional_freq.items():
            for item_xi,freq_xi_y in v.items():
                self.probs[(item_xi,class_y)] = freq_xi_y/self.total_freq[class_y] 
             

        pprint(self.total_freq)
        pprint(self.conditional_freq)
        pprint(self.probs)

        
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



