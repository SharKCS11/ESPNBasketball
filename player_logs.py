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
# end_idx = 1 # comment later
for idx in range(start_idx, end_idx):
	tpID = filtered_players[idx]['id']
	l_name = filtered_players[idx]['full_name']
	print("FPTS for ", l_name, "... ", end="")
	gamelog = playergamelog.PlayerGameLog(player_id=tpID, season=season)
	df = gamelog.get_data_frames()[0]
	if df.empty:
		print("Error: empty df at tpID ", tpID, " and idx ", idx)
		sys.exit(1)
	
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
	print(" saved to ", file_name)
	time.sleep(1)
'''

''' ********************************* ```
	CSVs GENERATED. NOW ANALYZE
``` ********************************* '''

all_shap_stats = {}
all_shap_pvals = {}

outData = pd.DataFrame(columns=["MP_Rank","ID","Name","MP_Tot","Ave","StdDev","W","PVal","CV"])

end_idx = len(filtered_players)
start_idx = 0

# end_idx = 1 # comment later

for idx in range(start_idx, end_idx):
	tpID = filtered_players[idx]['id']
	file_name = f"./player_list_data/igl/game_log_{tpID}.csv"
	gamelog_df = pd.read_csv(file_name)
	fpCol = gamelog_df['FPT']

	# Perform the Shapiro-Wilk test
	print("Player ", filtered_players[idx]['full_name'],
			"Mean and stddev are: ", round(fpCol.mean(), 2), 
			" and ", round(fpCol.std(), 2))
	stat, p_value = stats.shapiro(fpCol)
	stat = "{:.4g}".format(stat)
	p_value = "{:.4g}".format(p_value)
	all_shap_stats[idx] = stat
	all_shap_pvals[idx] = p_value
	
	new_row = pd.DataFrame([{"MP_Rank": idx,
				"ID": tpID,
				"Name": filtered_players[idx]['full_name'],
				"MP_Tot": sum(gamelog_df['MIN']),
				"Ave": round(fpCol.mean(), 2),
				"StdDev": round(fpCol.std(), 2),
				"W": stat,
				"PVal": p_value,
				"CV" : round(fpCol.std()/fpCol.mean(),2)}])
	outData = pd.concat([outData,new_row], ignore_index=True)
	
	print(f"    Shapiro Test Statistic: {stat}")
	print(f"    P-Value: {p_value}")
	

outData.to_csv('./player_list_data/processed_df.csv', index=False)


# Plotting the Q-Q plot
mIdx = 0
mID = filtered_players[mIdx]['id']
m_name = filtered_players[mIdx]['full_name']
plt.figure(figsize=(10, 6))
stats.probplot(fpCol, dist="norm", plot=plt)
plt.title(f"Q-Q Plot of {m_name} FPTS")
mStat = all_shap_stats[mIdx]; mPval = all_shap_pvals[mIdx];
mTextstr = f'Shapiro Normality Test\nStatistic: {mStat}\nP-Value: {mPval}'
plt.gca().text(0.05, 0.95, mTextstr, transform=plt.gca().transAxes, fontsize=12,
               verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5))

plt.show()



print("DONE.")

