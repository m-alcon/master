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
title_length = 70

methods = {
    'NB':   GaussianNB(),
    'NN':   KNeighborsClassifier(n_neighbors=28),
    'DT':   tree.DecisionTreeClassifier(),
    'SVM':  SVC(kernel="linear", C=1, gamma='auto')
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

def predict(method,X_train,y_train,X_test,y_test):
    y_pred = method.fit(X_train,y_train).predict(X_test)
    return accuracy_score(y_test,y_pred, normalize=True), y_pred

def predict_with_model(model,X_test,y_test):
    y_pred = model.predict(X_test)
    return accuracy_score(y_test,y_pred, normalize=True), y_pred

def feature_elimination_experiment(method,X,y,X_test,y_test,X_train,y_train):
    scores = cross_val_score(method, X, y, cv=10)
    main_score = np.mean(scores)
    print('Cross validation without feature elimination: %0.5f'%main_score)

    normal_score,_ = predict(method,X_train,y_train,X_test,y_test)
    print('Train-test without feature elimination: %0.5f'%normal_score)

    X_aux = X.copy()
    features_to_eliminate = []
    print('Dropping features:')
    for feature in list(X):
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
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

        scores = cross_val_score(method, X, y, cv=10)
        score = np.mean(scores)
        print('Cross validation: %0.5f'%score)
        feature_score,y_pred = predict(method,X_train,y_train,X_test,y_test)
        print('Final predicton accuracy: %0.5f'%feature_score)

        print('Confusion matrix:')
        cm = confusion_matrix(y_test,y_pred)
        print(cm)
        if feature_score < normal_score:
            score = -1
    return score, features_to_eliminate

def target_to_binary(y, y_train, y_test):
    binary_y = y.copy()
    binary_y_train = y_train.copy()
    binary_y_test = y_test.copy()

    binary_y = y.apply(lambda x: int(x > 0))
    binary_y_train = y_train.apply(lambda x: int(x > 0))
    binary_y_test = y_test.apply(lambda x: int(x > 0))
    return binary_y, binary_y_train, binary_y_test


def perform_experiment(method_name_1,method_name_2,X,y):
    print_title('=','%s & %s'%(method_name_1,method_name_2))

    method = methods[method_name_1]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

    print_title('-','Feature elimination')
    feature_elimination_experiment(method,X,y,X_test,y_test,X_train,y_train)

    print_title('-','Binary Feature elimination')
    binary_y, binary_y_train, binary_y_test = target_to_binary(y, y_train, y_test)
    feature_score, features = feature_elimination_experiment(method,X,binary_y,X_test,binary_y_test,X_train,binary_y_train)

    if features and feature_score != -1:
        X = X.drop(features, axis=1)
        X_train = X_train.drop(features, axis=1)
        X_test = X_test.drop(features, axis=1)

    # Train model and predict whether target y is 0 or 1, with 1 = {1,2,3}
    ## Test score
    print_title('-','First prediction')
    score,binary_y_pred = predict(method,X_train,binary_y_train,X_test,binary_y_test)
    print('Prediction 1 accuracy: %0.5f'%score)
    print('Confusion matrix:')
    cm = confusion_matrix(binary_y_test,binary_y_pred)
    print(cm)

    ## Train score
    score,train_binary_y_pred = predict(method,X_train,binary_y_train,X_train,binary_y_train)
    print_title('*','Method changed')
    method = methods[method_name_2]
    # Train model and predict if target is {0,1,2,3,4} with test data that predicts to 1 before
    ## New train data consists in all data with target != 0 and the ones that the other predictor failed
    new_X_train = X_train[y_train != 0]
    new_X_train = pd.concat([new_X_train,X_train[train_binary_y_pred != y_train]])
    new_y_train = y_train[y_train != 0]
    new_y_train = pd.concat([new_y_train,y_train[train_binary_y_pred != y_train]])
    #position_saver = [binary_y_pred != 0]

    ## New test data consists in all predictions != 0
    new_X_test = X_test[binary_y_pred != 0]
    new_y_test = y_test[binary_y_pred != 0]

    ## Prediction
    print_title('-','Second prediction')
    score,y_pred = predict(method,new_X_train,new_y_train,new_X_test,new_y_test)
    print('Prediction 2 accuracy: %0.5f'%score)
    print('Confusion matrix:')
    cm = confusion_matrix(new_y_test,y_pred)
    print(cm)

    print_title('-','Fusion')
    # Fusion predictions
    binary_indexs = binary_y_test.index.tolist()
    new_indexs = new_y_test.index.tolist()
    
    for i in range(len(binary_indexs)):
        if binary_y_pred[i] > 0:
            idx = new_indexs.index(binary_indexs[i])
            binary_y_pred[i] = y_pred[idx]

    print('Final accuracy: %0.5f'%accuracy_score(y_test,binary_y_pred, normalize=True))
    print('Final confusion matrix:')
    cm = confusion_matrix(y_test,binary_y_pred)
    print(cm)





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

    #####################################################################################################
    for method_name_1 in methods.keys():
        for method_name_2 in methods.keys():
            perform_experiment(method_name_1,method_name_2,X,y)
    
    ####################################################################################################
    # X = data[data['num'] != 0]
    # y = X.num
    # X = X.drop(['num'], axis=1)
    # perform_experiment('NB',X,y)
