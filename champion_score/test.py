import sys 
import math
import pandas as pd
import numpy as np

def filter_null(df):
    df = df[~df['W%'].str.contains('-')]
    return df

#score champion by region currently only games-winrate adjusted
def champion_score(region):
    total = math.floor((int(region['GP'].iloc[0])/float((region['P%'].iloc[0]).replace('%',''))*100))
    region['score'] = region.apply(lambda x : gp_adjust(total,x['GP'], x['W%']), axis = 1)
    return region


#Games/winrate bias
def gp_adjust(t, g, w):
    # print(w)
    # return(w)
    if float(w.replace('%','')) - 50 > 0:
        w = float(w.replace('%','')) - 50
    else:
        w = 1
        
    return (w * int(g))/t

#Presence bias?
def p_bias(s, pb):
    return
#Single Counter pick bias

#Single ally bias

#Aggregated ..

# total matches?
def main():
    lck = filter_null(pd.read_csv('LCK.csv'))
    lec = filter_null(pd.read_csv('LEC.csv'))
    lcs = filter_null(pd.read_csv('LCS.csv'))
    lpl = filter_null(pd.read_csv('LPL.csv'))
    match = pd.read_csv('2019.csv')
    
    #champion ranking
    df = champion_score(lcs)
    print('lcs\n')
    print(df[['Champion','score','GP','W%']].sort_values(by=['score'], ascending=False))
    df = champion_score(lec)
    print('lec\n')
    print(df[['Champion','score','GP','W%']].sort_values(by=['score'], ascending=False))
    df = champion_score(lck)
    print('lck\n')
    print(df[['Champion','score','GP','W%']].sort_values(by=['score'], ascending=False))
    df = champion_score(lpl)
    print('lpl\n')
    print(df[['Champion','score','GP','W%']].sort_values(by=['score'], ascending=False))

if __name__=='__main__':
    main()