import sys 
import math
import pandas as pd
import numpy as np
import scipy.stats
from scipy import stats
import matplotlib.pyplot as plt
from sklearn.preprocessing import FunctionTransformer
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier

def compare(model, X, region):
    #please ensure you input the appropriate region for the file you are using
    if region == "lck":
        region_data =  pd.read_csv("data/lck_matches.csv")
    elif region == "lec":
        region_data =  pd.read_csv("data/lec_matches.csv")
    elif region == "lcs":
        region_data =  pd.read_csv("data/lcs_matches.csv")
    else:
        return "please use a valid region"

    power_dict = {}
    team_dict = {}
    model_results = model.predict(X)
    team_list = region_data['red_team'].unique().tolist()
    for each in team_list:
        temp_red = region_data[region_data['red_team'] == each]
        temp_blue = region_data[region_data['blue_team'] == each]
        res_red = temp_red['result'].sum()
        tot_red = temp_red['result'].count()
        res_blue = temp_blue['result'].sum()
        tot_blue = temp_blue['result'].count()
        power_dict[each] = {"wins": (res_red + (tot_blue - res_blue)), "total":(tot_blue +tot_red)}
        team_dict[each] = {"correct":0, "total":0}
    for x, each in enumerate(model_results):
        if model_results[x] == region_data.iloc[x]['result']:
            team_dict[region_data.iloc[x]['red_team']]['correct'] +=1
            team_dict[region_data.iloc[x]['blue_team']]['correct'] +=1
        team_dict[region_data.iloc[x]['red_team']]['total'] +=1
        team_dict[region_data.iloc[x]['blue_team']]['total'] +=1 
    arr = []
    for each in team_dict:
        arr.append((team_dict[each]['correct']/team_dict[each]['total']))
    arr2 = []
    for each in team_dict:
        arr2.append((power_dict[each]['wins']/power_dict[each]['total']))
    return team_list, arr, arr2

    
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
    
#produce a bar plot to compare correct predictions by team to give insight of the legitimacy of the predictions
#################################################################################################################
    #ex.bayes
    team_list, correct_arr, power_arr = compare(bayes_model, X, "lck")
    
    #less than 0.05, there is a relationship between win percentage and prediction accuracy
    print("P-value manwhitney prediction%/win%: "+ str(stats.mannwhitneyu(correct_arr, power_arr).pvalue))
    
    plt.figure(figsize=(15,10))
    plt.bar(team_list, correct_arr)
    plt.xticks(rotation=35)
    plt.title("lck teams vs percentage of correct predictions")
    plt.xlabel('Teams')
    plt.ylabel('%predictions correct')
    plt.savefig("lck_predictions_by_team.png")
    plt.show()
    
    plt.bar(team_list, power_arr) 
    plt.xticks(rotation=35)
    plt.title("lck teams vs win percentage")
    plt.xlabel('Teams')
    plt.ylabel('win%')
    plt.savefig("lck_wins_by_team.png")
    plt.show()   
if __name__=='__main__':
    main()