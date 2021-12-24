from espn_api.basketball import League
import matplotlib.pyplot as plt


league = League(league_id=163551, year=2022, espn_s2=l_espns2, swid=l_swid)

erq = league.espn_request
ddata = erq.get_league_draft()['draftDetail']['picks']

pickAverages = [0 for x in range(0, len(league.teams))]
pickTotals = [0 for x in range(0, len(league.teams))]
masterPlayerMap = {} # map from player ID to player Object
drafterMap = {} # Map from player ID to index of team that drafted them


print("Building player map\n")
for l_team in league.teams:
    for l_player in l_team.roster:
        masterPlayerMap[l_player.playerId] = l_player
    #end
#end for

FAs = league.free_agents(size=300)
for l_player in FAs:
    masterPlayerMap[l_player.playerId] = l_player

for l_pick in ddata:
    l_player = None
    lpName = "";
    plid = l_pick['playerId']
    if plid in masterPlayerMap:
        l_player = masterPlayerMap[plid]
        lpname = l_player.name
    else:
        continue
    teamIdx = l_pick['teamId'] - 1;
    drafterMap[plid] = teamIdx;
    print("Pick {} player {} team {}".format(l_pick['roundPickNumber'], l_player.name, league.teams[teamIdx].team_name))
    # Add to totals
    pickTotals[teamIdx] += round(l_player.total_points,1)
    

def observeWeek(lg, week, draftedPointsAccum, totalPointsAccum):
    print("Week {}...".format(week));
    allBoxScores = lg.box_scores(matchup_period = week)
    for scorePair in allBoxScores:
        homeTeamIdx = scorePair.home_team.team_id - 1
        for l_player in scorePair.home_lineup:
            totalPointsAccum[homeTeamIdx] += l_player.points
            if (l_player.playerId in drafterMap) and (homeTeamIdx==drafterMap[l_player.playerId]): # was drafted by this team
                #print("Player {} points {} for team {}".format(l_player.name, l_player.points, lg.teams[homeTeamIdx].team_name))
                draftedPointsAccum[homeTeamIdx] += l_player.points
        #end home team loop
        awayTeamIdx = scorePair.away_team.team_id - 1
        for l_player in scorePair.away_lineup:
            totalPointsAccum[awayTeamIdx] += l_player.points
            if (l_player.playerId in drafterMap) and (awayTeamIdx==drafterMap[l_player.playerId]): # was drafted by this team
                #print("Player {} points {} for team {}".format(l_player.name, l_player.points, lg.teams[awayTeamIdx].team_name))
                draftedPointsAccum[awayTeamIdx] += l_player.points
        #end away team loop
    #end for
    return
#end func

draftPA = [0 for team in league.teams]
totalPA = [0 for team in league.teams]
draftPointProportions = [0 for team in league.teams]
for wk in range(1, league.currentMatchupPeriod + 1):
    observeWeek(league, wk, draftPA, totalPA)

for i in range(0, len(draftPA)):
    draftPointProportions[i] = round(draftPA[i]*100/totalPA[i],1)

'''
for i in range(0, len(pickTotals)):
    pickTotals[i] = round(pickTotals[i], 0)
    
fig, axis = plt.subplots()
xlabels = [t.team_abbrev for t in league.teams]
xlabels_sort =[x for _, x in sorted(zip(pickTotals, xlabels), key=lambda pair: pair[0], reverse=True)]
xvals = [(i+1)*1.5 for i in range(len(league.teams))]
p1 = axis.bar(xvals, sorted(pickTotals, reverse=True), width=0.75, tick_label=xlabels_sort)
axis.set_title('Total points by drafted players only')
axis.bar_label(p1, label_type='edge', padding=2)
'''

fig, axis = plt.subplots()
xlabels = [t.team_abbrev for t in league.teams]
xvals = [(i+1)*1.5 for i in range(len(league.teams))]
p1 = axis.bar(xvals, draftPointProportions, width=0.75, tick_label=xlabels)
axis.set_title('Percentage of fantasy points scored by drafted players')
axis.bar_label(p1, label_type='edge', padding=2)
axis.set_ylabel('%')
