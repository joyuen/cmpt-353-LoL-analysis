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
    return df

def top_five_banned(df, league):
    new_df = df[['Champion', 'B%']].copy()
    # convert str of percentage to float
    # https://stackoverflow.com/questions/50686004/change-column-with-string-of-percent-to-float-pandas-dataframe/50686042
    new_df['B_float'] = new_df['B%'].str.rstrip('%').astype('float') / 100.0
    new_df = new_df.groupby(by=['Champion']).mean()
    print(league, 'top five banned champs:')
    print(new_df.nlargest(5, 'B_float'))

# relationship between wards per muinute and games won for teams
def ward_win_relationship(df, league):
    new_df = df[['W', 'WPM']].copy()
    new_df['W_int'] = new_df['W'].astype('int')
    new_df['WPM_float'] = new_df['WPM'].astype('float')
    # fit line
    fit = stats.linregress(new_df['WPM_float'], new_df['W_int'])
    new_df['prediction'] = new_df['WPM_float']*fit.slope + fit.intercept
    print('\n')
    print(league, 'ward_win_relationship:')
    print('The slope is', fit.slope)
    print('The p-value is', fit.pvalue, '\n')
    # scatter plot of the data
    plt.figure()
    plt.plot(new_df['WPM_float'], new_df['W_int'], 'b.', alpha=0.5)
    # plot the best-fit line
    plt.plot(new_df['WPM_float'], new_df['prediction'], 'r-', linewidth=3)
    plt.title('Ward Placed per Minute and Games Won Relationship')
    plt.legend(['Actual Data', 'Fit Line'])
    plt.xlabel('Ward Placed per Minute')
    plt.ylabel('Games Won')
    plt.savefig(league + '_ward_win_relationship.png')

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

# common banned champs in all 4 leagues are 'Aphelios', 'Sett', 'Ornn' ,'LeBlanc' and 'Senna'
top_five_banned(lck_champ_data, 'lck')
top_five_banned(lec_champ_data, 'lec')
top_five_banned(lcs_champ_data, 'lcs')
top_five_banned(lpl_champ_data, 'lpl')

# we can combine all team data into one file to find the overall effect of wpm on games won
# ward_win_relationship(lck_team_data, 'lck')
# ward_win_relationship(lec_team_data, 'lec')
# ward_win_relationship(lcs_team_data, 'lcs')
# ward_win_relationship(lpl_team_data, 'lpl')

all_team_data = pd.concat([lck_team_data, lec_team_data, lcs_team_data, lpl_team_data])
ward_win_relationship(all_team_data, 'all_team')