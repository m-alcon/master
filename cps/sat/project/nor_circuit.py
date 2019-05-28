import numpy as np
import argparse

class Tree (object):

    def __init__ (self, depth):
        self.__now = 0
        self.__tree = [i+1 for i in range(pow(2,depth+1)-1)]
        self.depth = depth
    
    def __left_idx(self):
        return 2*self.__now + 1
    
    def __right_idx(self):
        return 2*self.__now + 2

    def actual_value(self):
        return self.__tree[self.__now]
    
    def go_root(self):
        self.__now = 0
        return self.actual_value()
    
    def go_left(self):
        now = self.__left_idx()
        if now < len(self.__tree):
            self.__now = now
        return self.actual_value()
    
    def go_right(self):
        now = self.__right_idx()
        if now < len(self.__tree):
            self.__now = now
        return self.actual_value()
    
    def go_parent(self):
        if self.__now % 2 and not self.__now:
            self.__now = int((self.__now - 2)/2)
        else:
            self.__now = int((self.__now - 1)/2)
        return self.actual_value()


#n = 0
#for line in sys.stdin:
#    if line.replace('\n','').isdigit():
#        n = int(line)
#        break
#    else:
#        print('Write N, an integer describing the size NxN of the board')

def generate_variables(n):
    variables = []
    actual_id = 1
    for i in range(n):
        variables.append([i+actual_id for i in range(n)])
        actual_id += n
    return variables

def at_most_one(variables):
    clauses = []
    for i in range(len(variables)-1):
        for j in range(i+1,len(variables)):
            clauses.append([-variables[i],-variables[j]])
    return clauses

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('N', help='Integer N representing the size of the board (NxN)')
    args = parser.parse_args()

    n = int(args.N)
    clauses = []
    variables = generate_variables(n)

    print('c Queens\' problem')
    print('p cnf %d %d'%(n*n,len(clauses)))
    for c in clauses:
        print('%s 0'%' '.join(map(str,c)))
