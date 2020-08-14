# CMPT353 Project
## League of Legends Professional Games Analysis

### Required Libraries:
* Sys 
* Math
* Pandas
* Numpy
* Scipy
* Seaborn
* Re
* Matplotlib
* Scikit-learn
* Statsmodels

### Running the Code
For all the python files in all folders, you can just run them by running the command python3 `'filename'.py`, where 'filename' is the name of the python file which you would like to run.

Files in the `champion_score`, `counterpick`, `game_rating` and `game_stats` folders can first be ran to see our findings from analyzing the champion data and team (game) data. Then file in the `player_comparison` and `ml` folders can be rans to generate our preditions.

Among all the python files, `stats.py`, `counterpick.py` and `game_rating.py` will output plots in `.png` file format. `player_compare.py`, `engine.py` and `pipeline.py` will output data in `.csv` file format, and some of them will also output images.



### Explanation of Abbreviations in CSV files
Champion Stats:<br/>
"Champion" - Champion Name<br/>
"Pos" - Position<br/>
"GP" - Games Played<br/>
"P%" - Percentage of Games Champion was picked in this Role<br/>
"B%" - Percentage of Games in which the Champion was Banned<br/>
"P+B%" - Percentage of Games in which the Champion was either Banned or picked<br/>
"W%" - Win Percentage<br/>
"CTR%" - Counter-pick Rate (percentage of games in which this champion was picked after their lane opponent)<br/>
"K" - Total Kills<br/>
"D" - Total Death<br/>
"A" - Total Assist<br/>
"KDA" - Total Kill/Death/Assit Ratio<br/>
"KP" - Kill Participation (kill or assist)<br/>
"DTH%" - Average Share of Team's Death<br/>
"FB%" - First Blood Rate<br/>
"GD10" - Average Gold Difference at 10 minutes<br/>
"XPD10" - Average Experience Difference at 10 minutes<br/>
"CSD10" - Average Creep Score Difference at 10 minutes<br/>
"CSPM" - Average Monster + Minions Killed per Minute<br/>
"CS%P15" - Average Share of Team's Total CS post-15-minutes<br/>
"DPM" - Avergae Damage to Champions per Minute<br/>
"DMG%" - Damage Share: Avergae Share of Team's total Damage to Champions<br/>
"GOLD%" - Gold Share: Avergae Share of Team's Total Gold Earned<br/>
"WPM" - Average Wards Placed per Minute<br/>
"WCPM" - Average Wards Cleared per Minute<br/>


Player Stats:<br/>
"Player" - Player in the Team<br/>
"Team" - Team Name<br/>
"Pos" - Position<br/>
"GP" - Games Played<br/>
"W%" - Win Percentage<br/>
"CTR%" - Counter-pick Rate (percentage of games in which this player was picked after their lane opponent)<br/>
"K" - Total Kills<br/>
"D" - Total Death<br/>
"A" - Total Assist<br/>
"KDA" - Total Kill/Death/Assit Ratio<br/>
"KP" - Kill Participation (kill or assist)<br/>
"KS%" - Kill Share (player's percentage of their team's total kill)<br/>
"DTH%" - Average Share of Team's Death<br/>
"FB%" - First Blood Rate<br/>
"GD10" - Average Gold Difference at 10 minutes<br/>
"XPD10" - Average Experience Difference at 10 minutes<br/>
"CSD10" - Average Creep Score Difference at 10 minutes<br/>
"CSPM" - Average Monster + Minions Killed per Minute<br/>
"CS%P15" - Average Share of Team's Total CS post-15-minutes<br/>
"DPM" - Avergae Damage to Champions per Minute<br/>
"DMG%" - Damage Share: Avergae Share of Team's total Damage to Champions<br/>
"GOLD%" - Gold Share: Avergae Share of Team's Total Gold Earned<br/>
"WPM" - Average Wards Placed per Minute<br/>
"WCPM" - Average Wards Cleared per Minute<br/>


Team Stats:<br/>
"Team" - Team Name<br/>
"GP" - Games Played<br/>
"W" - Wins<br/>
"L"	- Losses<br/>
"AGT" - Average Game Time/Duration, in Minutes<br/>
"K" - Total Kills<br/>
"D" - Total Death<br/>
"KD" - Kill to Death Ratio<br/>
"CKPM" - Average Combined Kills per Minute (team kills + oppotent kills)<br/>
"GPR" - Gold Percent Rating (average amount of game's total gold held, relative to 50%)<br/>
"GSPD" - Average Gold Spent Percentage Difference<br/>
"EGR" - Early-Game Rating<br/>
"MLR" - Mid/Late Rating<br/>
"GD15" - Average Gold Difference at 15 Minutes<br/>
"FB%" - First Blood Rate<br/>
"FT%" - First Tower Rate<br/>
"F3T%" - First-to-Three Towers Rate<br/>
"HLD%" - Rift Herald Control Rate<br/>
"FD%" - First Dragon Rate<br/>
"DRG%" - Dragon Control Rate<br/>
"ELD%" - Elder Dragon Control Rate<br/>
"FBN%" - First Baron Rate<br/>
"BN%" - Baron Control Rate<br/>
"LNE%" - Lane Control (average share of game's total lane CS)<br/>
"JNG%" - Jungle Control (average share of game's total jungle CS)<br/>
"WPM" - Average Wards Placed per Minute<br/>
"CWPM" - Average Wards Purchased per Minute<br/>
"WCPM" - Average Wards Cleared per Minute<br/>
