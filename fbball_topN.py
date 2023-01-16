from espn_api.basketball import League
from espn_api.basketball import Team
from espn_api.basketball import Player
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguestandings
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as mplanimation
from matplotlib.widgets import Slider, Button

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

def animInit():
	NforDraw = 0
	ax.set_xticks(xvals, labels)
	ax.set_yticks(l_yticks)
	titlelabel.set_text("")
	return ([rect for rect in bars1] + [titlelabel])

def animDraw(i):
	for rect, y in zip(bars1, baseFillArray[i]):
		rect.set_height(y)
	titlelabel.set_text('Top %d players' %i)
	return ([rect for rect in bars1] + [titlelabel])
	
'''
def plotBarN(teamsList, bfArr, N):
	fig, ax = plt.subplots()
	xvals = [(x+1) for x in range(len(teamsList))]
	labels = [x.team_abbrev for x in teamsList]
	l_yticks = [x for x in range(1,17)]
	bars1 = ax.bar(xvals, bfArr[N], width=0.4)
	ax.set_xticks(xvals, labels)
	ax.set_yticks(l_yticks)
	plt.title('Top %d players' %N)
'''


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

for N in range(1, len(baseFillArray)+1):
	l_player = allrosteredplayers[N-1]; # grab the N'th player
	l_teamIdx = playersToTeamIdx[l_player.name]; # grab the team it belongs to
	print(l_player.name + " --> " + league.teams[l_teamIdx].team_name)
	# add 1 to all teams for the base fill array indices <= N
	for bfi in range(N,len(allrosteredplayers)):
		# print("  bfi ", bfi, " tidx ", l_teamIdx)
		baseFillArray[bfi][l_teamIdx] += 1
		
# Plot it
# plotBarN(league.teams, baseFillArray, 10)

anim = mplanimation.FuncAnimation(fig, animDraw, init_func=animInit, frames=180, interval=200, blit=True, repeat=True)
plt.show()