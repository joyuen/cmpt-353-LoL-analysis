import sys 
import math
import pandas as pd
import numpy as np
import scipy.stats
import seaborn as sb
import re
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

#pre process match data to add kp and kda column
def pre_process(match):
    match['kp'] = match['kills']/match['teamkills']
    match['kda'] = match.apply(lambda x: kda(x['kills'], x['assists'], x['deaths']), axis = 1)
    return match

#Helper function
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

def feature_correlation_player(matches, team, position, feature_list):
    matches = matches[matches['team'] == team]
    matches = matches[matches['position'] == position][feature_list]
    #seperate red and blue
    scaler = MinMaxScaler()
    matches = pd.DataFrame(scaler.fit_transform(matches), columns=matches.columns)
    return matches.corr(method='pearson')
    
def feature_correlation_player_region(matches, region, position, feature_list):
    matches = matches[matches['league'] == region]
    matches = matches[matches['position'] == position][feature_list]
    #seperate red and blue
    scaler = MinMaxScaler()
    matches = pd.DataFrame(scaler.fit_transform(matches), columns=matches.columns)
    return matches.corr(method='pearson')

#feature correlation for player with sides
# def feature_correlation_player(matches, team, position, feature_list):
    # matches = matches[matches['team'] == team]
    # matches = matches[matches['position'] == position][feature_list]
    # #seperate red and blue
    # matches_red = (matches[matches['side'] == 'Blue']).drop(['side'], axis =1)
    # matches_blue = (matches[matches['side'] == 'Red']).drop(['side'], axis=1)
    # scaler = MinMaxScaler()
    # matches_red = pd.DataFrame(scaler.fit_transform(matches_red), columns=matches_red.columns)
    # matches_blue = pd.DataFrame(scaler.fit_transform(matches_blue), columns=matches_blue.columns)
    # return matches_red.corr(method='pearson'), matches_blue.corr(method='pearson') 
    
# def feature_correlation_player_region(matches, region, position, feature_list):
    # matches = matches[matches['league'] == region]
    # matches = matches[matches['position'] == position][feature_list]
    # #seperate red and blue
    # matches_red = (matches[matches['side'] == 'Blue']).drop(['side'], axis =1)
    # matches_blue = (matches[matches['side'] == 'Red']).drop(['side'], axis=1)
    # scaler = MinMaxScaler()
    # matches_red = pd.DataFrame(scaler.fit_transform(matches_red), columns=matches_red.columns)
    # matches_blue = pd.DataFrame(scaler.fit_transform(matches_blue), columns=matches_blue.columns)
    # return matches_red.corr(method='pearson'), matches_blue.corr(method='pearson')    
    
#calculate correlation difference
def diff_cor(cor, avg_cor):
    cor = abs(cor) - abs(avg_cor)
    return cor

#Add correlation values to dictionary
def add_correlation_dict(team_dict, match, region, team_feature_list, player_feature_list, champion_data):
    top_avg = feature_correlation_player_region(match, region, "top", player_feature_list)
    jng_avg = feature_correlation_player_region(match, region, "jng", player_feature_list)
    mid_avg = feature_correlation_player_region(match, region, "mid", player_feature_list)
    bot_avg = feature_correlation_player_region(match, region, "bot", player_feature_list)
    sup_avg = feature_correlation_player_region(match, region, "sup", player_feature_list)
    temp_dict={}
    for team in team_dict:
        for position in team_dict[team]:
            if position == "top":
                avg = top_avg
            if position == "jng":
                avg = jng_avg
            if position == "mid":
                avg = mid_avg
            if position == "bot":
                avg = bot_avg
            if position == "sup":
                avg = sup_avg
            correlation = feature_correlation_player(match, team, position, player_feature_list)  - avg           
            temp_dict.update({position+"_correlation":correlation})
            champion_score = get_score_adjusted(match, region, champion_data ,team, position, player_feature_list)
            temp_dict.update({position+"_champion_score":champion_score})
        team_dict[team].update(temp_dict)
        temp_dict = {}
    for team in team_dict:
        correlation_red, correlation_blue = feature_correlation_region(match,region,team_feature_list)
        team_dict[team].update({"correlation_red":correlation_red})
        team_dict[team].update({"correlation_blue":correlation_blue})
    return team_dict
 
#add kp and kda column
def kda(kills, assists, deaths):
    if deaths == 0:
        deaths = 1
    return (kills+assists)/deaths

