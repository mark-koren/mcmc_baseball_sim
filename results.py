import numpy as np
import pdb
import matplotlib.pyplot as plt
from pprint import pprint

from project import *	
from data import *

from player import Player
from team import Team
from game import Game
from league import League

def tim_anderson_stats():
	cws = chicago_whitesox_2019()

	game = Game(home_team=cws, away_team=cws, league=mlb_2019())

	tim = cws.players[3]
	print('-------- Simple ---------------')
	print('Tim Anderson P(walk) %f' % tim.walk)
	print('Tim Anderson P(single) %f' % tim.single)
	print('Tim Anderson P(double) %f' % tim.double)
	print('Tim Anderson P(triple) %f' % tim.triple)
	print('Tim Anderson P(homerun) %f' % tim.homerun)
	print('Tim Anderson P(out) %f' % tim.out)

	game.advanced_transition = True
	game.batter = tim
	game.pitcher = None
	game.update_transition()
	print('-------- vs Avg ---------------')
	print('Tim Anderson P(walk) %f' % game.walk)
	print('Tim Anderson P(single) %f' % game.single)
	print('Tim Anderson P(double) %f' % game.double)
	print('Tim Anderson P(triple) %f' % game.triple)
	print('Tim Anderson P(homerun) %f' % game.homerun)
	print('Tim Anderson P(out) %f' % game.out)

	game.batter = tim
	game.pitcher = make_pitcher_2019(player_id=0, name='kikucyu01')
	game.update_transition()
	print('--------vs Yusei Kikuchi ---------------')
	print('Tim Anderson P(walk) %f' % game.walk)
	print('Tim Anderson P(single) %f' % game.single)
	print('Tim Anderson P(double) %f' % game.double)
	print('Tim Anderson P(triple) %f' % game.triple)
	print('Tim Anderson P(homerun) %f' % game.homerun)
	print('Tim Anderson P(out) %f' % game.out)

	game.batter = tim
	game.pitcher = make_pitcher_2019(player_id=0, name='colege01')
	game.update_transition()
	print('--------vs Gerrit Cole---------------')
	print('Tim Anderson P(walk) %f' % game.walk)
	print('Tim Anderson P(single) %f' % game.single)
	print('Tim Anderson P(double) %f' % game.double)
	print('Tim Anderson P(triple) %f' % game.triple)
	print('Tim Anderson P(homerun) %f' % game.homerun)
	print('Tim Anderson P(out) %f' % game.out)

	print('----- Running Stats ---------')
	print('Tim Anderson P(productive_out) %f' % tim.productive_out)
	print('Tim Anderson P(s31st) %f' % tim.s31st)
	print('Tim Anderson P(dh1st) %f' % tim.dh1st)
	print('Tim Anderson P(sh2nd) %f' % tim.sh2nd)

def comparison_MC_MCMC_89Braves():
	braves = braves_1989()

	game = Game(home_team=braves, away_team=braves, league=mlb_1989()) 
	n = 10000

	u = game.sim_game_markov()
	run_dist = u[0, 21*8:].T
	runs = np.arange(21)
	print('Braves Runs (MC): ',  np.dot(runs,  run_dist))

	braves_runs = np.zeros((2*n, 9))

	for i in range(n):
		game_results = game.sim_game(debug=False)
		braves_runs[i,:] = game_results[0,:]
		braves_runs[n+i,:] = game_results[1,:]

	print('CWS Runs (Basic) (MCMC):  %f +/- %f' % confidence_interval_99(np.sum(braves_runs, axis=1)))

	game.advanced_transition=True

	u = game.sim_game_markov()
	run_dist = u[0, 21*8:].T
	runs = np.arange(21)
	print('Braves Runs (Adv) (MC): ',  np.dot(runs,  run_dist))

	braves_runs = np.zeros((2*n, 9))

	for i in range(n):
		game_results = game.sim_game(debug=False)
		braves_runs[i,:] = game_results[0,:]
		braves_runs[n+i,:] = game_results[1,:]

	print('CWS Runs (Basic) (MCMC):  %f +/- %f' % confidence_interval_99(np.sum(braves_runs, axis=1)))


