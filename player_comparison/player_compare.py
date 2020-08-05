import numpy as np
import pandas as pd
import math
from scipy import stats
import matplotlib.pyplot as plt
import sys
import seaborn as sb
sb.set()

pd.set_option("display.max_rows", None, "display.max_columns", None, "display.width", 0)

def filter_players(df):
    df = df[df["GP"] >= 10] # minimum of 10 professional games to be considered
    return df

def percent_to_float(x):
    return float(x.strip("%"))/100

def format_df(df):
    df["W%"] = df["W%"].apply(lambda x: percent_to_float(x))
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

def dominantGlobal(lck, lec, lcs, lpl):
    frames = [lck, lec, lcs, lpl]
    res = pd.concat(frames)
    

    # ties were given to players that played more games

    gold = res.sort_values(by=["GD10", "GP"], ascending=False).reset_index(drop=True)
    xp = res.sort_values(by=["XPD10", "GP"], ascending=False).reset_index(drop=True)
    cs = res.sort_values(by=["CSD10", "GP"], ascending=False).reset_index(drop=True)
    winrate = res.sort_values(by=["W%", "GP"], ascending=False).reset_index(drop=True)
    kda = res.sort_values(by=["KDA", "GP"], ascending=False).reset_index(drop=True)

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
    completeData = pd.concat(frames)
    completeData = fix_stats(completeData)
    completeData = completeData.groupby(["Player", "Pos"], as_index=False).sum() 
    
    completeData["rank"] = completeData["goldrank"] * 0.3 + completeData["xprank"] * 0.3 + completeData["csrank"] * 0.3 + completeData["wrrank"] * 0.05 + completeData["kdarank"] * 0.05   

    globalBest(completeData)
    globalRole(completeData)

def globalBest(df):
    df = df.sort_values(by=["rank"]).reset_index()
    df["rank"] = df.index + 1

    print("Top 5 most dominant players in the 4 regions:")
    print(df.head()) 
    print("\n")

def globalRole(df):
    df = df.sort_values(by=["rank"]).reset_index()
    df = df.drop_duplicates(subset="Pos")
    df["rank"] = df.index + 1
    print("Most dominant player in the 4 regions for each position:")
    print(df) 
    print("\n")


def dominantRegion(df, league):
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
    res = res.groupby(["Player", "Pos"], as_index=False).sum() 

    res["rank"] = res["goldrank"] * 0.3 + res["xprank"] * 0.3 + res["csrank"] * 0.3 + res["wrrank"] * 0.05 + res["kdarank"] * 0.05   

    regionBest(res, league)
    regionRole(res, league)

def regionBest(df, league):
    df = df.sort_values(by=["rank"]).reset_index()
    df["rank"] = df.index + 1

    print("Top 5 most dominant players in {}:".format(league))
    print(df.head()) 
    print("\n")

def regionRole(df, league):
    df = df.sort_values(by=["rank"]).reset_index()
    df = df.drop_duplicates(subset="Pos")
    df["rank"] = df.index + 1
    print("Most dominant player in {} for each position:".format(league))
    print(df) 
    print("\n")
    

def main():
    # Questions:
    # Dominance (GD10, XPD10, CSD10, W%, KDA)
    # Find where each player ranks in each category then use weighted average to determine overall rank
    # Weighted average favours in lane superiority over total winrate and KDA
    # 1.a) Most dominant player in each role
    # 1.b) Most dominant player in region
    # 2.a) Most dominant player in each role globally
    # 2.b) Most dominant player globally 


    lck = filter_players(pd.read_csv('lck_player.csv'))
    lec = filter_players(pd.read_csv('lec_player.csv'))
    lcs = filter_players(pd.read_csv('lcs_player.csv'))
    lpl = filter_players(pd.read_csv('lpl_player.csv'))

    lck = format_df(lck)
    lec = format_df(lec)
    lcs = format_df(lcs)
    lpl = format_df(lpl)

    dominantRegion(lck, "LCK")
    dominantRegion(lec, "LEC")
    dominantRegion(lcs, "LCS")
    dominantRegion(lpl, "LPL")

    dominantGlobal(lck, lec, lcs, lpl)
    
if __name__ == '__main__':
    main()