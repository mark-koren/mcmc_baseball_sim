import numpy as np
import pandas as pd
import pdb
from scipy.stats import beta

from player import Player
from team import Team
from game import Game
from league import League

PRODUCTIVE_OUTS_MADE_PRIOR = 13
PRODUCTIVE_OUTS_FAILED_PRIOR = 37

S31ST_MADE_PRIOR = 12
S31ST_FAILED_PRIOR = 29

DH1ST_MADE_PRIOR = 10
DH1ST_FAILED_PRIOR = 16

SH2ND_MADE_PRIOR = 29
SH2ND_FAILED_PRIOR = 19

def confidence_interval_99(samples):
	mu = samples[0]
	S = 0
	n = len(samples)
	for i in range(1,n):
		delta = samples[i] - mu
		mu = mu + delta/(i+1)
		S = S + delta ** 2 * i / (i + 1)

	s = np.sqrt(S/(n-1))
	ci_99 = 2.58*s/np.sqrt(n)
	return mu, ci_99

def win_probability(samples1, samples2, tie_prob_stop=0.001):
	# pdb.set_trace()
	game_samples1 = np.sum(samples1, axis=1)
	game_samples2 = np.sum(samples2, axis=1)

	run_samples1 = np.mean(samples1, axis=1)
	run_samples2 = np.mean(samples2, axis=1)

	run_dist1 = np.array([run_samples1[np.where(np.logical_and(run_samples1 >= x, run_samples1 < x+1))].shape[0] / run_samples1.shape[0] for x in range(21)])
	run_dist2 = np.array([run_samples2[np.where(np.logical_and(run_samples2 >= x, run_samples2 < x+1))].shape[0] / run_samples2.shape[0] for x in range(21)])

	game_dist1 = np.array([game_samples1[np.where(game_samples1 == x)].shape[0] / game_samples1.shape[0] for x in range(21)])
	game_dist2 = np.array([game_samples2[np.where(game_samples2 == x)].shape[0] / game_samples2.shape[0] for x in range(21)])

	win_prob1 = 0
	tie_prob = 0

	# pdb.set_trace()

	for i in range(game_dist1.shape[0]):
		for j in range(i + 1):
			if i == j:
			# Chances of winning in extra innings:
				tie_prob += game_dist1[i] * game_dist2[j]
			else:
				win_prob1 += game_dist1[i] * game_dist2[j]

	while (tie_prob > tie_prob_stop):
		# print(win_prob1, 1-(tie_prob + win_prob1), tie_prob)
		tie_prob_next = 0
		for i in range(run_dist1.shape[0]):
			for j in range(i + 1):
				if i == j:
				# Chances of winning in extra innings:
					tie_prob_next += tie_prob * run_dist1[i] * run_dist2[j]
				else:
					win_prob1 += tie_prob * run_dist1[i] * run_dist2[j]
		tie_prob = tie_prob_next

	# print(win_prob1, 1-(tie_prob + win_prob1), tie_prob)
	return win_prob1


def make_pitcher_2019(player_id, name):
	df_player_batting_against = pd.read_csv('./data/player_batting_against.csv')
	player_batting_against = df_player_batting_against[df_player_batting_against['Name'].str.contains(name)]

	ab = player_batting_against['AB'].values[0]
	hits = player_batting_against['H'].values[0]
	doubles = player_batting_against['2B'].values[0]
	triples = player_batting_against['3B'].values[0]
	homeruns = player_batting_against['HR'].values[0]
	singles = hits - (doubles + triples + homeruns)
	walks = player_batting_against['BB'].values[0]
	pa = ab+walks
	outs = pa - (hits + walks)

	return Player(player_id=player_id, name=name, walk = walks/pa, single=singles/pa,
				  double=doubles/pa, triple=triples/pa, homerun=homeruns/pa)