#helper
def gp_adjust( g, w, p):
    return ((w * int(g)) + p*10)/3
    
#score champion by region currently only games-winrate adjusted
def champion_score(region):
    region['score'] = region.apply(lambda x : gp_adjust(x['GP'], x['W%'], x['P+B%']), axis = 1)
    return region

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
    
#champion performance evaluation for a player, compared to average using given stats
def performance_on_champ(champion_stats, matches, team, position, champion):
    try:
        matches = matches[matches['team'] == team]
        matches = matches[matches['position'] == position]
        matches = matches[matches['champion'] == champion]
        #no matches played by that player on that champion
        if matches.empty:
            return 0.8
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
        #no data available, provide default guess o
        return 0.8


#assign champion compatibility given player data
#helper functions
def champ_compat_calc_help(x, champ_data):
    similar =  champ_data[x['index']] - x['scaled']
    return abs(similar)
    
def champ_compat_calc(champ_data, compat_dict):
    scaler = MinMaxScaler()  
    compat = pd.DataFrame(scaler.fit_transform(compat_dict), columns=compat_dict.columns)
    compat_dict = compat_dict.reset_index()
    compat_dict['scaled'] = compat
    compat_dict['similar'] = compat_dict.apply(lambda x: champ_compat_calc_help(x,champ_data), axis=1)
    return(10 - (compat_dict['similar'].sum()))

#Get champion compatibility score, champion scores, score adjusted, and performance
def champ_compat(position, player_cor, champ_data, team, matches):
    compat_dict = {"K":1, "D":1, "A":1, "KDA": 1, "KP":1, "FB%":1, "GD10":1, "XPD10":1, "CSD10":1, "CSPM":1, "DPM":1, "DMG%":1, "GOLD%":1, "WPM":1, "WCPM":1}
    #get champion scores
    #unmatching names requiring manual assignment
    champion_stats = champ_data
    champ_score = champion_score(champ_data)
    if position == "top":
        position_champ = "Top"
    if position == "jng":
        position_champ = "Jungle"
    if position == "mid":
        position_champ = "Middle"
    if position == "bot":
        position_champ = "ADC"
    if position == "sup":
        position_champ = "Support"
    player_cor = player_cor['result'][1:] 
    #champ_data = champ_data[champ_data['Pos']== position_champ]
    champ_score = (champ_score[champ_score['Pos']== position_champ])[['Champion', 'score']]
    #malformed and unmatching names requiring manual assignment
    compat_dict["K"] = compat_dict["K"] + player_cor['kills']
    compat_dict["D"] = compat_dict["D"] + player_cor['deaths']
    compat_dict["A"] = compat_dict["A"] + player_cor['assists']
    compat_dict["KDA"] = compat_dict["KDA"] + player_cor['kda']
    compat_dict["FB%"] = compat_dict["FB%"] + player_cor['firstblood']
    compat_dict["KP"] = compat_dict["KP"] + player_cor['kp']
    compat_dict["GD10"] = compat_dict["GD10"] + player_cor['golddiffat10']
    compat_dict["GD10"] = compat_dict["GD10"] + player_cor['golddiffat15']
    compat_dict["XPD10"] = compat_dict["XPD10"] + player_cor['xpdiffat10']
    compat_dict["XPD10"] = compat_dict["XPD10"] + player_cor['xpdiffat15']
    compat_dict["CSD10"] = compat_dict["CSD10"] + player_cor['csdiffat10']
    compat_dict["CSD10"] = compat_dict["CSD10"] + player_cor['csdiffat15']
    compat_dict["CSPM"] = compat_dict["CSPM"] + player_cor['cspm']
    compat_dict["DPM"] = compat_dict["DPM"] + player_cor['dpm']
    compat_dict["DMG%"] = compat_dict["DMG%"] + player_cor['damageshare']
    compat_dict["GOLD%"] = compat_dict["GOLD%"] + player_cor['earnedgoldshare']
    compat_dict["WPM"] = compat_dict["WPM"] + player_cor['visionscore']
    compat_dict["WCPM"] = compat_dict["WCPM"] + player_cor['visionscore']
    compat_dict["WPM"] = compat_dict["WPM"] + player_cor['controlwardsbought']
    compat_dict["WCPM"] = compat_dict["WCPM"] + player_cor['controlwardsbought']
    compat_dict["WCPM"] = compat_dict["WCPM"] + player_cor['controlwardsbought']    
    #scale for manipulation
    scaler = MinMaxScaler()   
    compat_dict = pd.DataFrame.from_dict(compat_dict, orient='index')  
    scale = champ_data.iloc[:,2:]
    scale = scale.loc[:,scale.columns !='Pos']
    scale = pd.DataFrame(scaler.fit_transform(scale), columns=scale.columns)
    scale['Champion'] = champ_data['Champion'].reset_index().drop(columns=['index'])
    champ_data = scale    
    champ_data['compatibility'] = champ_data.apply(lambda x : champ_compat_calc(x, compat_dict),axis=1)
    champ_data = champ_data.set_index("Champion").join(champ_score.set_index("Champion"), how='left', lsuffix='_left', rsuffix='_right').reset_index()
    champ_data['performance'] = champ_data.apply(lambda x: performance_on_champ(champion_stats, matches, team, position, x['Champion']),axis=1)   
    champ_data = champ_data[['Champion', 'compatibility', 'score_right', 'performance']]
    champ_data = champ_data.rename(columns={'score_right':'score'})
    champ_data['score'] = champ_data['score'].fillna(3)
    champ_data['score_adjusted'] = ((champ_data['compatibility']* champ_data['performance']) *(champ_data['score'] * champ_data['performance']))
    champ_data['score_adjusted'] = champ_data['score_adjusted'].clip(lower=10)
    return (champ_data.sort_values(by='score_adjusted', ascending = False))

