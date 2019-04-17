import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix


header = ['age','sex','cp','trestbps','chol','fbs','restecg','thalach',
        'exang','oldpeak','slope','ca','thal','num']

need_preprocess = False
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

    data = pd.read_csv('./data/processed.csv')

    if need_preprocess:
        data = preprocess(data,True)
    
    colors = ['#ff0000','#00ff00']

    X = data.drop(['num'], axis=1)
    y = data.num

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

    binary_y, binary_y_train, binary_y_test = target_to_binary(y, y_train, y_test)
    labels = [colors[y_i] for y_i in binary_y]

    #fig, ax = plt.subplot()
    plt.scatter(X['age'],X['sex'],c=labels,s=50)
    plt.show()
