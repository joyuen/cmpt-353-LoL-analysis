from engine import *
import csv

from sklearn.preprocessing import FunctionTransformer
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier


def load_data(matches):
    matches = pd.read_csv('data/'+matches)
    matches = pre_process(matches)
    return matches

#aggregate to take data for champions from the full year
def load_data_agg(spring, springp, summer, summerp):
    lcs1 = filter_null(pd.read_csv(spring))
    lcs2 = filter_null(pd.read_csv(springp))
    lcs3 = filter_null(pd.read_csv(summer))
    lcs4 = filter_null(pd.read_csv(summerp))
    lcs = aggregate(lcs1,lcs2)
    lcs = aggregate(lcs, lcs3)
    lcs = aggregate(lcs, lcs4)
    return lcs

def load_data_agg_lck(spring, springp):
    lcs1 = filter_null(pd.read_csv(spring))
    lcs2 = filter_null(pd.read_csv(springp))
    lcs = aggregate(lcs1,lcs2)
    return lcs

def main():

    #configuration section
    player_feature_list = ['result','kp','kda', 'kills', 'deaths','assists', 'firstblood', 'dpm', 'damageshare',  'controlwardsbought', 'visionscore', 'earned gpm', 'earnedgoldshare', 'cspm','csdiffat10', 'xpdiffat10','golddiffat10', 'csdiffat15', 'xpdiffat15', 'golddiffat15' ]
    team_feature_list= ['gamelength', 'result', 'firstdragon', 'dragons', 'firstherald', 'heralds', 'firstbaron', 'firsttower', 'firsttothreetowers' , 'firstmidtower', 'damagetochampions', 'wardsplaced', 'wardskilled', 'controlwardsbought','visionscore', 'csdiffat10', 'golddiffat10', 'csdiffat15', 'xpdiffat15', 'golddiffat15']
    
    # #set data
    match = load_data('2019.csv') 
    lcs = load_data_agg('data/LCS_spring.csv','data/LCS_springp.csv' ,'data/LCS_summer.csv', 'data/LCS_summerp.csv')
    lec = load_data_agg('data/LEC_spring.csv','data/LEC_springp.csv' ,'data/LEC_summer.csv', 'data/LEC_summerp.csv')
    lck = load_data_agg_lck('data/LCK_spring.csv','data/LCK_springp.csv')
    
    # #player data
    # lcs_players = format_df(filter_players(pd.read_csv('data/lcs_players.csv')))
    # lec_players = format_df(filter_players(pd.read_csv('data/lec_players.csv')))
    # lck_players = format_df(filter_players(pd.read_csv('data/lck_players.csv')))
    
    # train_matches = get_matches(match, "LCK")
    # df = make_list(train_matches)
    # df = make_player_data(lck_players, df)
    # df.to_csv("lck_players_rank.csv",encoding='utf-8', index=False)
    
    # train_matches = get_matches(match, "LEC")
    # df = make_list(train_matches)
    # df = make_player_data(lec_players, df)
    # df.to_csv("lec_players_rank.csv",encoding='utf-8', index=False)
    
    # train_matches = get_matches(match, "LCS")
    # df = make_list(train_matches)
    # df = make_player_data(lcs_players, df)
    # df.to_csv("lcs_players_rank.csv",encoding='utf-8', index=False)
    
    
    # #get_matches
    # #champ data
    # train_matches = get_matches(match, "LEC")
    # lec_teams = collect_team_dict(match, 'LEC')
    # lec_teams_correlated = add_correlation_dict(lec_teams, match, "LEC", team_feature_list, player_feature_list, lec)
    # team_dict = lec_teams_correlated 
    
    # df = make_list(train_matches)
    # df_p = make_data(df, team_dict, "performance")
    # df_s = make_data(df, team_dict, "score")
    # df_adj= make_data(df, team_dict, "score_adjusted")
    # df_c= make_data(df, team_dict, "compatibility")
    
    # df_p.to_csv("lec_performance.csv",encoding='utf-8', index=False)
    # df_s.to_csv("lec_score.csv",encoding='utf-8', index=False)
    # df_adj.to_csv("lec_score_adjusted.csv",encoding='utf-8', index=False)
    # df_c.to_csv("lec_compatibility.csv",encoding='utf-8', index=False)
    
    # train_matches = get_matches(match, "LCS")
    # lcs_teams = collect_team_dict(match, 'LCS')
    # lcs_teams_correlated = add_correlation_dict(lcs_teams, match, "LCS", team_feature_list, player_feature_list, lcs)
    # team_dict = lcs_teams_correlated 
    
    # df = make_list(train_matches)
    # df_p = make_data(df, team_dict, "performance")
    # df_s = make_data(df, team_dict, "score")
    # df_adj= make_data(df, team_dict, "score_adjusted")
    # df_c= make_data(df, team_dict, "compatibility")
    
    # df_p.to_csv("lcs_performance.csv",encoding='utf-8', index=False)
    # df_s.to_csv("lcs_score.csv",encoding='utf-8', index=False)
    # df_adj.to_csv("lcs_score_adjusted.csv",encoding='utf-8', index=False)
    # df_c.to_csv("lcs_compatibility.csv",encoding='utf-8', index=False)
    
    # train_matches = get_matches(match, "LCK")
    # lck_teams = collect_team_dict(match, 'LCK')
    # lck_teams_correlated = add_correlation_dict(lck_teams, match, "LCK", team_feature_list, player_feature_list, lck)
    # team_dict = lck_teams_correlated 
    
    # df = make_list(train_matches)
    # df_p = make_data(df, team_dict, "performance")
    # df_s = make_data(df, team_dict, "score")
    # df_adj= make_data(df, team_dict, "score_adjusted")
    # df_c= make_data(df, team_dict, "compatibility")
    
    # df_p.to_csv("lck_performance.csv",encoding='utf-8', index=False)
    # df_s.to_csv("lck_score.csv",encoding='utf-8', index=False)
    # df_adj.to_csv("lck_score_adjusted.csv",encoding='utf-8', index=False)
    # df_c.to_csv("lck_compatibility.csv",encoding='utf-8', index=False)
    
    #filter infinities:https://datascience.stackexchange.com/questions/11928/valueerror-input-contains-nan-infinity-or-a-value-too-large-for-dtypefloat32
    df = pd.read_csv("lcs_compatibility.csv")
    df[df==np.inf]=np.nan
    df.fillna(df.mean(), inplace=True)
    X = df[['red_team','blue_team']]
    #X = df[['red_team','red_top','red_jng', 'red_mid', 'red_bot', 'red_sup' ,'blue_team','blue_top','blue_jng', 'blue_mid', 'blue_bot', 'blue_sup']]
    y = df['result']
    X_train, X_valid, y_train,y_valid = train_test_split(X, y)   
    bayes_model = GaussianNB().fit(X_train,y_train)
    predictions = bayes_model.score(X_valid,y_valid)   
    print(predictions)
    rf_model = RandomForestClassifier().fit(X_train,y_train)
    predictions = rf_model.score(X_valid,y_valid)   
    print(predictions)
    knn_model = KNeighborsClassifier(n_neighbors=10).fit(X_train,y_train)
    predictions = knn_model.score(X_valid,y_valid)   
    print(predictions)
    
    # lck_teams = collect_team_dict(match, 'LEC')
    # lck_teams_correlated = add_correlation_dict(lck_teams, match, "LEC", team_feature_list, player_feature_list, lec)
    # team_dict = lck_teams_correlated  
    
    # f = open("results.txt", "w")
    
    #create diction for teams including team and player correlation data
    # f.write("lck\n")
    # train_matches = get_matches(match, "LCK")
    # lck_teams = collect_team_dict(match, 'LCK')
    # lck_teams_correlated = add_correlation_dict(lck_teams, match, "LCK", team_feature_list, player_feature_list, lck)
    # team_dict = lck_teams_correlated    
    
    #score matches
    # f.write("score_adjusted")
    # team, top, jng, mid, bot, sup = evaluate(train_matches, team_dict, "score_adjusted")
    # f.write(team+"\n")
    # f.write(top+"\n")
    # f.write(jng+"\n")
    # f.write(mid+"\n")
    # f.write(bot+"\n")
    # f.write(sup+"\n")
    # f.write("score\n")
    # team, top, jng, mid, bot, sup = evaluate(train_matches, team_dict, "score")
    # f.write(team+"\n")
    # f.write(top+"\n")
    # f.write(jng+"\n")
    # f.write(mid+"\n")
    # f.write(bot+"\n")
    # f.write(sup+"\n")
    # f.write("compatibility\n")
    # team, top, jng, mid, bot, sup = evaluate(train_matches, team_dict, "compatibility")
    # f.write(team+"\n")
    # f.write(top+"\n")
    # f.write(jng+"\n")
    # f.write(mid+"\n")
    # f.write(bot+"\n")
    # f.write(sup+"\n")
    # f.write("performance\n")
    # team, top, jng, mid, bot, sup = evaluate(train_matches, team_dict, "performance")
    # f.write(team+"\n")
    # f.write(top+"\n")
    # f.write(jng+"\n")
    # f.write(mid+"\n")
    # f.write(bot+"\n")
    # f.write(sup+"\n")
    
    # f.write("lcs\n")
    # train_matches = get_matches(match, "LCS")
    # lcs_teams = collect_team_dict(match, 'LCS')
    # lcs_teams_correlated = add_correlation_dict(lcs_teams, match, "LCS", team_feature_list, player_feature_list, lcs)
    # team_dict = lcs_teams_correlated    

    # #score matches
    # f.write("score_adjusted")
    # team, top, jng, mid, bot, sup = evaluate(train_matches, team_dict, "score_adjusted")
    # f.write(team+"\n")
    # f.write(top+"\n")
    # f.write(jng+"\n")
    # f.write(mid+"\n")
    # f.write(bot+"\n")
    # f.write(sup+"\n")
    # f.write("score\n")
    # team, top, jng, mid, bot, sup = evaluate(train_matches, team_dict, "score")
    # f.write(team+"\n")
    # f.write(top+"\n")
    # f.write(jng+"\n")
    # f.write(mid+"\n")
    # f.write(bot+"\n")
    # f.write(sup+"\n")
    # f.write("compatibility\n")
    # team, top, jng, mid, bot, sup = evaluate(train_matches, team_dict, "compatibility")
    # f.write(team+"\n")
    # f.write(top+"\n")
    # f.write(jng+"\n")
    # f.write(mid+"\n")
    # f.write(bot+"\n")
    # f.write(sup+"\n")
    # f.write("performance\n")
    # team, top, jng, mid, bot, sup = evaluate(train_matches, team_dict, "performance")
    # f.write(team+"\n")
    # f.write(top+"\n")
    # f.write(jng+"\n")
    # f.write(mid+"\n")
    # f.write(bot+"\n")
    # f.write(sup+"\n")
    
    # f.write("lec\n")
    # train_matches = get_matches(match, "LEC")
    # lck_teams = collect_team_dict(match, 'LEC')
    # lck_teams_correlated = add_correlation_dict(lck_teams, match, "LEC", team_feature_list, player_feature_list, lec)
    # team_dict = lck_teams_correlated    
   
   # #score matches   
    # f.write("score_adjusted")
    # team, top, jng, mid, bot, sup = evaluate(train_matches, team_dict, "score_adjusted")
    # f.write(team+"\n")
    # f.write(top+"\n")
    # f.write(jng+"\n")
    # f.write(mid+"\n")
    # f.write(bot+"\n")
    # f.write(sup+"\n")
    # f.write("score\n")
    # team, top, jng, mid, bot, sup = evaluate(train_matches, team_dict, "score")
    # f.write(team+"\n")
    # f.write(top+"\n")
    # f.write(jng+"\n")
    # f.write(mid+"\n")
    # f.write(bot+"\n")
    # f.write(sup+"\n")
    # f.write("compatibility\n")
    # team, top, jng, mid, bot, sup = evaluate(train_matches, team_dict, "compatibility")
    # f.write(team+"\n")
    # f.write(top+"\n")
    # f.write(jng+"\n")
    # f.write(mid+"\n")
    # f.write(bot+"\n")
    # f.write(sup+"\n")
    # f.write("performance\n")
    # team, top, jng, mid, bot, sup = evaluate(train_matches, team_dict, "performance")
    # f.write(team+"\n")
    # f.write(top+"\n")
    # f.write(jng+"\n")
    # f.write(mid+"\n")
    # f.write(bot+"\n")
    # f.write(sup+"\n")
    # f.close()
       
    #create diction for teams including team and player correlation data
    # print("lck")
    # train_matches = get_matches(match, "LCK")
    # lck_teams = collect_team_dict(match, 'LCK')
    # lck_teams_correlated = add_correlation_dict(lck_teams, match, "LCK", team_feature_list, player_feature_list, lck)
    # team_dict = lck_teams_correlated    
    
    # #score matches
    # print ("score_adjusted")
    # evaluate(train_matches, team_dict, "score_adjusted")
    # print ("score")
    # evaluate(train_matches, team_dict, "score")
    # print ("compatibility")
    # evaluate(train_matches, team_dict, "compatibility")
    # print ("performance")
    # unavilable = evaluate(train_matches, team_dict, "performance")
    # if unavilable != 0:
        # print(str(unavilable)+" matches involved champions with insufficient data to analyze")
    
    # print("lcs")
    # train_matches = get_matches(match, "LCS")
    # lcs_teams = collect_team_dict(match, 'LCS')
    # lcs_teams_correlated = add_correlation_dict(lcs_teams, match, "LCS", team_feature_list, player_feature_list, lcs)
    # team_dict = lcs_teams_correlated    

    # #score matches
    # print ("score_adjusted")
    # evaluate(train_matches, team_dict, "score_adjusted")
    # print ("score")
    # evaluate(train_matches, team_dict, "score")
    # print ("compatibility")
    # evaluate(train_matches, team_dict, "compatibility")
    # print ("performance")
    # unavilable = evaluate(train_matches, team_dict, "performance")
    # if unavilable != 0:
        # print(str(unavilable)+" matches involved champions with insufficient data to analyze")

    # print("lec")
    # train_matches = get_matches(match, "LEC")
    # lck_teams = collect_team_dict(match, 'LEC')
    # lck_teams_correlated = add_correlation_dict(lck_teams, match, "LEC", team_feature_list, player_feature_list, lec)
    # team_dict = lck_teams_correlated    
   
   # #score matches   
    # print ("score_adjusted")
    # evaluate(train_matches, team_dict, "score_adjusted")
    # print ("score")
    # evaluate(train_matches, team_dict, "score")
    # print ("compatibility")
    # evaluate(train_matches, team_dict, "compatibility")
    # print ("performance")
    # unavilable = evaluate(train_matches, team_dict, "performance")
    # if unavilable != 0:
        # print(str(unavilable)+" matches involved champions with insufficient data to analyze")      
       
    #player_correlation
    # print(get_score_adjusted(match, "LCS", lcs, "Team Liquid", "bot", player_feature_list))
        
    # red = sb_plot(tsm_mid)
    # red.savefig("test/clg_mid_good.png")
  
    #performance score of a player on a champion
    #print(performance_on_champ(lcs, match, 'Team SoloMid',  'mid', 'Syndra'))
     
    #champion score, adjusted for consistency over games played
    #champion ranking
    # df = champion_score(lcs)
    # print('lcs\n')
    # print(df[['Champion','score','GP','W%', "P+B%"]].sort_values(by=['score'], ascending=False))
    
    #feature correlation by region
    # lcs_correlation_red,  lcs_correlation_blue = feature_correlation_region(match, 'LCS', team_feature_list)
    
    #region correlation 
    # lcs_correlation_red,  lcs_correlation_blue = feature_correlation_region(match, 'LEC', team_feature_list)

    # dif_cor = diff_cor(lcs_correlation_red, lcs_correlation_blue)
    # red = sb_plot(dif_cor)
    # red.savefig("test/blue_red_eu.png")
    # lcs_correlation_red,  lcs_correlation_blue = feature_correlation_region(match, 'LCS', team_feature_list)

    # dif_cor = diff_cor(lcs_correlation_red, lcs_correlation_blue)
    # red = sb_plot(dif_cor)
    # red.savefig("test/blue_red_lcs.png")
    # lcs_correlation_red,  lcs_correlation_blue = feature_correlation_region(match, 'LCK', team_feature_list)

    # dif_cor = diff_cor(lcs_correlation_red, lcs_correlation_blue)
    # red = sb_plot(dif_cor)
    # red.savefig("test/blue_red_lck.png")
    
    # red = sb_plot(lcs_correlation_red)

    # red.savefig("test/lcs_red.png")
    # blue = sb_plot(lcs_correlation_blue)
    # blue.savefig("test/lcs_blue.png")
    
    #team correlation
    # lcs_correlation_red,  lcs_correlation_blue = feature_correlation_team(match, 'Team SoloMid', team_feature_list)
    
    # red = sb_plot(lcs_correlation_red)
    # red.savefig("test/tsm_red.png")
    # blue = sb_plot(lcs_correlation_blue)
    # blue.savefig("test/tsm_blue.png")
    
    # #player correlation by team
    # tsm_correlation = feature_correlation_player(match, 'Counter Logic Gaming', 'mid', player_feature_list)
    # lcs_correlation = feature_correlation_player_region(match, 'LCS', 'mid', player_feature_list)

    # tsm_mid = diff_cor(tsm_correlation, lcs_correlation)
    
if __name__=='__main__':
    main()