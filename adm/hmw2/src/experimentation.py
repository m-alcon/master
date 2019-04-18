import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture
from sklearn.datasets.samples_generator import make_blobs
from sklearn.model_selection import train_test_split
from sklearn import metrics
import matplotlib.colors as colors
import matplotlib.cm as cmx
from matplotlib import rcParams
import colorsys

rcParams['font.family'] = 'serif'
rcParams['font.size'] = 10
rcParams['font.sans-serif'] = ['Console Modern']
rcParams['savefig.format'] = ['pdf']
rcParams['savefig.bbox'] = 'tight'
rcParams['savefig.pad_inches'] = 0


header = ['age','sex','cp','trestbps','chol','fbs','restecg','thalach',
        'exang','oldpeak','slope','ca','thal','num']

title_length = 70

def print_title(char,title):
    bar_size = int(np.ceil(float(title_length - len(title) - 2)/2))
    if bar_size < 1:
        print(title)
    else:
        bar = char*bar_size
        print('%s %s %s'%(bar,title,bar))

def generate_centers(n):
    div = np.floor(np.sqrt(n))
    x = int(np.floor(n/div) + n%div)
    y = int(np.floor(n/div))
    print(x,y)
    centers = []
    for j in range(y):
        for i in range(x):
            centers.append([i*2,j*2])
    return centers


def map_labels(truth, pred):
    mapping = np.zeros((max(pred)+1,max(truth)+1))
    for t,p in zip(truth,pred):
        mapping[p][t] += 1
    return [np.argmax(m) for m in mapping]



if __name__ == '__main__':
    #n_centers = 8
    #centers = [[n_centers*x,n_centers*y] for x,y in np.random.rand(n_centers,2)]
    #centers = np.random.uniform(0,n_centers+4, (n_centers, 2))
    #print(centers)

    # Centers of the clusters to generate
    centers = generate_centers(16)
    n_centers = 16

    # Methods to compare
    methods = {
        'EM': GaussianMixture(n_components=n_centers, covariance_type='full')
    }

    # Generation of data
    data, truth_labels = make_blobs(n_samples=1000, centers=centers, cluster_std=0.4,
                            random_state=55)
    x = [d[0] for d in data]
    y = [d[1] for d in data]

    # Automatic cluster coloring
    cNorm  = colors.Normalize(vmin=0, vmax=n_centers)
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap='gist_rainbow')
    truth_colors = [scalarMap.to_rgba(l) for l in truth_labels]

    # Clustering
    methods['EM'].fit(data, y=truth_labels)
    pred_labels = methods['EM'].predict(data)
    pred_colors = [scalarMap.to_rgba(l) for l in pred_labels]

    # Map truth labels with predicted labels
    label_map = map_labels(truth_labels,pred_labels)
    mapped_labels = [label_map[l] for l in pred_labels]

    # Prepare colors for the plot
    mixed_colors = []
    for t,p in zip(truth_labels,mapped_labels):
        if t == p:
            mixed_colors.append(scalarMap.to_rgba(t))
        else:
            mixed_colors.append('#000000') # Color of a bad prediction
    
    # Print score
    print('Score:', metrics.adjusted_rand_score(truth_labels, pred_labels))
    
    # Generate and save plots
    plt.scatter(x,y,c=truth_colors)
    plt.savefig('./plots/truth.pdf')
    plt.scatter(x,y,c=pred_colors)
    plt.savefig('./plots/pred.pdf')
    plt.scatter(x,y,c=mixed_colors)
    plt.savefig('./plots/mixed.pdf')