def braves_scoring_index():
	braves = braves_1989()

	game = Game(home_team=braves, away_team=braves, league=mlb_1989()) 
	n = 10000

	for i in range (9):
		braves.order = [i]
		game = Game()
		game.home_team = braves
		game.away_team = braves
		u = game.sim_inning_markov()
		run_dist = u[:,-1].T
		runs = np.arange(20)
		print('Scoring Index (MC): ',  np.dot(runs,  run_dist))
		
		n = 10000
		braves_runs = np.zeros((2*n, 9))
		for j in range(n):
			game_results = game.sim_game(debug=False)
			braves_runs[j,:] = game_results[0,:]
			braves_runs[n+j,:] = game_results[1,:]

		print('Scoring Index (MCMC): ', np.mean(braves_runs[:,0], axis=0))

	# for i in range (9):
	# 	braves.order = [i]*9
	# 	game = Game()
	# 	game.home_team = braves
	# 	game.away_team = braves
	# 	# game.sim_half_inning(debug=True)
	# 	n = 10000
	# 	braves_runs = np.zeros((2*n, 9))
	# 	# pprint(run_dist)

	# 	for i in range(n):
	# 		game_results = game.sim_game(debug=False)
	# 		braves_runs[i,:] = game_results[0,:]
	# 		braves_runs[n+i,:] = game_results[1,:]

	# 	print('Scoring Index (MCMC): ', np.mean(braves_runs[:,0], axis=0))

def comparison_advanced_2019CWS():
	cws = chicago_whitesox_2019()

	game = Game(home_team=cws, away_team=cws, league=mlb_2019()) 

	u = game.sim_game_markov()
	run_dist = u[0, 21*8:].T
	runs = np.arange(21)
	print('CWS Runs (Basic) (MC): ',  np.dot(runs,  run_dist))

	n = 10000
	cws_runs = np.zeros((2*n, 9))
	for i in range(n):
		game_results = game.sim_game(debug=False)
		cws_runs[i,:] = game_results[0,:]
		cws_runs[n+i,:] = game_results[1,:]

	print('CWS Runs (Basic) (MCMC):  %f +/- %f' % confidence_interval_99(np.sum(cws_runs, axis=1)))

	game.advanced_transition=True

	u = game.sim_game_markov()
	run_dist = u[0, 21*8:].T
	runs = np.arange(21)
	print('CWS Runs (Adv) (MC): ',  np.dot(runs,  run_dist))

	n = 10000
	cws_runs = np.zeros((2*n, 9))
	for i in range(n):
		game_results = game.sim_game(debug=False)
		cws_runs[i,:] = game_results[0,:]
		cws_runs[n+i,:] = game_results[1,:]

	print('CWS Runs (Adv) (MCMC):  %f +/- %f' % confidence_interval_99(np.sum(cws_runs, axis=1)))

	game.baserunning = True
	game.advanced_transition=False

	n = 10000
	cws_runs = np.zeros((2*n, 9))
	for i in range(n):
		game_results = game.sim_game(debug=False)
		cws_runs[i,:] = game_results[0,:]
		cws_runs[n+i,:] = game_results[1,:]

	print('CWS Runs (BR) (MCMC):  %f +/- %f' % confidence_interval_99(np.sum(cws_runs, axis=1)))

	game.baserunning = True
	game.advanced_transition=True

	n = 10000
	cws_runs = np.zeros((2*n, 9))
	for i in range(n):
		game_results = game.sim_game(debug=False)
		cws_runs[i,:] = game_results[0,:]
		cws_runs[n+i,:] = game_results[1,:]

	print('CWS Runs (Adv) (BR) (MCMC):  %f +/- %f' % confidence_interval_99(np.sum(cws_runs, axis=1)))

