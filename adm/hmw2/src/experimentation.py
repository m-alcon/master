import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets.samples_generator import make_blobs
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix
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

methods = {
}

def print_title(char,title):
    bar_size = int(np.ceil(float(title_length - len(title) - 2)/2))
    if bar_size < 1:
        print(title)
    else:
        bar = char*bar_size
        print('%s %s %s'%(bar,title,bar))

def preprocess(data,save=False):
    count_erased_rows = 0
    for column in data:
        count_erased_rows += sum(data[column].apply(str) == '?')
        data = data[data[column].apply(str) != '?']
    print('%d rows which contain missing values erased.'%count_erased_rows)
    if save:
        data.to_csv('data/processed.csv',index=False)
    return data


def target_to_binary(y, y_train, y_test):
    binary_y = y.copy()
    binary_y_train = y_train.copy()
    binary_y_test = y_test.copy()

    binary_y = y.apply(lambda x: int(x > 0))
    binary_y_train = y_train.apply(lambda x: int(x > 0))
    binary_y_test = y_test.apply(lambda x: int(x > 0))
    return binary_y, binary_y_train, binary_y_test



if __name__ == '__main__':

    centers = [[1, 1], [-1, -1], [-1, 1], [1, -1]]
    #n_centers = 8
    #centers = [[n_centers*x,n_centers*y] for x,y in np.random.rand(n_centers,2)]
    #centers = np.random.uniform(0,n_centers+4, (n_centers, 2))
    #print(centers)

    cNorm  = colors.Normalize(vmin=0, vmax=len(centers))
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap='gist_rainbow')

    data, truth_labels = make_blobs(n_samples=300, centers=centers, cluster_std=0.4,
                            random_state=73)

    colors = [scalarMap.to_rgba(l) for l in truth_labels]

    x = [d[0] for d in data]
    y = [d[1] for d in data]

    #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

    #fig, ax = plt.subplot()
    plt.scatter(x,y,c=colors)
    plt.show()
