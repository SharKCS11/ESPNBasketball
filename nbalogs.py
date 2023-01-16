from espn_api.basketball import League
from espn_api.basketball import Team
from espn_api.basketball import Player
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguestandings
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as mplanimation
from matplotlib.widgets import Slider, Button
import pandas as pd
from difflib import SequenceMatcher

from nba_api.stats.static import players
player_dict = players.get_players();
player_dict = [ply for ply in player_dict if ply['is_active']]

bron_searched = None
min_thresh = 0.5
for ply in player_dict:
	name_key = "LeBron Jam".lower()
	fname_val = ply['full_name'].lower();
	smr = SequenceMatcher(None, name_key, fname_val).ratio()
	if (smr > min_thresh):
		print("Latest bron searched: ", ply['full_name'])
		bron_searched = ply
		min_thresh = smr 
		
print("Done searching")

'''
loc_espns2 = 'AEAyANDG6Feoz72dqFvI%2B8GLrRCe6B3zu%2Fy%2FPHz%2FcWIkacaxXUkjPfVdh%2BAL2gF2IA8TSTBrxqYE36mfp%2BiHLWvesx8QGFri8l9%2BmbxzqK5v2StZ5U%2Bb1gBmKQSgZx6KR7ykm7VHfiZmY7cNEoticKv4NphX6zjjOqpJWGjOIX62xSISktAlimWl3Bczq%2BncO1%2Bo62ZU0eRw2rW260lbr4ipuyAs0DlJOgviovzB%2BptBWa78jf6rhANeVXIVSh50NTc6rBnv%2Bo%2BUDjACGiMpW2qu'
loc_swid = '{906CAD31-CACC-4207-B203-2D5CCD556B31}'

league = League(league_id=163551, year=2023, espn_s2=loc_espns2, swid=loc_swid)

fig, ax = plt.subplots()
xvals = [(x+1) for x in range(len(league.teams))]
bars1 = ax.bar(xvals, [0 for x in range(len(league.teams))], width=0.4)
labels = [x.team_abbrev for x in league.teams]
l_yticks = [x for x in range(0,18)]
NforDraw = 0
baseFillArray = []
titlelabel = ax.text(0.9,0.95, "", transform=ax.transAxes, ha="center")

allrosteredplayers = []
playersToTeamIdx = {};

for team in league.teams:
	tIdx = league.teams.index(team)
	for player in team.roster:
		allrosteredplayers.append(player)
		playersToTeamIdx[player.name] = tIdx
		
numPlayers = len(allrosteredplayers)
allrosteredplayers = sorted(allrosteredplayers, key=lambda x: x.avg_points, reverse = True)

baseFillArray = [[0 for x in range(len(league.teams))] for x in range(len(allrosteredplayers))]

print("Filled roster map.")
'''