def comparison_baserunning_19cws():
	cws = chicago_whitesox_2019()

	game = Game(home_team=cws, away_team=cws, league=mlb_2019()) 
	game.advanced_transition=True
	game.baserunning = False

	u = game.sim_game_markov()
	run_dist = u[0, 21*8:].T
	runs = np.arange(21)
	print('Braves Runs (MC): ',  np.dot(runs,  run_dist))

	n = 10000
	braves_runs = np.zeros((2*n, 9))
	for i in range(n):
		game_results = game.sim_game(debug=False)
		braves_runs[i,:] = game_results[0,:]
		braves_runs[n+i,:] = game_results[1,:]

	print('Braves Runs (MCMC): ', np.mean(np.sum(braves_runs, axis=1)))

	game.baserunning = True

	n = 10000
	braves_runs = np.zeros((2*n, 9))
	for i in range(n):
		game_results = game.sim_game(debug=False)
		braves_runs[i,:] = game_results[0,:]
		braves_runs[n+i,:] = game_results[1,:]

	print('Braves Runs With baserunning (MCMC): ', np.mean(np.sum(braves_runs, axis=1)))

def comparison_stealing_2019():
	cws = chicago_whitesox_2019()

	game = Game(home_team=cws, away_team=cws, league=mlb_2019()) 
	game.advanced_transition=True
	game.baserunning = True
	runs = []
	
	n = 10000
	cws_runs = np.zeros((n, 1))
	for i in range(n):
		game.outs = 0
		game.runs = 0
		game.first_base = cws.players[3]
		cws.index = 1
		game.second_base = None
		game.third_base = None

		game.sim_half_inning(initial_setup = True, debug=False)
		cws_runs[i,:] = game.runs

	print('CWS runs 2019 (MCMC): ', np.mean(cws_runs))
	print('CWS P(1 run) 2019 (MCMC): ', cws_runs[np.where(cws_runs > 0)].shape[0] / cws_runs.shape[0])
	# plt.hist(cws_runs)
	# plt.show()
	runs.append(cws_runs)

	cws_runs = np.zeros((n, 1))
	for i in range(n):
		game.outs = 0
		game.runs = 0
		game.first_base = None
		cws.index = 1
		game.second_base = cws.players[3]
		game.third_base = None

		game.sim_half_inning(initial_setup = True, debug=False)
		cws_runs[i,:] = game.runs

	print('CWS runs 2019 (Stole 2nd) (MCMC): ', np.mean(cws_runs))
	print('CWS P(1 run) 2019 (MCMC): ', cws_runs[np.where(cws_runs > 0)].shape[0] / cws_runs.shape[0])
	# plt.hist(cws_runs)
	# plt.show()
	runs.append(cws_runs)

	cws_runs = np.zeros((n, 1))
	for i in range(n):
		game.outs = 1
		game.runs = 0
		game.first_base = None
		cws.index = 1
		game.second_base = None
		game.third_base = None

		game.sim_half_inning(initial_setup = True, debug=False)
		cws_runs[i,:] = game.runs

	print('CWS runs 2019 (Caught Stealing) (MCMC): ', np.mean(cws_runs))
	print('CWS P(1 run) 2019 (MCMC): ', cws_runs[np.where(cws_runs > 0)].shape[0] / cws_runs.shape[0])
	# plt.hist(cws_runs)
	# plt.show()
	runs.append(cws_runs)

	ta_steal_prob = 68/(68+16)

	runs.append(runs[1] * ta_steal_prob + runs[2] * (1 - ta_steal_prob))

	print('CWS runs 2019 (Stealing) (MCMC): ', np.mean(runs[-1]))
	print('CWS P(1 run) 2019 (MCMC): ', 
		runs[1][np.where(runs[1] > 0)].shape[0] / runs[1].shape[0] * ta_steal_prob +
		runs[2][np.where(runs[2] > 0)].shape[0] / runs[2].shape[0] * (1 - ta_steal_prob))

	xx = np.array(runs).reshape((4,-1))
	plt.hist(xx.T, bins=[0,1,2,3,4,5,6], density=True, histtype='bar', align='left',
			 label=['TA on 1st, 0 Outs', 'TA on 2nd, 0 Outs', 'No one on, 1 Outs', 'Stealing'])
	plt.legend()
	plt.xlabel('Runs in Inning')
	plt.ylabel('Probability')
	plt.show()

