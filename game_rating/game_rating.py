import sys 
import math
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn
seaborn.set()

def percent_to_float(x):
    return float(x.strip("%"))/100

def format_data(df):
    df["W%"] = round(df["W"] / df["GP"], 2)
    df["FT%"] = df["FT%"].apply(lambda x: percent_to_float(x))
    df["F3T%"] = df["F3T%"].apply(lambda x: percent_to_float(x))
    df["HLD%"] = df["HLD%"].apply(lambda x: percent_to_float(x))
    df["FD%"] = df["FD%"].apply(lambda x: percent_to_float(x))
    df["DRG%"] = df["DRG%"].apply(lambda x: percent_to_float(x))
    df["ELD%"] = df["ELD%"].apply(lambda x: percent_to_float(x))
    df["FBN%"] = df["FBN%"].apply(lambda x: percent_to_float(x))
    df["BN%"] = df["BN%"].apply(lambda x: percent_to_float(x))

    return df

def plot_relationship(df, xvalues, yvalues, title, xaxis, yaxis, filename):
    new_df = df.copy()

    fit = stats.linregress(new_df[xvalues], new_df[yvalues])
    new_df["prediction"] = new_df[xvalues] * fit.slope + fit.intercept

    plt.figure()
    plt.plot(new_df[xvalues], new_df[yvalues], 'b.', alpha=0.5)
    plt.plot(new_df[xvalues], new_df["prediction"], 'r-', linewidth=3)
    plt.title(title)
    plt.xlabel(xaxis)
    plt.ylabel(yaxis)
    #plt.show()
    plt.savefig(filename + ".png")

def main():
    # Questions: 
    # 1) Regionally
    # 2) Globally
    # EGR relationship to W% / FT% / F3T% / HLD% / FD% / DRG% / ELD% / FBN% / BN% 
    # MLR relationship to W% / DRG% / ELD% / BN%

    lck_team_data = format_data(pd.read_csv('lck_team_data.csv'))
    lec_team_data = format_data(pd.read_csv('lec_team_data.csv'))
    lcs_team_data = format_data(pd.read_csv('lcs_team_data.csv'))
    lpl_team_data = format_data(pd.read_csv('lpl_team_data.csv'))


    all_team_data = pd.concat([lck_team_data, lec_team_data, lcs_team_data, lpl_team_data])

    plot_relationship(all_team_data, "W%", "EGR", "Relationship between Win Rate and Early Game Rating", "Win Rate", "Early Game Rating", "win_rate_egr")

    plot_relationship(all_team_data, "FT%", "EGR", "Relationship between First Turret rate and Early Game Rating", "First Turret rate", "Early Game Rating", "ft_rate_egr")

    plot_relationship(all_team_data, "F3T%", "EGR", "Relationship between First 3 Turrets rate and Early Game Rating", "First 3 Turrets rate", "Early Game Rating", "f3t_rate_egr")

    plot_relationship(all_team_data, "HLD%", "EGR", "Relationship between Rift Herald Control rate Control and Early Game Rating", "Rift Herald Control rate", "Early Game Rating", "hld_rate_egr")

    plot_relationship(all_team_data, "FD%", "EGR", "Relationship between First Dragon rate and Early Game Rating", "First Dragon rate", "Early Game Rating", "fd_rate_egr")

    plot_relationship(all_team_data, "DRG%", "EGR", "Relationship between Dragon Control rate and Early Game Rating", "Dragon Control rate", "Early Game Rating", "drg_rate_egr")

    plot_relationship(all_team_data, "ELD%", "EGR", "Relationship between Elder Dragon Control rate and Early Game Rating", "Elder Dragon Control rate", "Early Game Rating", "eld_rate_egr")

    plot_relationship(all_team_data, "FBN%", "EGR", "Relationship between First Baron rate and Early Game Rating", "First Baron rate", "Early Game Rating", "fbn_rate_egr")

    plot_relationship(all_team_data, "BN%", "EGR", "Relationship between Baron Control rate and Early Game Rating", "Baron Control rate ", "Early Game Rating", "bn_rate_egr")


    plot_relationship(all_team_data, "W%", "MLR", "Relationship between Win Rate and Mid / Late Game Rating", "Win Rate", "Mid / Late Game Rating", "win_rate_mlr")

    plot_relationship(all_team_data, "DRG%", "MLR", "Relationship between Dragon Control rate and Mid / Late Game Rating", "Dragon Control rate", "Mid / Late Game Rating", "drg_rate_mlr")
    
    plot_relationship(all_team_data, "ELD%", "MLR", "Relationship between Elder Dragon Control rate and Mid / Late Game Rating", "Elder Dragon Control rate", "Mid / Late Game Rating", "eld_rate_mlr")

    plot_relationship(all_team_data, "BN%", "MLR", "Relationship between Baron Control rate and Mid / Late Game Rating", "Baron Control rate", "Mid / Late Game Rating", "bn_rate_mlr")

if __name__ == '__main__':
    main()