def make_batter_2019(player_id, name):
	df_player_batting = pd.read_csv('./data/player_standard_batting.csv')
	player_batting = df_player_batting[df_player_batting['Name'].str.contains(name)]

	df_player_baserunning = pd.read_csv('./data/player_baserunning_misc.csv')
	player_baserunning = df_player_baserunning[df_player_baserunning['Name'].str.contains(name)]

	df_player_situational = pd.read_csv('./data/player_situational_batting.csv')
	player_situational = df_player_situational[df_player_situational['Name'].str.contains(name)]

	ab = player_batting['AB'].values[0]
	hits = player_batting['H'].values[0]
	doubles = player_batting['2B'].values[0]
	triples = player_batting['3B'].values[0]
	homeruns = player_batting['HR'].values[0]
	singles = hits - (doubles + triples + homeruns)
	walks = player_batting['BB'].values[0]
	pa = ab+walks
	outs = pa - (hits + walks)

	s31st_made = player_baserunning['1stS3'].values[0]
	s31st_failed = player_baserunning['1stS'].values[0] - s31st_made
	s31st = beta(S31ST_MADE_PRIOR + s31st_made, s31st_failed + S31ST_FAILED_PRIOR).mean()

	dh1st_made = player_baserunning['1stDH'].values[0]
	dh1st_failed = player_baserunning['1stD'].values[0] - dh1st_made
	dh1st = beta(DH1ST_MADE_PRIOR + dh1st_made, dh1st_failed + DH1ST_FAILED_PRIOR).mean()

	sh2nd_made = player_baserunning['2ndSH'].values[0]
	sh2nd_failed = player_baserunning['2ndS'].values[0] - sh2nd_made
	sh2nd = beta(SH2ND_MADE_PRIOR + sh2nd_made, sh2nd_failed + SH2ND_FAILED_PRIOR).mean()
	# xbt = 0.5
	productive_outs_made = player_situational['POSuc'].values[0]
	productive_outs_failed = player_situational['POOpp'].values[0] - productive_outs_made
	productive_outs = beta(PRODUCTIVE_OUTS_MADE_PRIOR + productive_outs_made, productive_outs_failed + PRODUCTIVE_OUTS_FAILED_PRIOR).mean()

	return Player(player_id=player_id, name=name, walk = walks/pa, single=singles/pa,
				  double=doubles/pa, triple=triples/pa, homerun=homeruns/pa,
				  productive_out=productive_outs, s31st=s31st, dh1st=dh1st, sh2nd=sh2nd)

def make_team(name, players, pitcher, order=None):
	# df_team_batting = pd.read_csv('./data/team_standard_batting.csv')
	# team_batting = df_team_batting[df_team_batting['Tm'].str.match(name)]

	# df_team_baserunning = pd.read_csv('./data/team_baserunning_misc.csv')
	# team_baserunning = df_team_baserunning[df_team_baserunning['Tm'].str.match(name)]

	# df_team_situational = pd.read_csv('./data/team_situational_batting.csv')
	# team_situational = df_team_situational[df_team_situational['Tm'].str.match(name)]

	team = Team(name)
	team.players = players
	if order is None:
		order = [0,1,2,3,4,5,6,7,8]
	team.order = order
	# team.pitcher = pitcher

	# team.productive_out = productive_out
	# team.s31st = s31st
	# team.dh1st = dh1st
	# team.sh2nd = sh2nd

	return team