def comparison_stealing_2020():
	cws = chicago_whitesox_2020()

	game = Game(home_team=cws, away_team=cws, league=mlb_2019()) 
	game.advanced_transition=True
	game.baserunning = True
	runs = []
	
	n = 10000
	cws_runs = np.zeros((n, 1))
	for i in range(n):
		game.outs = 0
		game.runs = 0
		game.first_base = cws.players[3]
		cws.index = 1
		game.second_base = None
		game.third_base = None

		game.sim_half_inning(initial_setup = True, debug=False)
		cws_runs[i,:] = game.runs

	print('CWS runs 2020 (MCMC): ', np.mean(cws_runs))
	print('CWS P(1 run) 2020 (MCMC): ', cws_runs[np.where(cws_runs > 0)].shape[0] / cws_runs.shape[0])
	# plt.hist(cws_runs)
	# plt.show()
	runs.append(cws_runs)

	cws_runs = np.zeros((n, 1))
	for i in range(n):
		game.outs = 0
		game.runs = 0
		game.first_base = None
		cws.index = 1
		game.second_base = cws.players[3]
		game.third_base = None

		game.sim_half_inning(initial_setup = True, debug=False)
		cws_runs[i,:] = game.runs

	print('CWS runs 2020 (Stole 2nd) (MCMC): ', np.mean(cws_runs))
	print('CWS P(1 run) 2020 (MCMC): ', cws_runs[np.where(cws_runs > 0)].shape[0] / cws_runs.shape[0])
	# plt.hist(cws_runs)
	# plt.show()
	runs.append(cws_runs)

	cws_runs = np.zeros((n, 1))
	for i in range(n):
		game.outs = 1
		game.runs = 0
		game.first_base = None
		cws.index = 1
		game.second_base = None
		game.third_base = None

		game.sim_half_inning(initial_setup = True, debug=False)
		cws_runs[i,:] = game.runs

	print('CWS runs 2020 (Caught Stealing) (MCMC): ', np.mean(cws_runs))
	print('CWS P(1 run) 2020 (MCMC): ', cws_runs[np.where(cws_runs > 0)].shape[0] / cws_runs.shape[0])
	# plt.hist(cws_runs)
	# plt.show()
	runs.append(cws_runs)

	ta_steal_prob = 68/(68+16)

	runs.append(runs[1] * ta_steal_prob + runs[2] * (1 - ta_steal_prob))

	print('CWS runs 2020 (Stealing) (MCMC): ', np.mean(runs[-1]))
	print('CWS P(1 run) 2020 (MCMC): ', 
		runs[1][np.where(runs[1] > 0)].shape[0] / runs[1].shape[0] * ta_steal_prob +
		runs[2][np.where(runs[2] > 0)].shape[0] / runs[2].shape[0] * (1 - ta_steal_prob))

	xx = np.array(runs).reshape((4,-1))
	plt.hist(xx.T, bins=[0,1,2,3,4,5,6], density=True, histtype='bar', align='left',
			 label=['TA on 1st, 0 Outs', 'TA on 2nd, 0 Outs', 'No one on, 1 Outs', 'Stealing'])
	plt.legend()
	plt.xlabel('Runs in Inning')
	plt.ylabel('Probability')
	plt.show()

