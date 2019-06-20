import numpy as np
import time
import vptree

# Define distance function.
def euclidean(p1, p2):
    return np.sqrt(np.sum(np.power(p2 - p1, 2)))

# Generate some random points.
data = []
with open('data.txt', 'r') as file:
    data = np.array(eval(file.read()))

# Build tree in O(n log n) time complexity.
start = time.time()
tree = vptree.VPTree(data, euclidean)
py_const_time = time.time() - start

# Query single point.
py_results = []
py_times = []
with open('queries.txt', 'r') as file:
    for line in file.readlines():
        query = eval(line)
        start = time.time()
        py_results.append(tree.get_n_nearest_neighbors(query, 10000))
        py_times.append(time.time() - start)

cpp_results = []
with open('results.txt', 'r') as file:
    i = 0;
    for line in file.readlines():
        cpp_results.append(eval(line))

cpp_times = []
cpp_const_time = -1;
with open('times.txt', 'r') as file:
    cpp_times = eval(file.readline())
    cpp_const_time = cpp_times[0]
    cpp_times = cpp_times[1:]

py_points = [[list(e[1]) for e in r] for r in py_results]
cpp_points = [[list(e[1]) for e in r] for r in cpp_results]

py_dist = [[e[0] for e in r] for r in py_results]
cpp_dist = [[e[0] for e in r] for r in cpp_results]

correct = 0
almost_correct = 0
wrong = 0
dist_difference = []
lost_neig = []
for i in range(len(py_points)):
    # print(py)
    # print(cpp)
    if py_points[i] == cpp_points[i]:
        correct += 1
        dist_difference += list(np.array(py_dist[i]) - np.array(cpp_dist[i]))
    else:
        lost_neig.append(len(cpp_points[i]) - len(py_points[i]))
        if py_points[i] == cpp_points[i][:len(py_points[i])]:
            almost_correct += 1
            dist_difference += list(np.array(py_dist[i]) - np.array(cpp_dist[i][:len(py_points[i])]))
        else:
            wrong += 1

print('Correct: %0.5f'%float(correct/len(py_points)))
print('Almost correct: %0.5f'%float(almost_correct/len(py_points)))
print('Wrong: %0.5f'%float(wrong/len(py_points)))
print('Dist mean: %0.5f'%float(np.mean(dist_difference)))
print('Dist max: %0.5f'%float(np.max(dist_difference)))
print('Point lost mean: %0.5f'%float(np.sum(lost_neig)/len(py_points)))
print('Point lost max: %0.5f'%float(np.max(lost_neig)))
print('Point lost total: %0.5f'%float(np.sum(lost_neig)))
print('Py construct time: %0.5f'%float(py_const_time))
print('Py time mean: %0.5f'%float(np.mean(py_times)))
print('Py time max: %0.5f'%float(np.max(py_times)))
print('C++ construct time: %0.5f'%float(cpp_const_time/1000000))
print('C++ time mean: %0.5f'%float(np.mean(cpp_times)/1000000))
print('C++ time max: %0.5f'%float(np.max(cpp_times)/1000000))