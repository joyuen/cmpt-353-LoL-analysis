import sys 
import math
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn
seaborn.set()

def filter_null(df):
    df = df[~df['W%'].str.contains('-')]
    # at least 5 games played is needed
    df = df[df['GP'] >=5 ]
    return df

def top_five_banned(df, region):
    new_df = df[['Champion', 'B%']].copy()
    # convert str of percentage to float
    # https://stackoverflow.com/questions/50686004/change-column-with-string-of-percent-to-float-pandas-dataframe/50686042
    new_df['B_float'] = new_df['B%'].str.rstrip('%').astype('float') / 100.0
    new_df = new_df.groupby(by=['Champion']).mean()
    print(region, 'top five banned champs:')
    print(new_df.nlargest(5, 'B_float'))

def top_five_win(df, region):
    new_df = df[['Champion', 'W%']].copy()
    # convert str of percentage to float
    # https://stackoverflow.com/questions/50686004/change-column-with-string-of-percent-to-float-pandas-dataframe/50686042
    new_df['W_float'] = new_df['W%'].str.rstrip('%').astype('float') / 100.0
    new_df = new_df.groupby(by=['Champion']).mean()
    print(region, 'top five win rate champs:')
    print(new_df.nlargest(5, 'W_float'))

# relationship between wards per muinute and games won for teams
def find_relationship(df, var1, var2, var1_type, var2_type, title, xlab, ylab, image):
    new_df = df[[var1, var2]].copy()
    if var1_type == 'percent':
        new_df['var1_convert'] = new_df[var1].str.rstrip('%').astype('float') / 100.0
    else:
        new_df['var1_convert'] = new_df[var1].astype(var1_type)
    if var2_type == 'percent':
        new_df['var2_convert'] = new_df[var2].str.rstrip('%').astype('float') / 100.0
    else:
        new_df['var2_convert'] = new_df[var2].astype(var2_type)
    # fit line
    fit = stats.linregress(new_df['var1_convert'], new_df['var2_convert'])
    new_df['prediction'] = new_df['var1_convert']*fit.slope + fit.intercept
    print(title, ':')
    print('The slope is', fit.slope)
    print('The p-value is', fit.pvalue, '\n')
    # scatter plot of the data
    plt.figure()
    plt.plot(new_df['var1_convert'], new_df['var2_convert'], 'b.', alpha=0.5)
    # plot the best-fit line
    plt.plot(new_df['var1_convert'], new_df['prediction'], 'r-', linewidth=3)
    plt.title(title)
    plt.legend(['Actual Data', 'Fit Line'])
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.savefig(image + '.png')

# champ data
lck_champ_data = filter_null(pd.read_csv('LCK_champ.csv'))
lec_champ_data = filter_null(pd.read_csv('LEC_champ.csv'))
lcs_champ_data = filter_null(pd.read_csv('LCS_champ.csv'))
lpl_champ_data = filter_null(pd.read_csv('LPL_champ.csv'))

# team data
lck_team_data = pd.read_csv('LCK_team.csv')
lec_team_data = pd.read_csv('LEC_team.csv')
lcs_team_data = pd.read_csv('LCS_team.csv')
lpl_team_data = pd.read_csv('LPL_team.csv')

# common banned champs in all 4 regions are 'Aphelios', 'Sett', 'Ornn' ,'LeBlanc' and 'Senna'
top_five_banned(lck_champ_data, 'lck')
top_five_banned(lec_champ_data, 'lec')
top_five_banned(lcs_champ_data, 'lcs')
top_five_banned(lpl_champ_data, 'lpl')

top_five_win(lck_champ_data, 'lck')
top_five_win(lec_champ_data, 'lec')
top_five_win(lcs_champ_data, 'lcs')
top_five_win(lpl_champ_data, 'lpl')

# we can combine all team data into one file to find the overall effect of wpm on games won
all_team_data = pd.concat([lck_team_data, lec_team_data, lcs_team_data, lpl_team_data])
# slope is greater than 0 means positive relationship, and p-value is small enough to reject null at alpha = 0.05
find_relationship(all_team_data, 'WPM', 'W', 'float', 'int', 'Wards Placed and Games Won Relationship', 'Wards Placed per Minute', 'Games Won', 'ward_place_win_relationship')

find_relationship(all_team_data, 'WCPM', 'W', 'float', 'int', 'Wards Cleared and Games Won Relationship', 'Wards Cleared per Minute', 'Games Won', 'ward_clear_win_relationship')

find_relationship(all_team_data, 'DRG%', 'W', 'percent', 'int', 'Dragon Control and Games Won Relationship', 'Dragon Control Rate', 'Games Won', 'dragon_control_win_relationship')

find_relationship(all_team_data, 'BN%', 'W', 'percent', 'int', 'Baron Control and Games Won Relationship', 'Baron Control Rate', 'Games Won', 'baron_control_win_relationship')

find_relationship(all_team_data, 'JNG%', 'W', 'percent', 'int', 'Jungle Control and Games Won Relationship', 'Jungle Control Rate', 'Games Won', 'jungle_control_win_relationship')

find_relationship(all_team_data, 'K', 'W', 'int', 'int', 'Kills and Games Won Relationship', 'Kills', 'Games Won', 'kills_win_relationship')
# no significance in this one
find_relationship(all_team_data, 'FB%', 'W', 'percent', 'int', 'First Blood Rate and Games Won Relationship', 'First Blood Rate', 'Games Won', 'first_blood_win_relationship')

find_relationship(all_team_data, 'FT%', 'W', 'percent', 'int', 'First Tower Rate and Games Won Relationship', 'First Tower Rate', 'Games Won', 'first_tower_win_relationship')