import numpy as np
import argparse

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

def at_least_one(variables):
    return [frozenset(variables)]

def at_most_one(variables):
    clauses = []
    for i in range(len(variables)-1):
        for j in range(i+1,len(variables)):
            clauses.append(frozenset([-variables[i],-variables[j]]))
    return clauses


parser = argparse.ArgumentParser()
parser.add_argument('N', help='Integer N representing the size of the board (NxN)')
args = parser.parse_args()

n = int(args.N)
clauses = []
variables = generate_variables(n)

for row in variables:
    clauses += at_most_one(row)
    clauses += at_least_one(row)

t_variables = list(np.transpose(variables))
for col in t_variables:
    clauses += at_most_one(col)
    clauses += at_least_one(col)

# At most 1 queen per column right diagonal
for j in range(n):
    c = []
    for step in range(n-j):
        c.append(variables[step][j+step])
    clauses += at_most_one(c)

# At most 1 queen per row right diagonal
for i in range(n):
    c = []
    for step in range(n-i):
        c.append(variables[i+step][step])
    clauses += at_most_one(c)

# At most 1 queen per column left diagonal
for j in range(n):
    c = []
    for step in range(j+1):
        c.append(variables[step][j-step])
    clauses += at_most_one(c)

# At most 1 queen per row l eft diagonal
for i in range(n):
    c = []
    for step in range(n-i):
        c.append(variables[i+step][n-1-step])
    clauses += at_most_one(c)

print('c Queens\' problem')
clauses = frozenset(clauses)
print('p cnf %d %d'%(n*n,len(clauses)))
for c in clauses:
    print('%s 0'%' '.join(map(str,c)))