#easier use of function 
def get_score_adjusted(match, region, champ_data,team, position, player_feature_list):
    return champ_compat(position, diff_cor( feature_correlation_player(match, team, position, player_feature_list), feature_correlation_player_region(match, region, position, player_feature_list)), champ_data, team, match)
 
#get matches from matches file for a region
def get_matches(matches, region):
    condensed_matches = []
    matches = matches[matches['league'] == region]
    unique_matches = matches['gameid'].unique()
    for each in unique_matches:
        match = matches[matches['gameid'] == each]
        match = match[match['player'].str.len() > -1]
        red_team = match[match['side'] == "Red"]
        blue_team = match[match['side'] == "Blue"]
        red = {
            "team":red_team.loc[red_team.position =="top", 'team'].values[0], 
            "result": red_team.loc[red_team.position =="top", 'result'].values[0],
            "top": red_team.loc[red_team['position']=="top", 'champion'].values[0],
            "jng":red_team.loc[red_team['position']=="jng", 'champion'].values[0],
            "mid":red_team.loc[red_team['position']=="mid", 'champion'].values[0],
            "bot":red_team.loc[red_team['position']=="bot", 'champion'].values[0],
            "sup":red_team.loc[red_team['position']=="sup", 'champion'].values[0]}
        blue = {
            "team":blue_team.loc[blue_team.position =="top", 'team'].values[0], 
            "result": blue_team.loc[blue_team.position =="top", 'result'].values[0],
            "top": blue_team.loc[blue_team['position']=="top", 'champion'].values[0],
            "jng":blue_team.loc[blue_team['position']=="jng", 'champion'].values[0],
            "mid":blue_team.loc[blue_team['position']=="mid", 'champion'].values[0],
            "bot":blue_team.loc[blue_team['position']=="bot", 'champion'].values[0],
            "sup":blue_team.loc[blue_team['position']=="sup", 'champion'].values[0]}
        this_match = {"red":red,"blue":blue}
        condensed_matches.append(this_match)
    return condensed_matches          