def steal_scenario_1():

	players = []

	players.append(make_batter_2019(0, 'castiwe01'))
	players.append(make_batter_2019(1, 'abreujo02'))
	players.append(make_batter_2019(2, 'sanchca01'))
	players.append(make_batter_2019(3, 'anderti01'))
	players.append(make_batter_2019(4, 'moncayo01'))
	players.append(make_batter_2019(5, 'jimenel02'))
	players.append(make_batter_2019(6, 'garcile02'))
	players.append(make_batter_2019(7, 'palkada01'))
	players.append(make_batter_2019(8, 'alonsyo01'))


	order = [6, 4, 1, 8, 5, 7, 0, 3, 2]

	away_team = make_team('CWS', players, None, order=order)

	players = []

	players.append(make_batter_2019(0, 'maldoma01'))
	players.append(make_batter_2019(1, 'ohearry01'))
	players.append(make_batter_2019(2, 'owingch01'))
	players.append(make_batter_2019(3, 'mondera02'))
	players.append(make_batter_2019(4, 'doziehu01'))
	players.append(make_batter_2019(5, 'gordoal01'))
	players.append(make_batter_2019(6, 'hamilbi02'))
	players.append(make_batter_2019(7, 'merriwh01'))
	players.append(make_batter_2019(8, 'solerjo01'))


	order = [7, 3, 5, 8, 1, 2, 4, 0, 6]

	home_team = make_team('KC', players, None, order=order)

	game_init = np.array([[0,0,0,0,0,3,3,0,0],[0,0,3,0,1,4,0,0,0]])
	pre_scenario_dict = {'game':game_init,
		   				  'runs':0,
		   				  'first_base':away_team.players[3],
		   				  'second_base':None,
		   				  'third_base':None,
		   				  'outs':1,
		   				  'top_half':True,
		   				  'inning':7, 
		   				  'away_index':8,
		   				  'home_index':6}

	suc_scenario_dict = {'game':game_init,
		   				  'runs':0,
		   				  'first_base':None,
		   				  'second_base':away_team.players[3],
		   				  'third_base':None,
		   				  'outs':1,
		   				  'top_half':True,
		   				  'inning':7, 
		   				  'away_index':8,
		   				  'home_index':6}

	fail_scenario_dict = {'game':game_init,
		   				  'runs':0,
		   				  'first_base':None,
		   				  'second_base':None,
		   				  'third_base':None,
		   				  'outs':2,
		   				  'top_half':True,
		   				  'inning':7, 
		   				  'away_index':8,
		   				  'home_index':6}		

	steal_scenaro_2019(home_team, away_team, pre_scenario_dict, suc_scenario_dict, fail_scenario_dict, 100000)

def steal_scenario_2():

	players = []

	players.append(make_batter_2019(0, 'castiwe01'))
	players.append(make_batter_2019(1, 'abreujo02'))
	players.append(make_batter_2019(2, 'sanchca01'))
	players.append(make_batter_2019(3, 'anderti01'))
	players.append(make_batter_2019(4, 'moncayo01'))
	players.append(make_batter_2019(5, 'jimenel02'))
	players.append(make_batter_2019(6, 'garcile02'))
	players.append(make_batter_2019(7, 'palkada01'))
	players.append(make_batter_2019(8, 'alonsyo01'))


	order = [6, 4, 1, 8, 5, 3, 0, 7, 2]

	home_team = make_team('CWS', players, None, order=order)

	players = []

	players.append(make_batter_2019(0, 'gallaca01'))
	players.append(make_batter_2019(1, 'ohearry01'))
	players.append(make_batter_2019(2, 'merriwh01'))
	players.append(make_batter_2019(3, 'owingch01'))
	players.append(make_batter_2019(4, 'doziehu01'))
	players.append(make_batter_2019(5, 'gordoal01'))
	players.append(make_batter_2019(6, 'hamilbi02'))
	players.append(make_batter_2019(7, 'solerjo01'))
	players.append(make_batter_2019(8, 'dudalu01'))


	order = [2, 5, 4, 1, 7, 8, 3, 0, 6]

	away_team = make_team('KC', players, None, order=order)

	game_init = np.array([[0,1,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]])
	pre_scenario_dict = {'game':game_init,
		   				  'runs':0,
		   				  'first_base':home_team.players[3],
		   				  'second_base':None,
		   				  'third_base':None,
		   				  'outs':2,
		   				  'top_half':False,
		   				  'inning':2, 
		   				  'away_index':0,
		   				  'home_index':5}

	suc_scenario_dict = {'game':game_init,
		   				  'runs':0,
		   				  'first_base':None,
		   				  'second_base':home_team.players[3],
		   				  'third_base':None,
		   				  'outs':2,
		   				  'top_half':False,
		   				  'inning':2, 
		   				  'away_index':0,
		   				  'home_index':5}

	fail_scenario_dict = {'game':game_init,
		   				  'runs':0,
		   				  'first_base':None,
		   				  'second_base':None,
		   				  'third_base':None,
		   				  'outs':0,
		   				  'top_half':True,
		   				  'inning':3, 
		   				  'away_index':0,
		   				  'home_index':5}		
		   				  
	steal_scenaro_2019(home_team, away_team, pre_scenario_dict, suc_scenario_dict, fail_scenario_dict, 100000)

