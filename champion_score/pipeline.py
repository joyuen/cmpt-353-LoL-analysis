from engine import *


def load_data(lck, lec, lcs, lpl, matches):
    lck = filter_null(pd.read_csv('data/LCK.csv'))
    lec = filter_null(pd.read_csv('data/LEC.csv'))
    lcs = filter_null(pd.read_csv('data/LCS.csv'))
    lpl = filter_null(pd.read_csv('data/LPL.csv'))
    matches = pd.read_csv('data/2019.csv')
    matches = pre_process(matches)
    return lck, lec, lcs, lpl, matches


def main():

    #configuration section
    player_feature_list = ['result','kp','kda', 'kills', 'deaths','assists', 'firstblood', 'dpm', 'damageshare',  'controlwardsbought', 'visionscore', 'earned gpm', 'earnedgoldshare', 'cspm','csdiffat10', 'xpdiffat10','golddiffat10', 'csdiffat15', 'xpdiffat15', 'golddiffat15' ]
    team_feature_list= ['gamelength', 'result', 'firstdragon', 'dragons', 'firstherald', 'heralds', 'firstbaron', 'firsttower', 'firsttothreetowers' , 'firstmidtower', 'damagetochampions', 'wardsplaced', 'wardskilled', 'controlwardsbought','visionscore', 'csdiffat10', 'golddiffat10', 'csdiffat15', 'xpdiffat15', 'golddiffat15']
    lck, lec, lcs, lpl, match = load_data('LCK.csv', 'LEC.csv', 'LCS.csv', 'LPL.csv', '2019.csv')

    
    
    #create diction for teams including team and player correlation data
    lcs_teams = collect_team_dict(match, 'LCS')
    lcs_teams_correlated = add_correlation_dict(lcs_teams, match, "LCS", team_feature_list, player_feature_list)    

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
       
    # red = sb_plot(tsm_mid)
    # red.savefig("test/clg_mid_good.png")

    
    #performance score of a player on a champion
    # print(performance_on_champ(lcs, match, 'Team SoloMid',  'mid','Syndra'))
     
    #champion score, adjusted for consistency over games played
    #champion ranking
    # df = champion_score(lcs)
    # print('lcs\n')
    # print(df[['Champion','score','GP','W%']].sort_values(by=['score'], ascending=False))

    
    # lcs_correlation_red,  lcs_correlation_blue = feature_correlation_region(match, 'LCS', team_feature_list)
    
if __name__=='__main__':
    main()