#assemble data for evaluation 
def evaluate(matches, team_dict, metric):
    team_score = []
    top_score = []
    jng_score = []
    mid_score = []
    bot_score = []
    sup_score = []   
    x = 0
    for each in matches:
        try:
            team = each['red']['team']
            red_result = each['red']['result']
            top_red_score = team_dict[team]['top_champion_score'].loc[(team_dict[team]['top_champion_score'])['Champion']==each['red']['top'], metric].values[0]
            jng_red_score = team_dict[team]['jng_champion_score'].loc[(team_dict[team]['jng_champion_score'])['Champion']==each['red']['jng'], metric].values[0]
            mid_red_score = team_dict[team]['mid_champion_score'].loc[(team_dict[team]['mid_champion_score'])['Champion']==each['red']['mid'], metric].values[0]
            bot_red_score = team_dict[team]['bot_champion_score'].loc[(team_dict[team]['bot_champion_score'])['Champion']==each['red']['bot'], metric].values[0]
            sup_red_score = team_dict[team]['sup_champion_score'].loc[(team_dict[team]['sup_champion_score'])['Champion']==each['red']['sup'], metric].values[0]
            red_score = top_red_score + jng_red_score+ mid_red_score+ bot_red_score+ sup_red_score
            team = each['blue']['team']
            result = each['blue']['result']
            top_blue_score = team_dict[team]['top_champion_score'].loc[(team_dict[team]['top_champion_score'])['Champion']==each['blue']['top'], metric].values[0]
            jng_blue_score = team_dict[team]['jng_champion_score'].loc[(team_dict[team]['jng_champion_score'])['Champion']==each['blue']['jng'], metric].values[0]
            mid_blue_score = team_dict[team]['mid_champion_score'].loc[(team_dict[team]['mid_champion_score'])['Champion']==each['blue']['mid'], metric].values[0]
            bot_blue_score = team_dict[team]['bot_champion_score'].loc[(team_dict[team]['bot_champion_score'])['Champion']==each['blue']['bot'], metric].values[0]
            sup_blue_score = team_dict[team]['sup_champion_score'].loc[(team_dict[team]['sup_champion_score'])['Champion']==each['blue']['sup'], metric].values[0]
            blue_score = top_blue_score + jng_blue_score+ mid_blue_score+ bot_blue_score+ sup_blue_score
            team_score.append([(red_score/blue_score), red_result])
            top_score.append([(top_red_score/top_blue_score), red_result])
            jng_score.append([(jng_red_score/jng_blue_score), red_result])
            mid_score.append([(mid_red_score/mid_blue_score), red_result])
            bot_score.append([(bot_red_score/bot_blue_score), red_result])
            sup_score.append([(sup_red_score/sup_blue_score), red_result])            
        except:
                #print(each)
                x +=1
    # print(arith_eval(team_score,"team"))
    # print(arith_eval(top_score,"top"))
    # print(arith_eval(jng_score,"jng"))
    # print(arith_eval(mid_score,"mid"))
    # print(arith_eval(bot_score,"bot"))
    # print(arith_eval(sup_score,"sup"))
    return arith_eval(team_score,"team"), arith_eval(top_score,"top"), arith_eval(jng_score,"jng"), arith_eval(mid_score,"mid"), arith_eval(bot_score,"bot"), arith_eval(sup_score,"sup")

#perform arthimitec on assembled data   
def arith_eval(arr,pos):
    score = 0
    x = 0
    for x, each in enumerate(arr):
        if each[0] > 1:
            if each[1] == 1:
                score+=1
        else:
            if each[1] == 0:
                score+=1
    return (pos + " score :" + str(score) +"/"+str(x) +"\n")

#aggregate two champion datafiles into one
def aggregate(df1, df2): 
   df1 = df1.applymap(lambda x: percent_to_int(x))
   df2 = df2.applymap(lambda x: percent_to_int(x))
   df1['K'] = df1['K'].apply(int).div(df1["GP"].apply(int))
   df1['D'] = df1['D'].apply(int).div(df1["GP"].apply(int))
   df1['A'] = df1['A'].apply(int).div(df1["GP"].apply(int))
   df2['K'] = df2['K'].apply(int).div(df2["GP"].apply(int))
   df2['D'] = df2['D'].apply(int).div(df2["GP"].apply(int))
   df2['A'] = df2['A'].apply(int).div(df2["GP"].apply(int))
   #Duplicate rows:https://stackoverflow.com/questions/50788508/replicating-rows-in-pandas
   temp1 = pd.DataFrame(np.repeat(df1.values,df1["GP"],axis = 0))
   temp1.columns = df1.columns
   temp1['GP'] = 1
   temp2 = pd.DataFrame(np.repeat(df2.values,df2["GP"],axis = 0))
   temp2.columns = df2.columns
   temp2['GP'] = 1
   result = pd.concat([temp1, temp2])
   result = result.applymap(lambda x: percent_to_int(x))
   games_played = result.groupby(['Champion']).sum().reset_index()
   games_played = games_played.apply(lambda x: aggregate_help(x, result),axis=1)
   return (games_played.sort_values(by='GP', ascending = False))

#perform sum operations on rows 
def aggregate_help(x, df):  
    champ = x['Champion']
    gp = x['GP']
    df= df[df['Champion'] == champ]
    x['Pos'] = df.iloc[0]['Pos']
    for column in df:
        if column not in ['Champion', 'Pos', 'GP']:
            x[str(column)] = round((df[str(column)].apply(pd.to_numeric).sum())/(gp),3)
    return x

