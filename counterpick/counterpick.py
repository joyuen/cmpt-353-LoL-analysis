import numpy as np
import pandas as pd
import math
from scipy import stats
import matplotlib.pyplot as plt
import sys
import seaborn as sb
sb.set()

pd.set_option("display.max_rows", None, "display.max_columns", None, "display.width", 0)


def filter_null(df):
    df = df[~df['W%'].str.contains('-')]
    df = df[~df['CTR%'].str.contains('0%')]
    df = df[df['GP'] >= 10]
    return df
    
def percent_to_float(x):
    return float(x.strip("%"))/100
   
   
def format_df(df):
    df["string"] = df["Champion"] + " " + df["Pos"]
    df["W%"] = df["W%"].apply(lambda x: percent_to_float(x))
    df["CTR%"] = df["CTR%"].apply(lambda x: percent_to_float(x))
    df["GPasCTR"] = round(df["GP"] * df["CTR%"])
      
    return df[["Champion", "Pos", "string", "GP", "GPasCTR", "W%", "CTR%"]].sort_values(by=["GPasCTR", "W%"], ascending=False) 


def global_pick(lck, lec, lcs, lpl):
    temp_lck = lck[lck["CTR%"] >= 0.75]
    temp_lec = lec[lec["CTR%"] >= 0.75]
    temp_lcs = lcs[lcs["CTR%"] >= 0.75]
    temp_lpl = lpl[lpl["CTR%"] >= 0.75]

    globalChamps = set(temp_lck.string) & set(temp_lec.string) & set(temp_lcs.string) & set(temp_lpl.string)
    #print(globalChamps)

def most_played(lck, lec, lcs, lpl):
    globalChamps = set(lck.string) & set(lec.string) & set(lcs.string) & set(lpl.string)

    print("Top 5 LCK Counter Pick Champions")
    print(lck.sort_values(by=["GPasCTR"], ascending=False).head())
    print("\n")
    print("Top 5 LEC Counter Pick Champions")
    print(lec.sort_values(by=["GPasCTR"], ascending=False).head())
    print("\n")
    print("Top 5 LCS Counter Pick Champions")
    print(lcs.sort_values(by=["GPasCTR"], ascending=False).head())
    print("\n")
    print("Top 5 LPL Counter Pick Champions")
    print(lpl.sort_values(by=["GPasCTR"], ascending=False).head())  
    print("\n")
    
    frames = [lck, lec, lcs, lpl]
    res = pd.concat(frames)
    res = res.groupby(["Champion", "Pos", "string"], as_index=False).mean()
    res = res[res["string"].isin(globalChamps)]

    print("Most Played Counter Pick Champions in all 4 regions")
    print(res.sort_values(by=["GPasCTR"], ascending=False))

def counterpick_winrate(df, league):
    new_df = df.copy()

    new_df["CTR%"] = new_df["CTR%"] * 100
    new_df["W%"] = new_df["W%"] * 100

    fit = stats.linregress(new_df["CTR%"], new_df["W%"])
    new_df["prediction"] = new_df["CTR%"] * fit.slope + fit.intercept

    plt.figure(figsize=(10, 5))
    plt.plot(new_df["CTR%"], new_df["W%"], 'b.', alpha=0.5)
    plt.title("Relationship between Counter Pick Rate and Win Rate")
    plt.xlabel("Counter Pick Percentage")
    plt.ylabel("Win Rate Percentage")
    plt.plot(new_df['CTR%'], new_df['prediction'], 'r-', linewidth=3)
    plt.legend(['Actual Data', 'Fit Line'])
    plt.savefig(league + "_counterpick_winrate.png")

    
def main():
    # Questions
    # 1) Any counter picks that showed up in all regions?
    # 2) most played counterpick for each region
    # 3) most played counterpick globally
    # 4) Relationship between counter pick % and win rate %

    lck = filter_null(pd.read_csv('LCK.csv'))
    lec = filter_null(pd.read_csv('LEC.csv'))
    lcs = filter_null(pd.read_csv('LCS.csv'))
    lpl = filter_null(pd.read_csv('LPL.csv'))
    
    lck = format_df(lck)
    lec = format_df(lec)
    lcs = format_df(lcs)
    lpl = format_df(lpl)

    # 1) Finds counter pick champions that appear in all four 
    # There are no counter pick champions that are played in all four major regions
    global_pick(lck, lec, lcs, lpl)
    
    # 2) top 5 most played counter pick for each region
    # 3) most played counter pick champion globally
    most_played(lck, lec, lcs, lpl)

    # 4)
    counterpick_winrate(lpl, "lpl")
    counterpick_winrate(lck, "lck")
    counterpick_winrate(lec, "lec")
    counterpick_winrate(lcs, "lcs")

if __name__ == '__main__':
    main()