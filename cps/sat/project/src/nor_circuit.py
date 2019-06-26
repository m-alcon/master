import numpy as np
import subprocess
import sys

class Tree (object):
    def __init__ (self, data):
        self.__data = data
    
    def __str__ (self):
        return str(self.__data)
    
    def __repr__ (self):
        return "Tree(%s)"%str(self)
    
    def __iter__ (self):
        for i in range(self.size()):
            yield self.__data[i]

    def __compute_idx (self, i, j):
        return np.power(2, i) - 1 + j

    def v (self, i, j):
        idx = self.__compute_idx(i, j)
        if idx >= self.size():
            print('Error on V(%d,%d): position %d'%(i,j,idx), file=sys.stder)
        return self.__data[idx]

    def l(self, i, j):
        idx = 2*self.__compute_idx(i, j) + 1
        if idx >= self.size():
            print('Error on L(%d,%d): position %d'%(i,j,idx), file=sys.stder)
        return self.__data[idx]

    def r(self, i, j):
        idx = 2*self.__compute_idx(i, j)+2
        if idx >= self.size():
            print('Error on R(%d,%d): position %d'%(i,j,idx), file=sys.stder)
        return self.__data[idx]
    
    def size (self):
        return len(self.__data)


class NORCirucuit(object):

    def __init__ (self, n, truth_table, depth, size):
        self.id = 1
        self.clauses = []
        self.n = n
        if type(truth_table) == list:
            self.tt = [int(x) for x in truth_table]
        else:
            self.tt = [int(x) for x in truth_table.split()]
        self.d = depth
        self.size = size
        self.circuit_size = np.power(2, depth + 1) - 1
        self.Z = self.generate_variables(self.circuit_size)
        self.N = self.generate_variables(self.circuit_size)
        self.I = self.generate_variables(self.circuit_size, n)
        self.B = self.generate_variables(self.circuit_size, np.power(2, n))
        self.solution = []
        self.generate_clauses()

    def __str__ (self):
        s = 'c NOR Circuit problem\np cnf %d %d'%(self.id, len(self.clauses))
        for c in self.clauses:
            s += '\n%s 0'%' '.join(map(str,c))
        return s

    @staticmethod
    def __bit(k, t):
        return (np.power(2, k) & t) != 0;

    def __give_id(self):
        new = int(self.id)
        self.id += 1
        return new
    
    def has_solution(self):
        return len(self.solution) > 0

    def generate_variables(self, n, m=0):
        if not m:
            return Tree([self.__give_id() for i in range(n)])
        
        variables = []
        for i in range(m):
            variables.append(Tree([self.__give_id() for j in range(n)]))
        return variables

    def add_clause(self, clause):
        self.clauses.append(frozenset(clause))

    def add_amo(self, variables): # quadratic encoding
        for i in range(len(variables)-1):
            for j in range(i+1,len(variables)):
                self.add_clause([-variables[i],-variables[j]])

    def add_amo_log(self, variables): # logarithmic encoding
        m = int(np.ceil(np.log2(len(variables))))
        new_vars = [self.__give_id() for i in range(m)]
        for i in range(len(variables)):
            for j in range(m):
                if self.__bit(j,i):
                    self.add_clause([-variables[i],new_vars[j]])
                else:
                    self.add_clause([-variables[i],-new_vars[j]])
    
    def __2comparator (self, x1, x2):
        y1, y2 = self.__give_id(), self.__give_id()
        self.add_clause([-x1, y1])
        self.add_clause([-x2, y1])
        self.add_clause([-x1, -x2, y2])
        return [y1, y2]
    
    def __merge(self, variables1, variables2):
        if len(variables1) == 1:
            return self.__2comparator(variables1[0], variables2[0])
        else:
            even1, even2, odd1, odd2 = [], [], [], []
            for i in range(len(variables1)):
                if i % 2 == 0:
                    even1.append(variables1[i])
                    even2.append(variables2[i])
                else:
                    odd1.append(variables1[i])
                    odd2.append(variables2[i])

            merged1 = self.__merge(even1, even2)
            merged2 = self.__merge(odd1, odd2)
            used_vars = [merged1[0]]
            for i in range(len(merged2)-1):
                used_vars += self.__2comparator(merged2[i], merged1[i+1])
            used_vars.append(merged2[-1])
            return used_vars

    def __sorting_network(self, variables):
        if len(variables) % 2 == 1:
            new = self.__give_id()
            self.add_clause([-new])
            variables.append(new)
        if len(variables) == 2:
            return self.__2comparator(variables[0], variables[1])
        else:
            half = int(len(variables)/2)
            variables1 = variables[:half]
            variables2 = variables[half:]
            sorted1 = self.__sorting_network(variables1)
            sorted2 = self.__sorting_network(variables2)
            return self.__merge(sorted1, sorted2)
            

    def add_amk(self, k, variables):
        sorted_vars = self.__sorting_network(variables)
        self.add_clause([-sorted_vars[k]])

    def generate_clauses(self):
        self.clauses = []

        # The output of the circuit is equal to the desired value for each row t of the truth table.
        for t in range(np.power(2,self.n)):
            if self.tt[t]:
                self.add_clause([self.B[t].v(0,0)])
            else:
                self.add_clause([-self.B[t].v(0,0)])
        
        # NOR gates are not allowed on the leaves of the circuit.
        for j in range(np.power(2, self.d)):
            self.add_clause([-self.N.v(self.d,j)])
        
        # Force children (if any) of each node to be 0 if the node is not a NOR gate.
        for i in range(self.d):
            for j in range(np.power(2, i)):
                self.add_clause([self.N.v(i,j), self.Z.l(i,j)])
                self.add_clause([self.N.v(i,j), self.Z.r(i,j)])

        # Force non-symmetry of NOR gates’ children. Do not allow the same input on both sides.
        # for k in range(self.n):
        #     for i in range(self.d):
        #         for j in range(np.power(2, i)):
        #             self.add_amo([self.I[k].l(i,j),self.I[k].r(i,j)])

        #Link each NOR gate with its corresponding value, which is the NOR operation between both children.
        for t in range(np.power(2,self.n)):
            for i in range(self.d):
                for j in range(np.power(2, i)):
                    self.add_clause([-self.N.v(i,j), -self.B[t].l(i,j), -self.B[t].v(i,j)])
                    self.add_clause([-self.N.v(i,j), -self.B[t].r(i,j), -self.B[t].v(i,j)])
                    self.add_clause([-self.N.v(i,j), self.B[t].l(i,j), self.B[t].r(i,j), self.B[t].v(i,j)])
        
        # Link each constant 0 signal with ‘false’.
        for t in range(np.power(2,self.n)):
            for i in range(self.d+1):
                for j in range(np.power(2, i)):
                    self.add_clause([-self.Z.v(i,j), -self.B[t].v(i,j)])
        
        # Link each input signal that has value 1 in the truth table, with ‘true’.
        for k in range(self.n):
            for t in range(np.power(2,self.n)):
                for i in range(self.d+1):
                    for j in range(np.power(2, self.d)):
                        if self.__bit(n-k-1, t):
                            self.add_clause([-self.I[k].v(i,j), self.B[t].v(i,j)])
                        else:
                            self.add_clause([-self.I[k].v(i,j), -self.B[t].v(i,j)])

        # Force each node to be only of one type.
        for i in range(self.d+1):
            for j in range(np.power(2, self.d)):
                variables = [self.Z.v(i,j), self.N.v(i,j)]
                for k in range(self.n):
                    variables.append(self.I[k].v(i,j))
                self.add_amo(variables)
                self.add_clause(variables)

        # Limit the number of NOR gates to be less than size.
        self.add_amk(self.size, list(self.N))

        self.clauses = frozenset(self.clauses)


    def solve(self):
        p = subprocess.run(['lingeling'], stdout=subprocess.PIPE, 
            input=str(self), encoding='ascii')
        output = p.stdout
        if 'UNSATISFIABLE' in output:
            return False
        
        start = output.find('v ') + 2
        end = output[start:].find(' 0') + 1 + start
        out_solution = output[start:end].replace('v', '')
        self.solution = []
        for line in out_solution.split('\n'):
            self.solution += [int(e) for e in line.split()]
        return True
    
    def __print_solution(self, i, j, curr_id, remaining_id):
        code = -2
        if self.solution[self.Z.v(i,j)-1] > 0:
            code = 0
        elif self.solution[self.N.v(i,j)-1] > 0:
            code = -1
        else:
            for k in range(len(self.I)):
                if self.solution[self.I[k].v(i,j)-1] > 0:
                    code = k+1
        print('%d %d '%(curr_id, code),end='')
        if code == -1:
            left_id = remaining_id+1
            right_id = remaining_id+2
            print('%d %d'%(left_id, right_id))
            remaining_id += 2
            remaining_id = self.__print_solution(i+1, 2*j, left_id, remaining_id)
            remaining_id = self.__print_solution(i+1, 2*j+1, right_id, remaining_id)
            return remaining_id
        else:
            print('0 0')
        return remaining_id
    
    def print_solution(self):
        print(self.n)
        for t in self.tt:
            print(t)
        print(self.d, self.size)
        if self.solution:
            self.__print_solution(0, 0, 1, 1)
        

if __name__ == '__main__':
    
    n, truth_table = int(input()), []
    for _ in range(np.power(2,n)):
        truth_table.append(int(input()))

    max_depth = 5
    for depth in range(max_depth+1):
        max_size = np.power(2, depth) - 1
        for size in range(depth, max_size+1):
            problem = NORCirucuit(n, truth_table, depth, size)
            if problem.solve():
                break
            print('UNSAT', depth, size, file=sys.stderr)
        if problem.has_solution():
            break
    if problem.has_solution():
        problem.print_solution()
    else:
        print('UNSAT', file=sys.stderr)


    
