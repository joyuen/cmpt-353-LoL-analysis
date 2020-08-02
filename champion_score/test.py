import sys 
import math
import pandas as pd
import numpy as np
import scipy.stats
import seaborn as sb
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

def filter_null(df):
    df = df[~df['W%'].str.contains('-')]
    return df
    
#Games/winrate bias
def gp_adjust(t, g, w):
    if float(w.replace('%','')) - 50 > 0:
        w = float(w.replace('%','')) - 50
    else:
        w = 1
        
    return (w * int(g))/t

#score champion by region currently only games-winrate adjusted
def champion_score(region):
    total = math.floor((int(region['GP'].iloc[0])/float((region['P%'].iloc[0]).replace('%',''))*100))
    region['score'] = region.apply(lambda x : gp_adjust(total,x['GP'], x['W%']), axis = 1)
    return region

#Correlate:Pearson  
def feature_correlation_region(matches, region, feature_list):
    matches = matches[matches['league'] == region]
    matches_player = matches[matches['player'].str.len() > -1]
    #subtract dataframe:https://stackoverflow.com/questions/23284409/how-to-subtract-rows-of-one-pandas-data-frame-from-another
    new = matches.merge(matches_player,how='left',indicator=True)
    new = new[(new['_merge']=='left_only')]
    matches = new.drop(columns='_merge')
    #seperate red and blue
    matches_red = matches[matches['side'] == 'Blue'][feature_list]
    matches_blue = matches[matches['side'] == 'Red'][feature_list]
    scaler = MinMaxScaler()
    matches_red = pd.DataFrame(scaler.fit_transform(matches_red), columns=matches_red.columns)
    matches_blue = pd.DataFrame(scaler.fit_transform(matches_blue), columns=matches_blue.columns)
    return matches_red.corr(method='pearson'), matches_blue.corr(method='pearson')

def sb_plot(plot):
    fig = plt.figure(figsize=(16, 16))
    sb.heatmap(plot, 
            xticklabels=plot.columns,
            yticklabels=plot.columns,
            cmap='RdBu_r',
            annot=True,)
    return fig
    

#Presence bias?
def p_bias(s, pb):
    return
#Single Counter pick bias

#Single ally bias

#Aggregated ..

# total matches?
def main():
    team_feature_list= ['gamelength', 'result', 'firstdragon', 'dragons', 'firstherald', 'heralds', 'firstbaron', 'firsttower', 'firsttothreetowers' , 'firstmidtower', 'damagetochampions', 'wardsplaced', 'wardskilled', 'controlwardsbought','visionscore', 'csdiffat10', 'golddiffat10', 'csat10','goldat10', 'csdiffat15', 'xpdiffat15', 'golddiffat15']
    lck = filter_null(pd.read_csv('LCK.csv'))
    lec = filter_null(pd.read_csv('LEC.csv'))
    lcs = filter_null(pd.read_csv('LCS.csv'))
    lpl = filter_null(pd.read_csv('LPL.csv'))
    match = pd.read_csv('2019.csv')
    
    #champion ranking
    # df = champion_score(lcs)
    # print('lcs\n')
    # print(df[['Champion','score','GP','W%']].sort_values(by=['score'], ascending=False))
    # df = champion_score(lec)
    # print('lec\n')
    # print(df[['Champion','score','GP','W%']].sort_values(by=['score'], ascending=False))
    # df = champion_score(lck)
    # print('lck\n')
    # print(df[['Champion','score','GP','W%']].sort_values(by=['score'], ascending=False))
    # df = champion_score(lpl)
    # print('lpl\n')
    # print(df[['Champion','score','GP','W%']].sort_values(by=['score'], ascending=False))
    
    #feature correlation specific team 
    # lcs_matches = match[match['league'] == 'LCS']
    # tsm = lcs_matches[lcs_matches['team']=='Team SoloMid']
    # tsm_player_stats = tsm[tsm['player'].str.len() > -1]
    #subtract dataframe:https://stackoverflow.com/questions/23284409/how-to-subtract-rows-of-one-pandas-data-frame-from-another
    # new = tsm.merge(tsm_player_stats,how='left',indicator=True)
    # new = new[(new['_merge']=='left_only')]
    # tsm_matches = new.drop(columns='_merge')
    
    #seperate data by side
    # tsm_matches_red = tsm_matches[tsm_matches['side'] == 'Blue'][team_feature_list]
    # tsm_matches_blue = tsm_matches[tsm_matches['side'] == 'Red'][team_feature_list]
    
    #scale dataframes
    # scaler = MinMaxScaler()
    # tsm_matches_red = pd.DataFrame(scaler.fit_transform(tsm_matches_red), columns=tsm_matches_red.columns)
    # tsm_matches_blue = pd.DataFrame(scaler.fit_transform(tsm_matches_blue), columns=tsm_matches_blue.columns)
    
    # pearsoncorr = tsm_matches_red.corr(method='pearson')
    # plt.figure(figsize=(16, 16))
    # sb.heatmap(pearsoncorr, 
            # xticklabels=pearsoncorr.columns,
            # yticklabels=pearsoncorr.columns,
            # cmap='RdBu_r',
            # annot=True,)
    # plt.savefig("tsm_red.png")
    # pearsoncorr = tsm_matches_blue.corr(method='pearson')
    # plt.figure(figsize=(16, 16))
    # sb.heatmap(pearsoncorr, 
            # xticklabels=pearsoncorr.columns,
            # yticklabels=pearsoncorr.columns,
            # cmap='RdBu_r',
            # annot=True,)
    # plt.savefig("tsm_blue.png")
    
    lcs_correlation_red,  lcs_correlation_blue = feature_correlation_region(match, 'LCS', team_feature_list)
    
    red = sb_plot(lcs_correlation_red)
    red.savefig("lcs_red.png")
    blue = sb_plot(lcs_correlation_blue)
    blue.savefig("lcs_blue.png")
    
    lpl_correlation_red,  lpl_correlation_blue = feature_correlation_region(match, 'LPL', team_feature_list)
    
    red = sb_plot(lpl_correlation_red)
    red.savefig("lpl_red.png")
    blue = sb_plot(lpl_correlation_blue)
    blue.savefig("lpl_blue.png") 

    lec_correlation_red,  lec_correlation_blue = feature_correlation_region(match, 'LEC', team_feature_list)
    
    red = sb_plot(lec_correlation_red)
    red.savefig("lec_red.png")
    blue = sb_plot(lec_correlation_blue)
    blue.savefig("lec_blue.png")

    lck_correlation_red,  lck_correlation_blue = feature_correlation_region(match, 'LCK', team_feature_list)
    
    red = sb_plot(lck_correlation_red)
    red.savefig("lck_red.png")
    blue = sb_plot(lck_correlation_blue)
    blue.savefig("lck_blue.png")
    #bans
    
    #gamelength, result, first dragon, dragons, first heralds, heralds, first barons, firsttower
    #firsttothreetowers, firstmidtower, damagetochamp, wardsplaced, wardskilled, controlwardsbought
    #visionscore, csdiffat10, golddiffat10, csat10,goldat10, csdiffat15, xpdiffat15, golddiffat15
    


if __name__=='__main__':
    main()