def braves_1989():
	pa = 231+23
	hits = 39
	doubles = 5
	triples = 0
	homeruns = 4
	singles = hits - (doubles + triples + homeruns)
	walks = 23
	outs = pa - (hits + walks)

	# _, davis = get_transition(walk = walks/pa, single=singles/pa, double=doubles/pa, triple=triples/pa, homerun=homeruns/pa, out=outs/pa)
	p_davis = Player(player_id=0, name='Davis', walk = walks/pa, single=singles/pa, double=doubles/pa, triple=triples/pa, homerun=homeruns/pa)

	pa = 266+32
	hits = 67
	doubles = 11
	triples = 0
	homeruns = 4
	singles = hits - (doubles + triples + homeruns)
	walks = 32
	outs = pa - (hits + walks)

	# _, perry = get_transition(walk = walks/pa, single=singles/pa, double=doubles/pa, triple=triples/pa, homerun=homeruns/pa, out=outs/pa)
	p_perry = Player(player_id=1, name='Perry', walk = walks/pa, single=singles/pa, double=doubles/pa, triple=triples/pa, homerun=homeruns/pa)

	pa = 473+30
	hits = 131
	doubles = 18
	triples = 3
	homeruns = 8
	singles = hits - (doubles + triples + homeruns)
	walks = 30
	outs = pa - (hits + walks)

	# _, treadway = get_transition(walk = walks/pa, single=singles/pa, double=doubles/pa, triple=triples/pa, homerun=homeruns/pa, out=outs/pa)
	p_treadway = Player(player_id=2, name='Treadway', walk = walks/pa, single=singles/pa, double=doubles/pa, triple=triples/pa, homerun=homeruns/pa)

	pa = 554+12
	hits = 118
	doubles = 18
	triples = 0
	homeruns = 13
	singles = hits - (doubles + triples + homeruns)
	walks = 12
	outs = pa - (hits + walks)

	# _, thomas = get_transition(walk = walks/pa, single=singles/pa, double=doubles/pa, triple=triples/pa, homerun=homeruns/pa, out=outs/pa)
	p_thomas = Player(player_id=3, name='Thomas', walk = walks/pa, single=singles/pa, double=doubles/pa, triple=triples/pa, homerun=homeruns/pa)

	pa = 456+38
	hits = 123
	doubles = 24
	triples = 2
	homeruns = 12
	singles = hits - (doubles + triples + homeruns)
	walks = 38
	outs = pa - (hits + walks)

	# _, blauser = get_transition(walk = walks/pa, single=singles/pa, double=doubles/pa, triple=triples/pa, homerun=homeruns/pa, out=outs/pa)
	p_blauser = Player(player_id=4, name='Blauser', walk = walks/pa, single=singles/pa, double=doubles/pa, triple=triples/pa, homerun=homeruns/pa)

	pa = 482+76
	hits = 152
	doubles = 34
	triples = 4
	homeruns = 21
	singles = hits - (doubles + triples + homeruns)
	walks = 76
	outs = pa - (hits + walks)

	# _, smith = get_transition(walk = walks/pa, single=singles/pa, double=doubles/pa, triple=triples/pa, homerun=homeruns/pa, out=outs/pa)
	p_smith = Player(player_id=5, name='Smith', walk = walks/pa, single=singles/pa, double=doubles/pa, triple=triples/pa, homerun=homeruns/pa)

	pa = 574+65
	hits = 131
	doubles = 16
	triples = 0
	homeruns = 20
	singles = hits - (doubles + triples + homeruns)
	walks = 65
	outs = pa - (hits + walks)

	# _, murphy = get_transition(walk = walks/pa, single=singles/pa, double=doubles/pa, triple=triples/pa, homerun=homeruns/pa, out=outs/pa)
	p_murphy = Player(player_id=6, name='Murphy', walk = walks/pa, single=singles/pa, double=doubles/pa, triple=triples/pa, homerun=homeruns/pa)

	pa = 280+27
	hits = 85
	doubles = 18
	triples = 4
	homeruns = 7
	singles = hits - (doubles + triples + homeruns)
	walks = 27
	outs = pa - (hits + walks)

	# _, mcdowell = get_transition(walk = walks/pa, single=singles/pa, double=doubles/pa, triple=triples/pa, homerun=homeruns/pa, out=outs/pa)
	p_mcdowell = Player(player_id=7, name='McDowell', walk = walks/pa, single=singles/pa, double=doubles/pa, triple=triples/pa, homerun=homeruns/pa)

	pa = 67+62+63+41+31+28+10+7+6+3+3+2+2+1+1+1+1+1+1+5+6+4+3
	hits = 10+7+12+4+5+5+1+1+1
	doubles = 1+1
	triples = 1+1+1
	homeruns = 1
	singles = hits - (doubles + triples + homeruns)
	walks = 5+6+4+3
	outs = pa - (hits + walks)

	# _, pitcher = get_transition(walk = walks/pa, single=singles/pa, double=doubles/pa, triple=triples/pa, homerun=homeruns/pa, out=outs/pa)
	p_pitcher = Player(player_id=8, name='Pitcher', walk = walks/pa, single=singles/pa, double=doubles/pa, triple=triples/pa, homerun=homeruns/pa)


	braves = Team()
	braves.players = [p_smith, p_mcdowell, p_blauser, p_treadway, p_perry, p_murphy, p_thomas, p_davis, p_pitcher]
	braves.order = [4, 0, 1, 2, 3, 5, 6, 8, 7]
	return braves
	# return [perry, smith, mcdowell, blauser, treadway, murphy, thomas, pitcher, davis], braves
	# return [smith, mcdowell, perry, blauser, treadway, murphy, thomas, davis, pitcher]
	# return [pitcher, treadway, perry, davis, thomas, blauser, mcdowell, murphy, smith]

