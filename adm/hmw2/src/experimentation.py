import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture
from sklearn.cluster import DBSCAN
from sklearn.cluster import Birch
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

def print_title(char,title,title_length=30):
    bar_size = int(np.ceil(float(title_length - len(title) - 2)/2))
    if bar_size < 1:
        print(title)
    else:
        bar = char*bar_size
        print('%s %s %s'%(bar,title,bar))

def generate_centers(n):
    row_size = int(np.round(np.sqrt(n)))
    centers = []
    placed = 0
    while placed < n:
        if placed+row_size <= n:
            for i in range(row_size):
                centers.append((i*2,-placed*2))
        else:
            distance = row_size/(n-placed)
            for i in np.arange(distance,int(n-placed)+distance,distance):
                centers.append((i*2,-placed*2))
        placed += row_size
    return centers


def map_labels(truth, pred):
    mapping = np.zeros((max(pred)+1,max(truth)+1))
    for t,p in zip(truth,pred):
        mapping[p][t] += 1
    return [np.argmax(m) for m in mapping]

def clear_plt():
    plt.clf()
    plt.cla()
    plt.close()



if __name__ == '__main__':
    #n_centers = 8
    #centers = [[n_centers*x,n_centers*y] for x,y in np.random.rand(n_centers,2)]
    #centers = np.random.uniform(0,n_centers+4, (n_centers, 2))
    #print(centers)

    # Centers of the clusters to generate
    experiments = [(4,4),(1,4),(8,8),(8,4),(32,2),(32,32)]
    for real_centers, n_centers in experiments:
        print_title('=','%d-%d'%(real_centers,n_centers))
        n_samples = 2000
        centers = generate_centers(real_centers)

        # Methods to compare
        methods = {
            'em': GaussianMixture(n_components=n_centers, covariance_type='full'),
            #'DB': DBSCAN(eps=0.3, min_samples=10),
            'birch': Birch(branching_factor=50, n_clusters=n_centers, threshold=0.5, compute_labels=True)
        }

        # Generation of data
        data, truth_labels = make_blobs(n_samples=n_samples, centers=centers, cluster_std=0.4,
                                random_state=55)
        x = [d[0] for d in data]
        y = [d[1] for d in data]

        # Automatic cluster coloring
        cNorm  = colors.Normalize(vmin=0, vmax=real_centers)
        scalarMap = cmx.ScalarMappable(norm=cNorm, cmap='gist_rainbow')
        truth_colors = [scalarMap.to_rgba(l) for l in truth_labels]
        
        cNorm  = colors.Normalize(vmin=0, vmax=n_centers)
        scalarMap_pred = cmx.ScalarMappable(norm=cNorm, cmap='gist_rainbow')
        

        plt.scatter(x,y,c=truth_colors)
        plt.savefig('./plots/truth_%d-%d.pdf'%(real_centers,n_centers))
        clear_plt()

        # Clustering
        for method_name in methods.keys():
            print_title('-',method_name)
            methods[method_name].fit(data)
            pred_labels = methods[method_name].predict(data)
            pred_colors = [scalarMap_pred.to_rgba(l) for l in pred_labels]

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
            plt.scatter(x,y,c=pred_colors)
            plt.savefig('./plots/%d-%d_pred_%s.pdf'%(real_centers,n_centers,method_name))
            clear_plt()
            if real_centers == n_centers:
                plt.scatter(x,y,c=mixed_colors)
                plt.savefig('./plots/%d-%d_mixed_%s.pdf'%(real_centers,n_centers,method_name))
                clear_plt()
