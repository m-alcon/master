import pandas as pd
import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn import tree
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
#from sklearn.feature_selection import RFE


header = ['age','sex','cp','trestbps','chol','fbs','restecg','thalach',
        'exang','oldpeak','slope','ca','thal','num']

need_preprocess = False

methods = {
    'NB':   GaussianNB(),
    'NN':   KNeighborsClassifier(n_neighbors=28),
    'DT':   tree.DecisionTreeClassifier(),
    'SVM':  SVC(kernel="linear", C=1)
}

def preprocess(data,save=False):
    count_erased_rows = 0
    for column in data:
        count_erased_rows += sum(data[column].apply(str) == '?')
        data = data[data[column].apply(str) != '?']
    print('%d rows which contain missing values erased.'%count_erased_rows)
    if save:
        data.to_csv('data/processed.csv',index=False)
    return data

def predict(method,X_train,y_train,X_test,y_test):
    y_pred = method.fit(X_train,y_train).predict(X_test)
    return accuracy_score(y_test,y_pred, normalize=True), y_pred

if __name__ == '__main__':

    data = pd.read_csv('./data/processed.csv')

    if need_preprocess:
        data = preprocess(data,True)

    X = data.drop(['num'], axis=1)
    y = data.num

    #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)


    #score,_ = predict(X_train,y_train,X_test,y_test)
    #print(score)


    method = methods['NN']
    scores = cross_val_score(method, X, y, cv=10)
    main_score = np.mean(scores)
    print('Without feature elimination: %0.5f'%main_score)

    X_aux = X.copy()
    features_to_eliminate = []
    for feature in list(X):
        #print('Drop %s feature.'%feature)
        X_aux = X.drop(feature, axis=1)
        scores = cross_val_score(method, X_aux, y, cv=10)
        score = np.mean(scores)
        print('Drop %s feature: %0.5f.'%(feature,score))
        if score > main_score:
            features_to_eliminate.append(feature)
    if not features_to_eliminate:
        print('Any feature to eliminate.')
    else:
        print('Features to eliminate: %s'%' '.join(features_to_eliminate))
        X = X.drop(features_to_eliminate, axis=1)
        # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

        # score,_ = predict(method,X_train,y_train,X_test,y_test)
        scores = cross_val_score(method, X, y, cv=10)
        score = np.mean(scores)
        print(score)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

    score,_ = predict(method,X_train,y_train,X_test,y_test)
    print('Final predictor accuracy: %0.5f'%score)



    # print('Number of mislabeled points out of a total %d points : %d'
    #     % (data.shape[0],(data[-1] != pred).sum()))
