import matplotlib.pyplot as plt
import argparse
from matplotlib import rcParams


rcParams['font.family'] = 'serif'
rcParams['font.size'] = 10
rcParams['font.sans-serif'] = ['Console Modern']
rcParams['savefig.format'] = ['pdf']
rcParams['savefig.bbox'] = 'tight'
rcParams['savefig.pad_inches'] = 0

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('path', help='Path of the data file.')
args = parser.parse_args()

data = []
with open(args.path, 'r') as file:
    for line in file.readlines():
        data.append(line.split())

name = args.path[8:args.path.find('_')]

x = []
y_kd = []
y_rkd = []
y_acc = []
for row in data:
    x.append(float(row[0]))
    y_acc.append(float(row[1])/100)
    y_kd.append(float(row[2])/1000)
    y_rkd.append(float(row[3])/1000)

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(x, y_kd, color='tab:blue')
ax.plot(x, y_rkd, color='coral')
if 'construct' in name:
    plt.xlabel('k')
    
else:
    plt.xlabel(name)
plt.ylabel('Time (s)')
plt.savefig('../plots/%s_times.pdf'%name)
ax.clear()

plt.plot(x,y_acc, color='coral')
plt.xlabel(name)
plt.ylabel('Accuracy')
plt.savefig('../plots/%s_acc.pdf'%name)


