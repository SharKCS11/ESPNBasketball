from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import shapiro



# Get the list of all players
all_players = players.get_players()

# Filter players by those who have stats in the 2023-24 season
df_2023_24 = pd.read_csv('./player_list_data/player_list_2023_24_top250.csv')
minPlayedDict = {}
names_filter = set()
for row in df_2023_24.itertuples():
	name_lower = row.Player.lower()
	names_filter.add(row.Player.lower())
	minPlayedDict[name_lower] = row.MP

filtered_players = []
	
for player in all_players:
	# print(player['full_name'],"... ", end="")
	if player['full_name'].lower() in names_filter:
		# print("found!")
		filtered_players.append(player)

		
filtered_players.sort(key= lambda x: minPlayedDict[x['full_name'].lower()], reverse=True)
		
print("Top 250 active players and IDs in 2023-24 are:")
for player in filtered_players:
	print(player['full_name'], " - " , player['id'])



''' ********************************* ```
	LIST OF PLAYERS IS HERE, NOW START ANALYSIS
``` ********************************* '''

'''
tpID = 201942
tplayer = players.find_player_by_id(tpID)
season = "2023-24"
gamelog = playergamelog.PlayerGameLog(player_id=tpID, season=season)
gamelog_df = gamelog.get_data_frames()[0]
gamelog_df['FPT'] = (
    gamelog_df['PTS'] + 
    1.5 * gamelog_df['AST'] + 
    gamelog_df['REB'] + 
    0.2 * gamelog_df['OREB'] +
    3 * gamelog_df['STL'] + 
    3 * gamelog_df['BLK'] - 
    gamelog_df['TOV'] - 
    0.5 * (gamelog_df['FTA'] - gamelog_df['FTM'])
)

fpCol = gamelog_df['FPT']


# Plotting the histogram of the 'FPT' column
# ~ plt.figure(figsize=(10, 6))
# ~ plt.hist(fpCol, bins=20, edgecolor='black', alpha=0.7)
# ~ plt.title('Histogram of FPT')
# ~ plt.xlabel('FPT')
# ~ plt.ylabel('Frequency')
# ~ plt.show()

# Plotting the Q-Q plot
plt.figure(figsize=(10, 6))
stats.probplot(fpCol, dist="norm", plot=plt)
plt.title('Q-Q Plot of FPT')
plt.show()

# Perform the Shapiro-Wilk test
stat, p_value = shapiro(fpCol)
print(f"Shapiro-Wilk Test Statistic: {stat}")
print(f"P-Value: {p_value}")

print("DONE.")
'''