#make list from get matches
def make_list_help(matches, side,pos): 
    res = []
    for each in matches:
        res.append(each[side][pos])
    return res

def make_list(train_matches):   
    df = pd.DataFrame()
    df['result'] = make_list_help(train_matches, 'red', 'result')
    df['red_team'] = make_list_help(train_matches, 'red', 'team')
    df['red_top'] = make_list_help(train_matches, 'red', 'top')
    df['red_jng'] = make_list_help(train_matches, 'red', 'jng')
    df['red_mid'] = make_list_help(train_matches, 'red', 'mid')
    df['red_bot'] = make_list_help(train_matches, 'red', 'bot')
    df['red_sup'] = make_list_help(train_matches, 'red', 'sup')
    df['blue_team'] = make_list_help(train_matches, 'blue', 'team')
    df['blue_top'] = make_list_help(train_matches, 'blue', 'top')
    df['blue_jng'] = make_list_help(train_matches, 'blue', 'jng')
    df['blue_mid'] = make_list_help(train_matches, 'blue', 'mid')
    df['blue_bot'] = make_list_help(train_matches, 'blue', 'bot')
    df['blue_sup'] = make_list_help(train_matches, 'blue', 'sup')   
    return df

def make_data_help(champ, team, team_dict, metric,ind):
    try:
        return round(team_dict[team][ind].loc[(team_dict[team][ind])['Champion']==champ, metric].values[0], 3)
    except:
        #use median values if there is problem with data
        if metric == 'performance':
            return 0.8
        elif metric == 'Champion_score':
            return 10
        elif metric == 'compatibility':
            return 3.0
        elif metric == 'score_adjusted':
            return 15
        else:
            return 0.8
def team_score(x, side):
    return (x[side+'_top'] + x[side+'_jng'] + x[side+'_mid'] + x[side+'_bot'] + x[side+'_sup'])

def make_data(train_list, team_dict,metric): 
    df = pd.DataFrame()
    df['result'] = train_list['result']
    df['red_top'] = train_list.apply(lambda x: make_data_help(x['red_top'],x['red_team'], team_dict, metric, 'top_champion_score'), axis=1)
    df['red_jng'] = train_list.apply(lambda x: make_data_help(x['red_jng'],x['red_team'], team_dict, metric, 'jng_champion_score'), axis=1)
    df['red_mid'] = train_list.apply(lambda x: make_data_help(x['red_mid'],x['red_team'], team_dict, metric, 'mid_champion_score'), axis=1)
    df['red_bot'] = train_list.apply(lambda x: make_data_help(x['red_bot'],x['red_team'], team_dict, metric, 'bot_champion_score'), axis=1)
    df['red_sup'] = train_list.apply(lambda x: make_data_help(x['red_sup'],x['red_team'], team_dict, metric, 'sup_champion_score'), axis=1)
    df['blue_top'] = train_list.apply(lambda x: make_data_help(x['blue_top'],x['blue_team'], team_dict, metric, 'top_champion_score'), axis=1)
    df['blue_jng'] = train_list.apply(lambda x: make_data_help(x['blue_jng'],x['blue_team'], team_dict, metric, 'jng_champion_score'), axis=1)
    df['blue_mid'] = train_list.apply(lambda x: make_data_help(x['blue_mid'],x['blue_team'], team_dict, metric, 'mid_champion_score'), axis=1)
    df['blue_bot'] = train_list.apply(lambda x: make_data_help(x['blue_bot'],x['blue_team'], team_dict, metric, 'bot_champion_score'), axis=1)
    df['blue_sup'] = train_list.apply(lambda x: make_data_help(x['blue_sup'],x['blue_team'], team_dict, metric, 'sup_champion_score'), axis=1)
    df['red_team'] = df.apply(lambda x:team_score(x, "red"), axis=1)
    df['blue_team'] = df.apply(lambda x:team_score(x, "blue"), axis=1)
    return df
   
#function from player_comparison
def percent_to_float(x):
    return float(x.strip("%"))/100

def format_df(df):
    df["W%"] = df["W%"].apply(lambda x: percent_to_float(x))
    return df
def filter_players(df):
    df = df[df["GP"] >= 10] # minimum of 10 professional games to be considered
    return df

