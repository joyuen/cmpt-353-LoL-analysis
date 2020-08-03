import numpy as np
import pandas as pd
import math
from scipy import stats
import matplotlib.pyplot as plt
import sys
import seaborn as sb

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
    #df["GW"] = df["W%"] * df["GP"]
      
    return df[["Champion", "Pos", "string", "GP", "GPasCTR", "W%", "CTR%"]].sort_values(by=["GPasCTR", "W%"], ascending=False) 
    
def main():
    # Questions
    # 1) Any counter picks that showed up in all regions?
    # 2) most successful/played counterpick for each region
    # 3) most successful/played counterpick globally
    # 4) does counterpicking result in increased winrates

    lck = filter_null(pd.read_csv('LCK.csv'))
    lec = filter_null(pd.read_csv('LEC.csv'))
    lcs = filter_null(pd.read_csv('LCS.csv'))
    lpl = filter_null(pd.read_csv('LPL.csv'))
    
    lck = format_df(lck)
    lec = format_df(lec)
    lcs = format_df(lcs)
    lpl = format_df(lpl)
    
    # n = 66 
    #print(lck)   

    # n = 41
    #print(lec)
    
    # n = 36
    #print(lcs)
    
    # n = 64
    #print(lpl)

        
    # 1) Finds counter pick champions that appear in all four regions
    globalChamps = set(lck.string) & set(lec.string) & set(lcs.string) & set(lpl.string)
    #print(globalChamps)    
    

    # 2.a) top 5 most played counter pick for each region
    #print(lck.sort_values(by=["GPasCTR"], ascending=False).head())
    #print(lec.sort_values(by=["GPasCTR"], ascending=False).head())
    #print(lcs.sort_values(by=["GPasCTR"], ascending=False).head())
    #print(lpl.sort_values(by=["GPasCTR"], ascending=False).head())
    
    # 2.b) top 5 most successfuly counter pick for each region
    #print(lck.sort_values(by=["W%"], ascending=False).head())
    #print(lec.sort_values(by=["W%"], ascending=False).head())
    #print(lcs.sort_values(by=["W%"], ascending=False).head())
    #print(lpl.sort_values(by=["W%"], ascending=False).head())
    
    
    frames = [lck, lec, lcs, lpl]
    res = pd.concat(frames)
    res = res.groupby(["Champion", "Pos", "string"], as_index=False).mean()
    res = res[res["string"].isin(globalChamps)]
    
    # 3.a) most played counter pick champion globally
    #print(res.sort_values(by=["GPasCTR"], ascending=False))
    
    
    # 3.b) most successfuly counter pick champion globally
    #print(res.sort_values(by=["W%"], ascending=False))






    # Normality tests fails for both sets of data
    #print(stats.normaltest(lck["CTR%"]).pvalue)
    #print(stats.normaltest(lck["W%"]).pvalue)
    
    
        
    #sb.set()
    #plt.subplots(figsize=(15,7))
    #plt.xlabel("Win Rate %")
    #plt.ylabel("Counter Pick Rate %")   
    #plt.plot(lck["W%"], lck["CTR%"], 'b.', alpha=0.5)  
    #plt.show()
    
    



if __name__ == '__main__':
    main()