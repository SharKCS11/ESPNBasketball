from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import pickle


'''
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

with open('./player_list_data/filtered_players_dict.pkl','wb') as file:
	pickle.dump(filtered_players, file)

'''

''' ********************************* ```
	LIST OF PLAYERS IS PICKLED. LOAD THEM
``` ********************************* '''
filtered_players = None
with open('player_list_data/filtered_players_dict.pkl', 'rb') as file:
	filtered_players = pickle.load(file)

''' ********************************* ```
	NOW GENERATE THE CSVs
``` ********************************* '''

'''
end_idx = len(filtered_players)
start_idx = 0

season = '2023-24'
end_idx = 1 # uncomment later
for idx in range(start_idx, end_idx):
	tpID = filtered_players[idx]['id']
	gamelog = playergamelog.PlayerGameLog(player_id=tpID, season=season)
	df = gamelog.get_data_frames()[0]
	df['FPT'] = (df['PTS'] * 1 +
             df['AST'] * 1.5 +
             df['REB'] * 1 +
             df['OREB'] * 0.2 +
             df['STL'] * 3 +
             df['BLK'] * 3 -
             df['TOV'] * 1 -
             (df['FTA'] - df['FTM']) * 0.5)
	file_name = f"./player_list_data/igl/game_log_{tpID}.csv"
	df.to_csv(file_name, index=False, mode='w')
	print("FPTS for ", filtered_players[idx]['full_name'], " saved to ", file_name)
	
'''

''' ********************************* ```
	CSVs GENERATED. NOW ANALYZE
``` ********************************* '''


end_idx = len(filtered_players)
start_idx = 0

end_idx = 1 # unclomment later

for idx in range(start_idx, end_idx):
	tpID = filtered_players[idx]['id']
	file_name = f"./player_list_data/igl/game_log_{tpID}.csv"
	gamelog_df = pd.read_csv(file_name)
	fpCol = gamelog_df['FPT']

	# Perform the Shapiro-Wilk test
	print("Mean and stddev are: ", round(fpCol.mean(), 2), 
			" and ", round(fpCol.std(), 2))
	stat, p_value = stats.shapiro(fpCol)
	stat = "{:.4g}".format(stat)
	p_value = "{:.4g}".format(p_value)
	print(f"Shapiro Test Statistic: {stat}")
	print(f"P-Value: {p_value}")


# Plotting the Q-Q plot
plt.figure(figsize=(10, 6))
stats.probplot(fpCol, dist="norm", plot=plt)
plt.title('Q-Q Plot of FPT')
plt.show()




print("DONE.")