def chicago_whitesox_2019():
	players = []

	players.append(make_batter_2019(0, 'mccanja02'))
	players.append(make_batter_2019(1, 'abreujo02'))
	players.append(make_batter_2019(2, 'sanchca01'))
	players.append(make_batter_2019(3, 'anderti01'))
	players.append(make_batter_2019(4, 'moncayo01'))
	players.append(make_batter_2019(5, 'jimenel02'))
	players.append(make_batter_2019(6, 'engelad01'))
	players.append(make_batter_2019(7, 'garcile02'))
	players.append(make_batter_2019(8, 'goinsry01'))


	order = [3, 4, 1, 5, 0, 8, 2, 7, 6]

	return make_team('CWS', players, None, order=order)

def chicago_whitesox_2020():
	players = []

	players.append(make_batter_2019(0, 'grandya01'))
	players.append(make_batter_2019(1, 'abreujo02'))
	players.append(make_batter_2019(2, 'garcile02'))
	players.append(make_batter_2019(3, 'anderti01'))
	players.append(make_batter_2019(4, 'moncayo01'))
	players.append(make_batter_2019(5, 'jimenel02'))
	players.append(make_batter_2019(6, 'mazarno01'))
	players.append(make_batter_2019(7, 'sotoju01'))
	players.append(make_batter_2019(8, 'encared01'))


	order = [3, 4, 1, 5, 0, 8, 7, 6, 2]

	return make_team('CWS', players, None, order=order)
	# ab = 231
	# hits = 39
	# doubles = 5
	# triples = 0
	# homeruns = 4
	# singles = hits - (doubles + triples + homeruns)
	# walks = 23
	# pa = ab+walks
	# outs = pa - (hits + walks)
	# xbt = 0.5

	# productive_outs = 0.5

def mlb_2019():


	ab = 166651
	hits = 42039
	doubles = 8531
	triples = 785
	homeruns = 6776
	singles = hits - (doubles + triples + homeruns)
	walks = 15895
	pa = ab+walks

	return League(name='MLB2019', walk = walks/pa, single=singles/pa,
			  double=doubles/pa, triple=triples/pa, homerun=homeruns/pa)

def mlb_1989():


	ab = 142821
	hits = 36293
	doubles = 6307
	triples = 868
	homeruns = 3083
	singles = hits - (doubles + triples + homeruns)
	walks = 13528
	pa = ab+walks

	return League(name='MLB1989', walk = walks/pa, single=singles/pa,
			  double=doubles/pa, triple=triples/pa, homerun=homeruns/pa)	

if __name__ == '__main__':
	xx = make_batter_2019(0, 'Jose Abreu')
	cws = chicago_whitesox_2019()
	pdb.set_trace()
