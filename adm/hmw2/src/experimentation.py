import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture
from sklearn.cluster import DBSCAN
from sklearn.cluster import Birch
from sklearn.datasets import samples_generator as sg
from sklearn.model_selection import train_test_split
from sklearn import metrics
import matplotlib.colors as colors
import matplotlib.cm as cmx
from matplotlib import rcParams
import colorsys
from pprint import pprint

rcParams['font.family'] = 'serif'
rcParams['font.size'] = 10
rcParams['font.sans-serif'] = ['Console Modern']
rcParams['savefig.format'] = ['pdf']
rcParams['savefig.bbox'] = 'tight'
rcParams['savefig.pad_inches'] = 0

color_map = 'plasma'

def print_title(char,title,title_length=30):
    bar_size = int(np.ceil(float(title_length - len(title) - 2)/2))
    if bar_size < 1:
        print(title)
    else:
        bar = char*bar_size
        print('%s %s %s'%(bar,title,bar))

def generate_centers(n, separation):
    row_size = int(np.round(np.sqrt(n)))
    centers = []
    placed = 0
    while placed < n:
        if placed+row_size <= n:
            for i in range(row_size):
                centers.append((i*separation,-(placed/row_size)*separation))
        else:
            distance = (row_size-1)/float(n-placed+1)
            x_centers = [(i+1)*distance for i in range(n-placed)]
            for x in x_centers:
                centers.append((x*separation,-(placed/row_size)*separation))
        placed += row_size
    return centers

def map_labels(truth, pred):
    mapping = {}
    for t,p in zip(truth,pred):
        if not p in mapping:
            mapping[p] = np.zeros(max(truth)+1)
        mapping[p][t] += 1
    keys = list(mapping.keys())
    keys.sort()
    return {k:np.argmax(mapping[k]) for k in keys}

def clear_plt():
    plt.clf()
    plt.cla()
    plt.close()

if __name__ == '__main__':

    make_experiment = [True,False,False]
    n_samples = 2000
    default_sep = 2

    # FIRST EXPERIMENT
    if make_experiment[0]:
        print_title('=','FIRST EXPERIMENT')
        #Centers of the clusters to generate
        experiments = [(4,4,default_sep),(7,3,default_sep), (30,30,default_sep),(30,30,6)]
        for real_centers,n_centers,separation in experiments:
            props = '%s-%s'%(n_centers,real_centers)
            if separation != default_sep:
                props += '-%s'%separation
            print_title('+',props)
            centers = generate_centers(real_centers, separation)

            # Methods to compare
            methods = {
                'em': GaussianMixture(n_components=n_centers),
                'dbscan': DBSCAN(eps=0.2, min_samples=5),
                #'birch': Birch(branching_factor=50, n_clusters=n_centers, threshold=0.5, compute_labels=True)
            }

            # Generation of data
            data, truth_labels = sg.make_blobs(n_samples=n_samples, centers=centers, cluster_std=0.4,
                                    random_state=25)
            x = [d[0] for d in data]
            y = [d[1] for d in data]

            # Automatic cluster coloring
            cNorm  = colors.Normalize(vmin=0, vmax=real_centers-1)
            scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=color_map)
            truth_colors = [scalarMap.to_rgba(l) for l in truth_labels]

            plt.scatter(x,y,c=truth_colors)
            plt.savefig('./plots/truth_%s.pdf'%(props))
            clear_plt()

            # Clustering
            for method_name in methods.keys():
                print_title('-',method_name)
                pred_labels = methods[method_name].fit_predict(data)
                pred_colors = []

                # Colors for predicted labels
                n_labels = len((set(pred_labels)))
                if n_labels > 1:
                    n_labels -= 1
                cNorm  = colors.Normalize(vmin=0, vmax=n_labels)
                scalarMap_pred = cmx.ScalarMappable(norm=cNorm, cmap=color_map)

                for l in pred_labels:
                    color = scalarMap_pred.to_rgba(l)
                    if l == -1:
                        color = '#AAAAAA'
                    pred_colors.append(color)

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

                # Generate and save plots
                plt.scatter(x,y,c=pred_colors)
                plt.savefig('./plots/%s_pred_%s.pdf'%(props,method_name))
                clear_plt()
                if real_centers == n_centers:
                    plt.scatter(x,y,c=mixed_colors)
                    plt.savefig('./plots/%s_mixed_%s.pdf'%(props,method_name))
                    clear_plt()
                # Print score
                    print('Score:', metrics.adjusted_rand_score(truth_labels, pred_labels))
                else:
                    print('Score: not meaningful')

    # SECOND EXPERIMENT
    if make_experiment[1]:
        print_title('=','SECOND EXPERIMENT')
        methods = {
            'em': GaussianMixture(n_components=2, covariance_type='full'),
            'dbscan': DBSCAN(eps=0.2, min_samples=10),
            #'birch': Birch(branching_factor=50, n_clusters=2, threshold=0.5, compute_labels=True)
        }

        ## Automatic cluster coloring
        cNorm  = colors.Normalize(vmin=0, vmax=1)
        scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=color_map)

        for method_name, m in methods.items():
            print_title('+','%s'%method_name)
            x,y = sg.make_circles(n_samples=n_samples, factor=.5, noise=.05)
            pred_labels = m.fit_predict(x)
            colors = [scalarMap.to_rgba(l) for l in pred_labels]
            plt.scatter(x[:,0],x[:,1], c=colors)
            plt.savefig('./plots/circle_%s.pdf'%method_name)
            clear_plt()

            x,y = sg.make_moons(n_samples=n_samples, noise=.05)
            pred_labels = m.fit_predict(x)
            colors = [scalarMap.to_rgba(l) for l in pred_labels]
            plt.scatter(x[:,0],x[:,1], c=colors)
            plt.savefig('./plots/moons_%s.pdf'%method_name)
            clear_plt()

    # THIRD EXPERIMENT
    #header = ['age','sex','cp','trestbps','chol','fbs','restecg','thalach',
    #    'exang','oldpeak','slope','ca','thal','num']
    if make_experiment[2]:
        print_title('=','THIRD EXPERIMENT')
        data = pd.read_csv('./data/processed.csv')
        x = data.drop(['num'], axis=1)
        experiments = {
            'binary': (2,data.num.apply(lambda x: int(x != 0))),
            'normal': (4,data.num)
        }
        for e in experiments.keys():
            n_clusters, truth_labels = experiments[e]
            print_title('+','%s'%e)
            methods = {
                'em': GaussianMixture(n_components=n_clusters, covariance_type='full'),
                'dbscan': DBSCAN(eps=0.1, min_samples=10),
                'birch': Birch(branching_factor=50, n_clusters=n_clusters, threshold=0.5, compute_labels=True)
            }
            for method_name,m in methods.items():
                print_title('-','%s'%method_name)
                summary = {}
                pred_labels = m.fit_predict(x)
                for p,t in zip(pred_labels,truth_labels):
                    if not p in summary:
                        summary[p] = np.zeros(max(truth_labels)+1)
                    summary[p][t] += 1
                pprint(summary)
                print('Score:', metrics.adjusted_rand_score(truth_labels, pred_labels))
                