from engine import *
import csv

#data loading and filtering
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
    #configuration section to choose which features from the data we wish to look at(data indexes were not named consistently from champion to player to match files so altering configurations features may require manual intervention in the engine, recomended to not alter)
    player_feature_list = ['result','kp','kda', 'kills', 'deaths','assists', 'firstblood', 'dpm', 'damageshare',  'controlwardsbought', 'visionscore', 'earned gpm', 'earnedgoldshare', 'cspm','csdiffat10', 'xpdiffat10','golddiffat10', 'csdiffat15', 'xpdiffat15', 'golddiffat15' ]
    team_feature_list= ['gamelength', 'result', 'firstdragon', 'dragons', 'firstherald', 'heralds', 'firstbaron', 'firsttower', 'firsttothreetowers' , 'firstmidtower', 'damagetochampions', 'wardsplaced', 'wardskilled', 'controlwardsbought','visionscore', 'csdiffat10', 'golddiffat10', 'csdiffat15', 'xpdiffat15', 'golddiffat15']
    
    #set match and champion data
    #lpl data for 2019 was largely missing and was not used
    #only the first half of the lck data was taken as they play more games in the first half than the other regions in the entire year
    match = load_data('2019.csv') 
    lcs = load_data_agg('data/LCS_spring.csv','data/LCS_springp.csv' ,'data/LCS_summer.csv', 'data/LCS_summerp.csv')
    lec = load_data_agg('data/LEC_spring.csv','data/LEC_springp.csv' ,'data/LEC_summer.csv', 'data/LEC_summerp.csv')
    lck = load_data_agg_lck('data/LCK_spring.csv','data/LCK_springp.csv')
    
    #player data
    lcs_players = format_df(filter_players(pd.read_csv('data/lcs_players.csv')))
    lec_players = format_df(filter_players(pd.read_csv('data/lec_players.csv')))
    lck_players = format_df(filter_players(pd.read_csv('data/lck_players.csv')))


#feature correlation for all teams by region, includes seperate map sides
#example usage shown below outputs sb correlation plots for the differences between each region on red side
#def feature_correlation_region(matches, region, feature_list):
#####################################################################################################################

    #ex.
    # lcs_correlation_red,  lcs_correlation_blue = feature_correlation_region(match, 'LCS', team_feature_list)
    # eu_correlation_red,  eu_correlation_blue = feature_correlation_region(match, 'LEC', team_feature_list)
    # kr_correlation_red,  kr_correlation_blue = feature_correlation_region(match, 'LCK', team_feature_list)
    
    # dif_cor = diff_cor(eu_correlation_red, kr_correlation_red)
    # red = sb_plot(dif_cor)
    # red.savefig("data_output/kr_eu_red.png")

    # dif_cor = diff_cor(lcs_correlation_red, kr_correlation_red)
    # red = sb_plot(dif_cor)
    # red.savefig("data_output/na_kr_red.png")
    
    # dif_cor = diff_cor(lcs_correlation_red, eu_correlation_red)
    # red = sb_plot(dif_cor)
    # red.savefig("data_output/na_eu_red.png")
    
#feature correlation by team in a region, mainly used for computations in complex functions
#def feature_correlation_team(matches, team, feature_list):
#####################################################################################################################

    #ex.
    # lcs_correlation_red,  lcs_correlation_blue = feature_correlation_team(match, 'Team SoloMid', team_feature_list)
    # red = sb_plot(lcs_correlation_red)
    # red.savefig("data_output/tsm_red.png")
    # blue = sb_plot(lcs_correlation_blue)
    # blue.savefig("data_output/tsm_blue.png")

#Pearson correlation for a single player indexing by their team and region using data from matches file to correlate ALL features from player_feature_list
#def feature_correlation_player(matches, team, position, feature_list):
#####################################################################################################################         
    #ex.
    # clg_bot = feature_correlation_player(match, 'Counter Logic Gaming', 'bot', player_feature_list)
    # clg = sb_plot(clg_bot)
    # clg.savefig("data_output/clg_bot.png")
 
