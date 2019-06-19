import matplotlib.pyplot as plt

data = []
with open('../data/n_experiment.txt', 'r') as file:
    for line in file.readlines():
        data.append(line.split())

x = []
y_kd = []
y_rkd = []
y_acc = []
for row in data:
    x.append(float(row[0]))
    y_acc.append(float(row[1])/100)
    y_kd.append(float(row[2])/100000)
    y_rkd.append(float(row[3])/100000)

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(x, y_kd, color='tab:blue')
ax.plot(x, y_rkd, color='tab:orange')
plt.show()

plt.plot(x,y_acc)
plt.show()


