import matplotlib.pyplot as plt
import argparse
from matplotlib import rcParams


rcParams['font.family'] = 'serif'
rcParams['font.size'] = 10
rcParams['font.sans-serif'] = ['Console Modern']
rcParams['savefig.format'] = ['pdf']
rcParams['savefig.bbox'] = 'tight'
rcParams['savefig.pad_inches'] = 0

names = {
    'bf': 'BF',
    'horspool': 'H',
    'bndm': 'BNDM',
    'bom': 'BOM'
}

colors = {
    'bf': 'royalblue',
    'horspool': 'mediumseagreen',
    'bndm': 'gold',
    'bom': 'coral'
}

data = []
with open('output.txt', 'r') as file:
    for line in file.readlines():
        data.append(line.split())

organizer = {}
for row in data:
    if row[0] in organizer:
        organizer[row[0]]['time'][row[3]] = row[1]
        organizer[row[0]]['count'][row[3]] = row[2]
    else:
        organizer[row[0]] = {
            'time': {},
            'count': {}
        }

min_times = {}
for k,v in organizer.items():
    n = [int(vk) for vk in v['time'].keys()]
    n.sort()
    times = [float(v['time'][str(i)]) for i in n]
    for i,t in zip(n,times):
        if i in min_times and min_times[i][1] > t:
            min_times[i] = [names[k],t]
        elif not i in min_times:
            min_times[i] = [names[k],t]
    plt.plot(n,times, color=colors[k], label=names[k])
plt.legend()
plt.ylabel('Running time (s)')
plt.xlabel('Length of the pattern')
plt.savefig('../plots/time.pdf')
plt.clf()


x = [min_times[i][0] for i in n]
plt.scatter(n,x, color='grey')
plt.ylabel('Algorithm with best time')
plt.xlabel('Length of the pattern')
plt.savefig('../plots/best.pdf')
plt.clf()

for k,v in organizer.items():
    n = [int(vk) for vk in v['count'].keys()]
    n.sort()
    counts = [int(v['count'][str(i)]) for i in n]
    plt.plot(n,counts, color=colors[k], label=names[k])
plt.legend()
plt.ylabel('Number of patterns found')
plt.xlabel('Length of the pattern')
plt.savefig('../plots/found.pdf')
plt.clf()