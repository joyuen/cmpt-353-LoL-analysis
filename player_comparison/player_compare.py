import numpy as np
import pandas as pd
import math
from scipy import stats
import matplotlib.pyplot as plt
import sys
import seaborn as sb
sb.set()

pd.set_option("display.max_rows", None, "display.max_columns", None, "display.width", 0)

def dominantRegion(df):
    gold = df.sort_values(by=["GD10"], ascending=False).reset_index(drop=True)
    xp = df.sort_values(by=["XPD10"], ascending=False).reset_index(drop=True)
    cs = df.sort_values(by=["CSD10"], ascending=False).reset_index(drop=True)
    winrate = df.sort_values(by=["W%"], ascending=False).reset_index(drop=True)
    kda = df.sort_values(by=["KDA"], ascending=False).reset_index(drop=True)

    gold["rank"] = gold.index
    xp["rank"] = xp.index
    cs["rank"] = cs.index
    winrate["rank"] = winrate.index
    kda["rank"] = kda.index

    gold["rank"] = gold["rank"] + 1 
    xp["rank"] = xp["rank"] + 1 
    cs["rank"] = cs["rank"] + 1 
    winrate["rank"] = winrate["rank"] + 1 
    kda["rank"] = kda["rank"] + 1 

    frames = [gold, xp, cs, winrate, kda]
    res = pd.concat(frames)
    res = res.groupby(["Player", "Pos"], as_index=False).sum() 
    res["rank"] = dresf["rank"] / 5

    # unique players, some players played 2 roles


    #regionRole(res)
    regionBest(res)

def regionBest(df):
    print(df.sort_values(by=["rank"])) 

#def regionRole(df):

    

def main():
    # Questions
    # Dominance (GD10, XPD10, CSD10, W%, KDA)
    # Find where each player ranks in each category, sum ranks and divide by 5 to get overall score
    # 1.a) Most dominant player in each role
    # 1.b) Most dominant player in region
    # 2.a) Most dominant player in each role globally
    # 2.b) Most dominant player globally 


    lck = pd.read_csv('lck_player.csv')
    lec = pd.read_csv('lec_player.csv')
    lcs = pd.read_csv('lcs_player.csv')
    lpl = pd.read_csv('lpl_player.csv')

   

    dominantRegion(lck)
    #dominantRegion(lec)
    #dominantRegion(lcs)
    #dominantRegion(lpl)
    


if __name__ == '__main__':
    main()