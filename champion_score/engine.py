import sys 
import math
import pandas as pd
import numpy as np
import scipy.stats
import seaborn as sb
import re
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler


#Helper functions
def filter_null(df):
    df = df[~df['W%'].str.contains('-')]
    return df

#Change malformed strings in champion stats to useable ints where applicable, complex to be used with map
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

#Collect list of players for a team in dictionary format        
def collect_team_dict(matches, region):
    matches = matches[matches['league'] == region]
    teams = matches['team']
    teams = (teams.unique()).tolist()
    team_dict = {}
    for each in teams:
        team_dict[each] = {
            "top": ((matches[(matches['team'] == each) & (matches['position'] == 'top')])['player']).value_counts().index[0],
            "jng": ((matches[(matches['team'] == each) & (matches['position'] == 'jng')])['player']).value_counts().index[0],
            "mid": ((matches[(matches['team'] == each) & (matches['position'] == 'mid')])['player']).value_counts().index[0],
            "bot": ((matches[(matches['team'] == each) & (matches['position'] == 'bot')])['player']).value_counts().index[0],
            "sup": ((matches[(matches['team'] == each) & (matches['position'] == 'sup')])['player']).value_counts().index[0]
        }
    return team_dict
    
#Add correlation values to dictionary
def add_correlation(team_dict, match, region, team_feature_list, player_feature_list):
    temp_dict={}
    for team in team_dict:
        for position in team_dict[team]:
            correlation_red, correlation_blue = feature_correlation_player(match, team, position, player_feature_list)           
            temp_dict.update({position+"_correlation_red":correlation_red})
            temp_dict.update({position+"_correlation_blue":correlation_blue}) 
        team_dict[team].update(temp_dict)
        temp_dict = {}
    for team in team_dict:
        correlation_red, correlation_blue = feature_correlation_region(match,region,team_feature_list)
        team_dict[team].update({"correlation_red":correlation_red})
        team_dict[team].update({"correlation_blue":correlation_blue})
    return team_dict
    
#Games/winrate bias
def gp_adjust(t, g, w):
    if float(w.replace('%','')) - 50 > 0:
        w = float(w.replace('%','')) - 50
    else:
        w = 1 
    return (w * int(g))/t
 
#Evaluate at 10 stats for performance on champion
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
    #seperate red and blue
    matches_red = (matches[matches['side'] == 'Blue']).drop(['side'], axis =1)
    matches_blue = (matches[matches['side'] == 'Red']).drop(['side'], axis=1)
    scaler = MinMaxScaler()
    matches_red = pd.DataFrame(scaler.fit_transform(matches_red), columns=matches_red.columns)
    matches_blue = pd.DataFrame(scaler.fit_transform(matches_blue), columns=matches_blue.columns)
    return matches_red.corr(method='pearson'), matches_blue.corr(method='pearson')  

#naive champion performance evaluation for a player
def performance_on_champ(champion_stats, matches, team, position, champion):
    try:
        matches = matches[matches['team'] == team]
        matches = matches[matches['position'] == position]
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
        
#heat plot
def sb_plot(plot):
    fig = plt.figure(figsize=(16, 16))
    sb.heatmap(plot, 
            xticklabels=plot.columns,
            yticklabels=plot.columns,
            cmap='RdBu_r',
            annot=True,)
    return fig
    