#feature correlation for player by team, mainly used for computations in larger functions when comparing players, can use version incluing sides by uncommenting in engine. not recommended without a ton of data.
#also feature correlation for all players in that region by team to better compare a players playstyle
#def feature_correlation_player(matches, team, position, feature_list):
#def feature_correlation_player_region(matches, region, position, feature_list):
#####################################################################################################################

    #ex.
    # clg_correlation = feature_correlation_player(match, 'Counter Logic Gaming', 'mid', player_feature_list)
    # lcs_correlation = feature_correlation_player_region(match, 'LCS', 'mid', player_feature_list)   
    # dif_cor = diff_cor(clg_correlation, lcs_correlation)
    # clg = sb_plot(dif_cor)
    # clg.savefig("data_output/clg_avg_mid.png") 
    
#requres above player dif_cor
#get champ compat dataframe based on position, players_correlation, champion data dataframe, team, and match csv
#correlation data for a player versus the average in that position is used to find the champion who is most similar
#most similar is taken as the champion whose proportions differ the least from the average champion in that pool
#they are scored based on how similar for a maximum score of 10
#def champ_compat(position, player_cor, champ_data, team, matches):
#####################################################################################################################
    
    # print(champ_compat("mid", dif_cor, lcs, 'Counter Logic Gaming', match))   
 

#get performance score of a player on a champion by region, team, position, and champion name
#####################################################################################################################
    # print(performance_on_champ(lcs, match, 'Team SoloMid',  'mid', 'Syndra'))
     
#champion score, or champion meta score by region, scores champions in general based on winrate, games played, and pick ban presence 
#champion_score(champ_data_region):
#champion ranking
#####################################################################################################################
    #ex. 
    # df = champion_score(lcs)
    # print('lcs\n')
    # print(df[['Champion','score','GP','W%', "P+B%"]].sort_values(by=['score'], ascending=False))
    

#get score adjusted, an aggregation of the scores from the three other measurements created(champion_score, performance, compatibility), min scsore is 10
#def get_score_adjusted(match, region, champ_data,team, position, player_feature_list):
#####################################################################################################################
    #for team liquid bot player
    #ex.
    # print(get_score_adjusted(match, "LCS", lcs, "Team Liquid", "bot", player_feature_list)) 
   

#Warning, the following functions create large datastructures and take time to run
#Create dictionary of teams from a region include ALL correlation data for the teams and players in that region, uses all above functions
#general sense
#{Team}{players position}
#      {correlation for position}
#      {correlation for team}
#      {champion score dataframe(compatibility,performance, champion_score, score adjusted)}
#please print and observe data structure for usage 
#print of manual prediction of matches included underneath each dictionary creation
######################################################################################################################
    # ex. 
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
    # print("score_adjusted")
    # evaluate(train_matches, team_dict, "score_adjusted")
    # print("score")
    # evaluate(train_matches, team_dict, "score")
    # print("compatibility")
    # evaluate(train_matches, team_dict, "compatibility")
    # print("performance")
    # unavilable = evaluate(train_matches, team_dict, "performance")
    # if unavilable != 0:
        # print(str(unavilable)+" matches involved champions with insufficient data to analyze")      
    
    
