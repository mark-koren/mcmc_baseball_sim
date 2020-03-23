import numpy as np
import pdb
import matplotlib.pyplot as plt
from pprint import pprint

from player import Player
from team import Team
from game import Game
from league import League
from data import *

def morey_z(p_b, p_p, p_l):
	return (((p_b - p_l)/np.sqrt(p_l*(1-p_l)) + (p_p - p_l)/np.sqrt(p_l*(1-p_l))) 
		/ np.sqrt(2) * np.sqrt(p_l*(1-p_l)) + p_l)


# def make_markov_player(walk, single, double, triple, homerun, out):
# 	P, P_list = get_transition(walk, single, double, triple, homerun, out)
# 	markov_p_list = []
# 	pdb.set_trace()
# 	for i in len(P_list):
# 		markov_p_list.append(np.concatenate([P_list[i]]*9))



def MetropolisHastingsUpdate(x, pi, Q_sample, Q_eval):
	y = Q_sample(x)
	R = pi(y)/pi(x) * Q_eval(y,x) / Q_eval(x,y)

	if np.random.uniform() <= R:
		return y
	else:
		return x

def MetropolisHastingsSampler(n, x0, pi, Q_sample, Q_eval):
	x = [x0]
	for i in range(1,n):
		x.append(MetropolisHastingsUpdate(x=x[i-1], pi=pi, Q_sample=Q_sample, Q_eval=Q_eval))

	return np.array(x)


if __name__ == '__main__':
	cws = chicago_whitesox_2019()

	game = Game(home_team=cws, away_team=cws, league=mlb_2019()) 
	game.baserunning = True
	game.advanced_transition=True

	n = 10000
	home_runs = np.zeros((n, 9))
	away_runs = np.zeros((n, 9))
	for i in range(n):
		game_results = game.sim_game(debug=False)
		away_runs[i,:] = game_results[0,:]
		home_runs[i,:] = game_results[1,:]

	print('CWS Runs (Basic) (MCMC):  %f +/- %f' % confidence_interval_99(np.sum(home_runs, axis=1)))
	print(win_probability(away_runs, home_runs, tie_prob_stop=0.001))


	n = 10000
	home_runs = np.zeros((n, 9))
	away_runs = np.zeros((n, 9))
	game_init = np.array([[0,0,0,0,0,0,0,0,0],[1,0,0,0,0,0,0,0,0]])
	for i in range(n):
		game.set_scenario(game=game_init,
		   				  runs=0,
		   				  first_base=None,
		   				  second_base=None,
		   				  third_base=None,
		   				  outs=0,
		   				  top_half=True,
		   				  inning=1, 
		   				  away_index=0,
		   				  home_index=0)
		game_results = game.sim_scenario(debug=False)
		away_runs[i,:] = game_results[0,:]
		home_runs[i,:] = game_results[1,:]

	print('CWS Runs (Basic) (MCMC):  %f +/- %f' % confidence_interval_99(np.sum(home_runs, axis=1)))
	print(win_probability(away_runs, home_runs, tie_prob_stop=0.001))

	# game.advanced_transition=True

	# u = game.sim_game_markov()
	# run_dist = u[0, 21*8:].T
	# runs = np.arange(21)
	# print('CWS Runs (Adv) (MC): ',  np.dot(runs,  run_dist))

	# n = 10000
	# cws_runs = np.zeros((2*n, 9))
	# for i in range(n):
	# 	game_results = game.sim_game(debug=False)
	# 	cws_runs[i,:] = game_results[0,:]
	# 	cws_runs[n+i,:] = game_results[1,:]

	# print('CWS Runs (Adv) (MCMC):  %f +/- %f' % confidence_interval_99(np.sum(cws_runs, axis=1)))

	# game.baserunning = True
	# game.advanced_transition=False

	# n = 10000
	# cws_runs = np.zeros((2*n, 9))
	# for i in range(n):
	# 	game_results = game.sim_game(debug=False)
	# 	cws_runs[i,:] = game_results[0,:]
	# 	cws_runs[n+i,:] = game_results[1,:]

	# print('CWS Runs (BR) (MCMC):  %f +/- %f' % confidence_interval_99(np.sum(cws_runs, axis=1)))

	# game.baserunning = True
	# game.advanced_transition=True

	# n = 10000
	# cws_runs = np.zeros((2*n, 9))
	# for i in range(n):
	# 	game_results = game.sim_game(debug=False)
	# 	cws_runs[i,:] = game_results[0,:]
	# 	cws_runs[n+i,:] = game_results[1,:]

	# print('CWS Runs (Adv) (BR) (MCMC):  %f +/- %f' % confidence_interval_99(np.sum(cws_runs, axis=1)))
