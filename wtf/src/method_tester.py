import pandas as pd
import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn import tree
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix
#from sklearn.feature_selection import RFE


header = ['age','sex','cp','trestbps','chol','fbs','restecg','thalach',
        'exang','oldpeak','slope','ca','thal','num']

need_preprocess = False

methods = {
    'NB':   GaussianNB(),
    'NN':   KNeighborsClassifier(n_neighbors=28),
    'DT':   tree.DecisionTreeClassifier(),
    'SVM':  SVC(kernel="poly", C=10, gamma='auto')
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

def predict_with_model(model,X_test,y_test):
    y_pred = model.predict(X_test)
    return accuracy_score(y_test,y_pred, normalize=True), y_pred

def perform_experiment(method_name,X,y):
    method = methods[method_name]
    print('================== %s =================='%method_name)
    scores = cross_val_score(method, X, y, cv=10)
    main_score = np.mean(scores)
    print('Cross validation without feature elimination: %0.5f'%main_score)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
    score,_ = predict(method,X_train,y_train,X_test,y_test)
    print('Train-test without feature elimination: %0.5f'%score)


    X_aux = X.copy()
    features_to_eliminate = []
    print('Dropping features:')
    for feature in list(X):
        #print('Drop %s feature.'%feature)
        X_aux = X.drop(feature, axis=1)
        scores = cross_val_score(method, X_aux, y, cv=10)
        score = np.mean(scores)
        print('  - Drop %s feature: %0.5f.'%(feature,score))
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
        print('Cross validation: %0.5f'%score)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
    
    binary_y_train = y_train.copy()
    binary_y_test = y_test.copy()

    binary_y_train.num = y_train.apply(lambda x: int(x > 0))
    binary_y_test.num = y_test.apply(lambda x: int(x > 0))



    score,binary_y_pred = predict(method,X_train,binary_y_train,X_test,binary_y_test)
    print('Final predictor (train-test) accuracy: %0.5f'%score)
    print('Confusion matrix:')
    cm = confusion_matrix(y_test,binary_y_pred)
    print(cm)
    position_saver = []
    new_X_test = []
    new_y_test = []
    for i,v in enumerate(binary_y_pred):
        position_saver.append(i)
        new_y_test.append(v)
        new_X_test.append(X_test[i])
    score,y_pred = predict(method,X_train,y_train,new_X_test,new_y_test)
    print('Final predictor (train-test) accuracy: %0.5f'%score)
    print('Confusion matrix:')
    cm = confusion_matrix(y_test,y_pred)

    



if __name__ == '__main__':

    data = pd.read_csv('./data/processed.csv')

    if need_preprocess:
        data = preprocess(data,True)

    X = data.drop(['num'], axis=1)
    y = data.num
    #y = y.apply(lambda x: int(x > 0))


    #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)


    #score,_ = predict(X_train,y_train,X_test,y_test)
    #print(score)


    #for method_name,method in methods.items():
    perform_experiment('NB',X,y)
    
    
    # X = data[data['num'] != 0]
    # y = X.num
    # X = X.drop(['num'], axis=1)
    # perform_experiment('NB',X,y)
