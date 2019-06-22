import numpy as np
import argparse

class Tree (object):
    def __init__ (self, data):
        self.__data = data
    
    def __str__ (self):
        return str(self.__data)

    def __compute_idx (self, i, j):
        return np.power(2, i) - 1 + j

    def v (self, i, j):
        return self.__data[self.__compute_idx(i, j)]

    def l(self, i, j):
        return self.__data[2*self.__compute_idx(i, j) + 1]

    def r(self, i, j):
        return self.__data[2*self.__compute_idx(i, j) + 2]


class NORCirucuit(object):

    def __init__ (self, n, truth_table, depth, size):
        self.id = 0
        self.clauses = []
        self.n = n
        self.tt = truth_table
        self.d = depth
        self.size = size
        self.circuit_size = np.power(2, n + 1) - 1
        self.Z = self.generate_variables(self.circuit_size)
        self.N = self.generate_variables(self.circuit_size)
        self.I = self.generate_variables(self.circuit_size, n)
        self.B = self.generate_variables(self.circuit_size, np.power(2, n))
        self.generate_clauses()
    
    @staticmethod
    def bit(k, t):
        return (np.power(2, k) & t) != 0;

    def give_id(self):
        new = int(self.id)
        self.id += 1
        return new

    def generate_variables(self, n, m=0):
        if not m:
            return [self.give_id() for i in range(n)]
        
        variables = []
        for i in range(m):
            variables.append(Tree([self.give_id() for j in range(n)]))
        return variables

    def add_clause(self, clause):
        self.clauses.append(clause)

    def add_amo(self, variables):
        for i in range(len(variables)-1):
            for j in range(i+1,len(variables)):
                self.add_clause([-variables[i],-variables[j]])

    def generate_clauses(self):
        # The output of the circuit is equal to the desired value for each row t of the truth table.
        for t in range(len(self.tt)):
            if self.tt[t]:
                self.add_clause([self.B[t].v(0,0)])
            else:
                self.add_clause([-self.B[t].v(0,0)])
        
        # NOR gates are not allowed on the leaves of the circuit.
        for j in range(np.power(2, self.d)):
            self.add_clause([-self.N.v(self.d,j)])
        
        # Force children (if any) of each node to be 0 if the node is not a NOR gate.
        # Force non-symmetry of NOR gates’ children. Do not allow the same input on both sides.
        for k in range(n):
            for i in range(self.d):
                for j in range(np.pow(2, self.d)):
                    self.add_amo([self.I[k].l(i,j),self.I[k].r(i,j)])

        #Link each NOR gate with its corresponding value, which is the NOR operation between both children.
        for t in range(np.power(2,n)):
            for i in range(self.d):
                for j in range(np.pow(2, self.d)):
                    self.add_amo([self.B[t].v(i,j)])
                    #TODO
        
        #Link each constant 0 signal with ‘false’.
        for t in range(np.power(2,n)):
            for i in range(self.d):
                for j in range(np.pow(2, self.d)):
                    self.add_clause([-self.Z.v(i,j), self.B[t].v(i,k)])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('N', type=int, help='Integer N representing the size of the board (NxN)')
    parser.add_argument('-d', '--depth', type=int, help='Depth')
    parser.add_argument('-s', '--size', type=int, help='Max size')
    parser.add_argument('-t', '--tt', type=str, help='Truth table')
    args = parser.parse_args()

    problem = NORCirucuit(args.N, args.tt.split(), args.depth, args.size)
    print('Z',problem.Z)
    print('N',problem.N)
    print('I',problem.I)
    print('B',problem.B)


    