def steal_scenario_3():

	players = []

	players.append(make_batter_2019(0, 'castiwe01'))
	players.append(make_batter_2019(1, 'alonsyo01'))
	players.append(make_batter_2019(2, 'sanchca01'))
	players.append(make_batter_2019(3, 'anderti01'))
	players.append(make_batter_2019(4, 'moncayo01'))
	players.append(make_batter_2019(5, 'jimenel02'))
	players.append(make_batter_2019(6, 'garcile02'))
	players.append(make_batter_2019(7, 'palkada01'))
	players.append(make_batter_2019(8, 'abreujo02'))


	order = [6, 4, 8, 1, 3, 0, 5, 7, 2]

	home_team = make_team('CWS', players, None, order=order)

	players = []

	players.append(make_batter_2019(0, 'perezmi03'))
	players.append(make_batter_2019(1, 'choiji01'))
	players.append(make_batter_2019(2, 'lowebr01'))
	players.append(make_batter_2019(3, 'adamewi01'))
	players.append(make_batter_2019(4, 'diazya01'))
	players.append(make_batter_2019(5, 'meadoau01'))
	players.append(make_batter_2019(6, 'kiermke01'))
	players.append(make_batter_2019(7, 'garciav01'))
	players.append(make_batter_2019(8, 'phamth01'))


	order = [5, 8, 1, 2, 4, 6, 7, 0, 3]

	away_team = make_team('TB', players, None, order=order)

	game_init = np.array([[1,3,1,2,0,0,0,0,0],[0,0,2,0,0,0,0,0,0]])
	pre_scenario_dict = {'game':game_init,
		   				  'runs':0,
		   				  'first_base':home_team.players[3],
		   				  'second_base':None,
		   				  'third_base':None,
		   				  'outs':2,
		   				  'top_half':False,
		   				  'inning':6, 
		   				  'away_index':2,
		   				  'home_index':5}

	suc_scenario_dict = {'game':game_init,
		   				  'runs':0,
		   				  'first_base':None,
		   				  'second_base':home_team.players[3],
		   				  'third_base':None,
		   				  'outs':2,
		   				  'top_half':False,
		   				  'inning':6, 
		   				  'away_index':2,
		   				  'home_index':5}

	fail_scenario_dict = {'game':game_init,
		   				  'runs':0,
		   				  'first_base':None,
		   				  'second_base':None,
		   				  'third_base':None,
		   				  'outs':0,
		   				  'top_half':True,
		   				  'inning':7, 
		   				  'away_index':2,
		   				  'home_index':5}		
		   				  
	steal_scenaro_2019(home_team, away_team, pre_scenario_dict, suc_scenario_dict, fail_scenario_dict, 100000)

