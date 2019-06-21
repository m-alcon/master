import matplotlib.pyplot as plt
import argparse
from matplotlib import rcParams


rcParams['font.family'] = 'serif'
rcParams['font.size'] = 10
rcParams['font.sans-serif'] = ['Console Modern']
rcParams['savefig.format'] = ['pdf']
rcParams['savefig.bbox'] = 'tight'
rcParams['savefig.pad_inches'] = 0

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

for k,v in organizer.items():
    n = [int(vk) for vk in v['time'].keys()]
    n.sort()
    times = [float(v['time'][str(i)]) for i in n]
    print(n)
    print(times)
    plt.plot(n,times, color=colors[k], label=k)

plt.legend()
plt.show()

# ax.plot(, v[0]['time'], color='tab:blue')
# plt.savefig('../plots/%s_times.pdf'%name)
# ax.clear()

# plt.plot(x,y_acc, color='coral')
# plt.savefig('../plots/%s_acc.pdf'%name)