#Create csv data for ml folder, requires aggregation of many previous parts  
######################################################################################################################
    #load and format data 
    
    # train_matches = get_matches(match, "LCK")
    # df = make_list(train_matches)
    # df = make_player_data(lck_players, df)
    # df.to_csv("data_output/lck_players_rank.csv",encoding='utf-8', index=False)
    
    # train_matches = get_matches(match, "LEC")
    # df = make_list(train_matches)
    # df = make_player_data(lec_players, df)
    # df.to_csv("data_output/lec_players_rank.csv",encoding='utf-8', index=False)
    
    # train_matches = get_matches(match, "LCS")
    # df = make_list(train_matches)
    # df = make_player_data(lcs_players, df)
    # df.to_csv("data_output/lcs_players_rank.csv",encoding='utf-8', index=False)
    
    # #get matches 
    
    # #champ data
    # train_matches = get_matches(match, "LEC")
    # lec_teams = collect_team_dict(match, 'LEC')
    # lec_teams_correlated = add_correlation_dict(lec_teams, match, "LEC", team_feature_list, player_feature_list, lec)
    # team_dict = lec_teams_correlated 
    
    # #create csv's for each region, did not functionalize this step
    
    # df = make_list(train_matches)
    # df_p = make_data(df, team_dict, "performance")
    # df_s = make_data(df, team_dict, "score")
    # df_adj= make_data(df, team_dict, "score_adjusted")
    # df_c= make_data(df, team_dict, "compatibility")
    
    # df_p.to_csv("data_output/lec_performance.csv",encoding='utf-8', index=False)
    # df_s.to_csv("data_output/lec_score.csv",encoding='utf-8', index=False)
    # df_adj.to_csv("data_output/lec_score_adjusted.csv",encoding='utf-8', index=False)
    # df_c.to_csv("data_output/lec_compatibility.csv",encoding='utf-8', index=False)
    
    # train_matches = get_matches(match, "LCS")
    # lcs_teams = collect_team_dict(match, 'LCS')
    # lcs_teams_correlated = add_correlation_dict(lcs_teams, match, "LCS", team_feature_list, player_feature_list, lcs)
    # team_dict = lcs_teams_correlated 
    
    # df = make_list(train_matches)
    # df_p = make_data(df, team_dict, "performance")
    # df_s = make_data(df, team_dict, "score")
    # df_adj= make_data(df, team_dict, "score_adjusted")
    # df_c= make_data(df, team_dict, "compatibility")
    
    # df_p.to_csv("data_output/lcs_performance.csv",encoding='utf-8', index=False)
    # df_s.to_csv("data_output/lcs_score.csv",encoding='utf-8', index=False)
    # df_adj.to_csv("data_output/lcs_score_adjusted.csv",encoding='utf-8', index=False)
    # df_c.to_csv("data_output/lcs_compatibility.csv",encoding='utf-8', index=False)
    
    # train_matches = get_matches(match, "LCK")
    # lck_teams = collect_team_dict(match, 'LCK')
    # lck_teams_correlated = add_correlation_dict(lck_teams, match, "LCK", team_feature_list, player_feature_list, lck)
    # team_dict = lck_teams_correlated 
    
    # df = make_list(train_matches)
    # df_p = make_data(df, team_dict, "performance")
    # df_s = make_data(df, team_dict, "score")
    # df_adj= make_data(df, team_dict, "score_adjusted")
    # df_c= make_data(df, team_dict, "compatibility")
    
    # df_p.to_csv("data_output/lck_performance.csv",encoding='utf-8', index=False)
    # df_s.to_csv("data_output/lck_score.csv",encoding='utf-8', index=False)
    # df_adj.to_csv("data_output/lck_score_adjusted.csv",encoding='utf-8', index=False)
    # df_c.to_csv("data_output/lck_compatibility.csv",encoding='utf-8', index=False)
    
#Create data and manually score data, output in a "results.txt" file(achieved roughly the same scores as the ml folder)   
#also create csvs for ml results analysis 
#metrics for score are team wide(sum of all positions), or positional, just that position. 
######################################################################################################################    
    
    # f = open("data_output/results.txt", "w")
    
    # #create diction for teams including team and player correlation data
    # f.write("lck\n")
    # train_matches = get_matches(match, "LCK")
    # df = make_data_team(make_list(train_matches))
    # df.to_csv("data_output/lck_matches.csv",encoding='utf-8', index=False)
    # lck_teams = collect_team_dict(match, 'LCK')
    # lck_teams_correlated = add_correlation_dict(lck_teams, match, "LCK", team_feature_list, player_feature_list, lck)
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
    
    #f.write("lcs\n")
    # train_matches = get_matches(match, "LCS")
    # df = make_data_team(make_list(train_matches))
    # df.to_csv("data_output/lcs_matches.csv",encoding='utf-8', index=False)
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
    # df = make_data_team(make_list(train_matches))
    # df.to_csv("data_output/lec_matches.csv",encoding='utf-8', index=False)
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
 
if __name__=='__main__':
    main()