def fix_stats(df):
    df["GP"] = df["GP"] / 5
    df["W%"] = df["W%"] / 5
    df["K"] = df["K"] / 5
    df["D"] = df["D"] / 5
    df["A"] = df["A"] / 5
    df["KDA"] = df["KDA"] / 5
    df["GD10"] = df["GD10"] / 5
    df["XPD10"] = df["XPD10"] / 5
    df["CSD10"] = df["CSD10"] / 5
    df["CSPM"] = df["CSPM"] / 5
    df["DPM"] = df["DPM"] / 5
    df["WPM"] = df["WPM"] / 5
    df["WCPM"] = df["WCPM"] / 5
    return df 
    
def score_player(df, pos):
    df = df[df["Pos"] == pos]

    gold = df.sort_values(by=["GD10", "GP"], ascending=False).reset_index(drop=True)
    xp = df.sort_values(by=["XPD10", "GP"], ascending=False).reset_index(drop=True)
    cs = df.sort_values(by=["CSD10", "GP"], ascending=False).reset_index(drop=True)
    winrate = df.sort_values(by=["W%", "GP"], ascending=False).reset_index(drop=True)
    kda = df.sort_values(by=["KDA", "GP"], ascending=False).reset_index(drop=True)

    gold["rank"] = gold.index + 1
    xp["rank"] = xp.index + 1
    cs["rank"] = cs.index + 1
    winrate["rank"] = winrate.index + 1
    kda["rank"] = kda.index + 1

    gold["goldrank"] = gold["rank"]  
    xp["xprank"] = xp["rank"] 
    cs["csrank"] = cs["rank"] 
    winrate["wrrank"] = winrate["rank"] 
    kda["kdarank"] = kda["rank"]

    frames = [gold, xp, cs, winrate, kda]
    res = pd.concat(frames)
    res = fix_stats(res)
    res = res.groupby(["Team", "Pos"], as_index=False).sum() 

    res["rank"] = res["goldrank"] * 0.25 + res["xprank"] * 0.25 + res["csrank"] * 0.25 + res["wrrank"] * 0.125 + res["kdarank"] * 0.125   
    
    res = res.sort_values(by=["rank"], ascending = False).reset_index()
    res["rank"] = (res.index + 1)/10
    res = res.drop(["index"], axis=1)
    if pos == "Top":
        pos = "top"
    if pos == "Jungle":
        pos = "jng"
    if pos == "Middle":
        pos = "mid"
    if pos == "ADC":
        pos = "bot"
    if pos == "Support":
        pos = "sup"
    res['pos'] = pos

    new_df = res[["Team",'pos', "rank"]]

    return new_df 

#format player comparison data   
def make_player_data_help(x_team, pos):
    try:
        return (pos.loc[pos['Team'] == x_team, 'rank'].iloc[0])
    except:
        return 0.5

def make_player_data(df, matches):
    top = score_player(df, "Top")
    jng = score_player(df, "Jungle")
    mid = score_player(df, "Middle")
    bot = score_player(df, "ADC")
    sup = score_player(df, "Support")
    df = pd.DataFrame()
    df['result'] = matches['result']
    df['red_top'] = matches.apply(lambda x:make_player_data_help(x['red_team'],top), axis = 1)
    df['red_jng'] = matches.apply(lambda x:make_player_data_help(x['red_team'],jng), axis = 1)
    df['red_mid'] = matches.apply(lambda x:make_player_data_help(x['red_team'],mid), axis = 1)
    df['red_bot'] = matches.apply(lambda x:make_player_data_help(x['red_team'],bot), axis = 1)
    df['red_sup'] = matches.apply(lambda x:make_player_data_help(x['red_team'],sup), axis = 1)
    df['blue_top'] = matches.apply(lambda x:make_player_data_help(x['blue_team'],top), axis = 1)
    df['blue_jng'] = matches.apply(lambda x:make_player_data_help(x['blue_team'],jng), axis = 1)
    df['blue_mid'] = matches.apply(lambda x:make_player_data_help(x['blue_team'],mid), axis = 1)
    df['blue_bot'] = matches.apply(lambda x:make_player_data_help(x['blue_team'],bot), axis = 1)
    df['blue_sup'] = matches.apply(lambda x:make_player_data_help(x['blue_team'],sup), axis = 1)
    df['red_team'] = df.apply(lambda x:team_score(x, "red"), axis=1)
    df['blue_team'] = df.apply(lambda x:team_score(x, "blue"), axis=1)
    return df
 
#heat plot
def sb_plot(plot):
    fig = plt.figure(figsize=(16, 16))
    sb.heatmap(plot, 
            xticklabels=plot.columns,
            yticklabels=plot.columns,
            cmap='RdBu_r',
            annot=True,)
    return fig
    