from engine import *


def load_data(lck, lec, lcs, lpl, matches):
    lck = filter_null(pd.read_csv('data/LCK.csv'))
    lec = filter_null(pd.read_csv('data/LEC.csv'))
    lcs = filter_null(pd.read_csv('data/LCS.csv'))
    lpl = filter_null(pd.read_csv('data/LPL.csv'))
    matches = pd.read_csv('data/2019.csv')
    return lck, lec, lcs, lpl, matches


def main():

    #configuration section
    player_feature_list = ['side', 'result','kills', 'deaths','assists', 'firstblood', 'dpm', 'damageshare',  'controlwardsbought', 'visionscore', 'earned gpm', 'earnedgoldshare', 'cspm','csdiffat10', 'xpdiffat10','golddiffat10', 'csdiffat15', 'xpdiffat15', 'golddiffat15' ]
    team_feature_list= ['gamelength', 'result', 'firstdragon', 'dragons', 'firstherald', 'heralds', 'firstbaron', 'firsttower', 'firsttothreetowers' , 'firstmidtower', 'damagetochampions', 'wardsplaced', 'wardskilled', 'controlwardsbought','visionscore', 'csdiffat10', 'golddiffat10', 'csdiffat15', 'xpdiffat15', 'golddiffat15']
    lck, lec, lcs, lpl, match = load_data('LCK.csv', 'LEC.csv', 'LCS.csv', 'LPL.csv', '2019.csv')

    lcs_teams_correlated = add_correlation(collect_team_dict(match, 'LCS'), match, "LCS", team_feature_list, player_feature_list)    
        
    # lcs_correlation_red,  lcs_correlation_blue = feature_correlation_region(match, 'LCS', team_feature_list)
    
    # red = sb_plot(lcs_correlation_red)
    # red.savefig("test/lcs_red.png")
    # blue = sb_plot(lcs_correlation_blue)
    # blue.savefig("test/lcs_blue.png")
    
    # lcs_correlation_red,  lcs_correlation_blue = feature_correlation_team(match, 'Team SoloMid', team_feature_list)
    
    # red = sb_plot(lcs_correlation_red)
    # red.savefig("test/tsm_red.png")
    # blue = sb_plot(lcs_correlation_blue)
    # blue.savefig("test/tsm_blue.png")
    
    
    # lcs_correlation_red,  lcs_correlation_blue = feature_correlation_player(match, 'Team SoloMid', 'mid', player_feature_list)
    
    # red = sb_plot(lcs_correlation_red)
    # red.savefig("test/tsm_mid_red.png")
    # blue = sb_plot(lcs_correlation_blue)
    # blue.savefig("test/tsm_mid_blue.png") 
    
    
    # print(performance_on_champ(lcs, match, 'Team SoloMid',  'mid','Syndra'))
       
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