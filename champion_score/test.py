import sys 
import math
import pandas as pd
import numpy as np
import scipy.stats
import seaborn as sb
import re
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

def filter_null(df):
    df = df[~df['W%'].str.contains('-')]
    return df

#change malformed strings in champion stats to useable ints where applicable
def percent_to_int(x):
    if type(x) == str:
        if "%" in x:
            x = int(x.replace('%','').replace('.',''))
            if x > 100:
                x = x/1000
                return x
            else:
                return x/100
        else:
            return x
    else:
        return x
    
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
 
#only first line is different from region
def feature_correlation_team(matches, team, feature_list):
    matches = matches[matches['team'] == team]
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

def feature_correlation_player(matches, team, position, feature_list):
    matches = matches[matches['team'] == team]
    matches = matches[matches['position'] == position][feature_list]
    matches['kp'] = matches['kills']/matches['teamkills']
    matches_red = matches[matches['side'] == 'Blue'][feature_list]
    matches_blue = matches[matches['side'] == 'Red'][feature_list]
    scaler = MinMaxScaler()
    matches_red = pd.DataFrame(scaler.fit_transform(matches_red), columns=matches_red.columns)
    matches_blue = pd.DataFrame(scaler.fit_transform(matches_blue), columns=matches_blue.columns)
    matches = pd.DataFrame(scaler.fit_transform(matches), columns=matches.columns)
    return matches_red.corr(method='pearson'), matches_blue.corr(method='pearson')

#evaluate at 10 stats
def eval_at_10(x,y,type_stat):
    if (x > y) or (x==y):
        if type_stat == "cs":
            if (x - y) < 15:
                return (1 + (x-y)/15)
            else:
                return 2
        if type_stat == "g":
            if (x - y) < 300:
                return (1 + (x-y)/300)
            else:
                return 2
        if type_stat == "xp":
            if (x - y) < 300:
                return (1 + (x-y)/300)
            else:
                return 2           
    else:
        if type_stat == "cs":
            if(x - y) > -15:
                return (1 + (x-y)/15)
            else:
                return 0
        if type_stat == "g":
            if (x - y) > -300:
                return (1 + (x-y)/300)
            else:
                return 0
        if type_stat == "xp":
            if (x - y) > -300:
                return (1 + (x-y)/300)
            else:
                return 0   

def performance_on_champ(champion_stats, matches, player, champion):
    try:
        matches = matches[matches['player'] == player]
        matches = matches[matches['champion'] == champion]
        champion_stats = champion_stats[champion_stats['Champion'] == champion]
        matches['deaths'] = matches['deaths'].replace(0,1)
        matches['kda'] = (matches['kills']+matches['assists'])/matches['deaths']
        matches['kp'] = matches['kills']/matches['teamkills']
        matches = matches[['kda','kp','cspm', 'dpm', 'damageshare', 'xpdiffat10', 'csdiffat10', 'golddiffat10', 'wpm', 'wcpm']].mean(axis=0)  
        champion_stats = champion_stats.applymap(lambda x: percent_to_int(x))
        #arbitrary computation
        kda = float(matches['kda'])/float(champion_stats['KDA'])   
        kp = float(matches['kp'])/float(champion_stats['KP'])
        cspm = float(matches['cspm'])/float(champion_stats['CSPM'])
        dpm = float(matches['dpm'])/float(champion_stats['DPM'])
        damageshare =float(matches['damageshare'])/float(champion_stats['DMG%'])
        xd10 = eval_at_10(float(matches['xpdiffat10']),float(champion_stats['XPD10']),"xp")
        cd10 = eval_at_10(float(matches['csdiffat10']),float(champion_stats['CSD10']),"cs")
        gd10 = eval_at_10(float(matches['golddiffat10']),float(champion_stats['GD10']),"g")
        wpm = float(matches['wpm'])/float(champion_stats['WPM'])
        wcpm = float(matches['wcpm'])/float(champion_stats['WCPM'])
        return ((kda+kp+cspm+dpm+damageshare+xd10+cd10+gd10+wpm+wcpm)/10)
    except:
        #no data available, provide default guess of 1
        return 1

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
    player_feature_list = ['result', 'kills', 'deaths','assists', 'firstblood', 'dpm', 'damageshare',  'controlwardsbought', 'visionscore', 'earned gpm', 'earnedgoldshare', 'cspm','csdiffat10', 'xpdiffat10','golddiffat10', 'csdiffat15', 'xpdiffat15', 'golddiffat15' ]
    team_feature_list= ['gamelength', 'result', 'firstdragon', 'dragons', 'firstherald', 'heralds', 'firstbaron', 'firsttower', 'firsttothreetowers' , 'firstmidtower', 'damagetochampions', 'wardsplaced', 'wardskilled', 'controlwardsbought','visionscore', 'csdiffat10', 'golddiffat10', 'csdiffat15', 'xpdiffat15', 'golddiffat15']
    lck = filter_null(pd.read_csv('LCK.csv'))
    lec = filter_null(pd.read_csv('LEC.csv'))
    lcs = filter_null(pd.read_csv('LCS.csv'))
    lpl = filter_null(pd.read_csv('LPL.csv'))
    match = pd.read_csv('2019.csv')

    print(performance_on_champ(lcs, match, 'Bjergsen','Syndra'))
       
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
    
    # lcs_correlation_red,  lcs_correlation_blue = feature_correlation_region(match, 'LCS', team_feature_list)
    
    # red = sb_plot(lcs_correlation_red)
    # red.savefig("lcs_red.png")
    # blue = sb_plot(lcs_correlation_blue)
    # blue.savefig("lcs_blue.png")
    
    # lpl_correlation_red,  lpl_correlation_blue = feature_correlation_region(match, 'LPL', team_feature_list)
    
    # red = sb_plot(lpl_correlation_red)
    # red.savefig("lpl_red.png")
    # blue = sb_plot(lpl_correlation_blue)
    # blue.savefig("lpl_blue.png") 

    # lec_correlation_red,  lec_correlation_blue = feature_correlation_region(match, 'LEC', team_feature_list)
    
    # red = sb_plot(lec_correlation_red)
    # red.savefig("lec_red.png")
    # blue = sb_plot(lec_correlation_blue)
    # blue.savefig("lec_blue.png")

    # lck_correlation_red,  lck_correlation_blue = feature_correlation_region(match, 'LCK', team_feature_list)
    
    # red = sb_plot(lck_correlation_red)
    # red.savefig("lck_red.png")
    # blue = sb_plot(lck_correlation_blue)
    # blue.savefig("lck_blue.png")
    #bans
    
if __name__=='__main__':
    main()