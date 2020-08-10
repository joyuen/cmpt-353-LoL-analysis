import sys 
import math
import pandas as pd
import numpy as np
import scipy.stats
from sklearn.preprocessing import FunctionTransformer
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier


def main():
    
    #read file
    df = pd.read_csv("data/"+sys.argv[1])
    df[df==np.inf]=np.nan
    df.fillna(df.mean(), inplace=True)
    
    #seperate data, the X can be adjusted
    #X = df[['red_team','blue_team']]
    X = df[['red_team','red_top','red_jng', 'red_mid', 'red_bot', 'red_sup' ,'blue_team','blue_top','blue_jng', 'blue_mid', 'blue_bot', 'blue_sup']]
    y = df['result']
    X_train, X_valid, y_train,y_valid = train_test_split(X, y)   
    
    
    bayes_model = GaussianNB().fit(X_train,y_train)
    predictions = bayes_model.score(X_valid,y_valid)
    print("\n")
    print("Bayes score: "+str(round(predictions,3))+"%\n")
    rf_model = RandomForestClassifier().fit(X_train,y_train)
    predictions = rf_model.score(X_valid,y_valid)   
    print("Random Forrest score: "+str(round(predictions,3))+"%\n")
    knn_model = KNeighborsClassifier(n_neighbors=10).fit(X_train,y_train)
    predictions = knn_model.score(X_valid,y_valid)   
    print("k-nearest score: "+str(round(predictions,3))+"%\n")
    
if __name__=='__main__':
    main()