def steal_scenaro_2019(home_team, away_team, pre_scenario_dict, suc_scenario_dict, fail_scenario_dict, n=10000):		  	   				 

	game = Game(home_team=home_team, away_team=away_team, league=mlb_2019()) 
	game.advanced_transition=True
	game.baserunning = True
	runs = []

	away_runs = np.zeros((n, 9))
	home_runs = np.zeros((n, 9))
	for i in range(n):
		game.set_scenario(**pre_scenario_dict)
		game_results = game.sim_scenario(debug=False)
		away_runs[i,:] = game_results[0,:]
		home_runs[i,:] = game_results[1,:]

	pre_away_exp_runs = confidence_interval_99(np.sum(away_runs, axis=1))
	pre_home_exp_runs = confidence_interval_99(np.sum(home_runs, axis=1))
	pre_away_win_probability = win_probability(away_runs, home_runs)
	print('----- Pre-Steal -------')
	print('Away Runs (BR) (MCMC):  %f +/- %f' % pre_away_exp_runs)
	print('Home Runs (BR) (MCMC):  %f +/- %f' % pre_home_exp_runs)
	print('Away Win Probability: %f' % pre_away_win_probability)

	away_runs = np.zeros((n, 9))
	home_runs = np.zeros((n, 9))
	for i in range(n):
		game.set_scenario(**suc_scenario_dict)
		game_results = game.sim_scenario(debug=False)
		away_runs[i,:] = game_results[0,:]
		home_runs[i,:] = game_results[1,:]

	
	suc_away_exp_runs = confidence_interval_99(np.sum(away_runs, axis=1))
	suc_home_exp_runs = confidence_interval_99(np.sum(home_runs, axis=1))
	suc_away_win_probability = win_probability(away_runs, home_runs)
	print('----- Stole 2nd -------')
	print('Away (BR) (MCMC):  %f +/- %f' % suc_away_exp_runs)
	print('Home (BR) (MCMC):  %f +/- %f' % suc_home_exp_runs)
	print('Away Probability: %f' % suc_away_win_probability)

	away_runs = np.zeros((n, 9))
	home_runs = np.zeros((n, 9))
	for i in range(n):
		game.set_scenario(**fail_scenario_dict)
		game_results = game.sim_scenario(debug=False)
		away_runs[i,:] = game_results[0,:]
		home_runs[i,:] = game_results[1,:]

	
	fail_away_exp_runs = confidence_interval_99(np.sum(away_runs, axis=1))
	fail_home_exp_runs = confidence_interval_99(np.sum(home_runs, axis=1))
	fail_away_win_probability = win_probability(away_runs, home_runs)
	print('----- Caught Stealing -------')
	print('Away (BR) (MCMC):  %f +/- %f' % fail_away_exp_runs)
	print('Home (BR) (MCMC):  %f +/- %f' % fail_home_exp_runs)
	print('Away Probability: %f' % fail_away_win_probability)

	ta_steal_prob = 68/(68+16)

	steal_away_exp_runs = ta_steal_prob * suc_away_exp_runs[0] + (1 - ta_steal_prob) * fail_away_exp_runs[0]
	steal_home_exp_runs = ta_steal_prob * suc_home_exp_runs[0] + (1 - ta_steal_prob) * fail_home_exp_runs[0]
	steal_away_win_probability = ta_steal_prob * suc_away_win_probability + (1 - ta_steal_prob) * fail_away_win_probability
	print('----- Stealing -------')
	print('Away (BR) (MCMC):  %f' % steal_away_exp_runs)
	print('Home (BR) (MCMC):  %f' % steal_home_exp_runs)
	print('Away Probability: %f' % steal_away_win_probability)

	print('Steal Change in Away Runs: %f' % (steal_away_exp_runs - pre_away_exp_runs[0]))
	print('Steal Change in Home Runs: %f' % (steal_home_exp_runs - pre_home_exp_runs[0]))
	print('Steal Change in Win Probability: %f' % (steal_away_win_probability - pre_away_win_probability))

if __name__ == '__main__':
	# comparison_MC_MCMC_89Braves()
	# comparison_advanced_2019CWS()
	# tim_anderson_stats()
	# comparison_stealing_2019()
	# comparison_stealing_2020()
	# steal_scenario_1()
	steal_scenario_2()
	steal_scenario_3()