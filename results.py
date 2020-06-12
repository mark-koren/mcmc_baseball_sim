import numpy as np
import pdb
import matplotlib.pyplot as plt
from pprint import pprint
import pandas as pd
import progressbar
import multiprocessing as mp

from project import *
from data import *
from retrosheet_parse import *
from utils import *

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
    run_dist = u[0, 21 * 8:].T
    runs = np.arange(21)
    print('Braves Runs (MC): ', np.dot(runs, run_dist))

    braves_runs = np.zeros((2 * n, 9))

    for i in range(n):
        game_results = game.sim_game(debug=False)
        braves_runs[i, :] = game_results[0, :]
        braves_runs[n + i, :] = game_results[1, :]

    print('CWS Runs (Basic) (MCMC):  %f +/- %f' % confidence_interval_99(np.sum(braves_runs, axis=1)))

    game.advanced_transition = True

    u = game.sim_game_markov()
    run_dist = u[0, 21 * 8:].T
    runs = np.arange(21)
    print('Braves Runs (Adv) (MC): ', np.dot(runs, run_dist))

    braves_runs = np.zeros((2 * n, 9))

    for i in range(n):
        game_results = game.sim_game(debug=False)
        braves_runs[i, :] = game_results[0, :]
        braves_runs[n + i, :] = game_results[1, :]

    print('CWS Runs (Basic) (MCMC):  %f +/- %f' % confidence_interval_99(np.sum(braves_runs, axis=1)))


def braves_scoring_index():
    braves = braves_1989()

    game = Game(home_team=braves, away_team=braves, league=mlb_1989())
    n = 10000

    for i in range(9):
        braves.order = [i]
        game = Game()
        game.home_team = braves
        game.away_team = braves
        u = game.sim_inning_markov()
        run_dist = u[:, -1].T
        runs = np.arange(20)
        print('Scoring Index (MC): ', np.dot(runs, run_dist))

        n = 10000
        braves_runs = np.zeros((2 * n, 9))
        for j in range(n):
            game_results = game.sim_game(debug=False)
            braves_runs[j, :] = game_results[0, :]
            braves_runs[n + j, :] = game_results[1, :]

        print('Scoring Index (MCMC): ', np.mean(braves_runs[:, 0], axis=0))


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
    run_dist = u[0, 21 * 8:].T
    runs = np.arange(21)
    print('CWS Runs (Basic) (MC): ', np.dot(runs, run_dist))

    n = 10000
    cws_runs = np.zeros((2 * n, 9))
    for i in range(n):
        game_results = game.sim_game(debug=False)
        cws_runs[i, :] = game_results[0, :]
        cws_runs[n + i, :] = game_results[1, :]

    print('CWS Runs (Basic) (MCMC):  %f +/- %f' % confidence_interval_99(np.sum(cws_runs, axis=1)))

    game.advanced_transition = True

    u = game.sim_game_markov()
    run_dist = u[0, 21 * 8:].T
    runs = np.arange(21)
    print('CWS Runs (Adv) (MC): ', np.dot(runs, run_dist))

    n = 10000
    cws_runs = np.zeros((2 * n, 9))
    for i in range(n):
        game_results = game.sim_game(debug=False)
        cws_runs[i, :] = game_results[0, :]
        cws_runs[n + i, :] = game_results[1, :]

    print('CWS Runs (Adv) (MCMC):  %f +/- %f' % confidence_interval_99(np.sum(cws_runs, axis=1)))

    game.baserunning = True
    game.advanced_transition = False

    n = 10000
    cws_runs = np.zeros((2 * n, 9))
    for i in range(n):
        game_results = game.sim_game(debug=False)
        cws_runs[i, :] = game_results[0, :]
        cws_runs[n + i, :] = game_results[1, :]

    print('CWS Runs (BR) (MCMC):  %f +/- %f' % confidence_interval_99(np.sum(cws_runs, axis=1)))

    game.baserunning = True
    game.advanced_transition = True

    n = 10000
    cws_runs = np.zeros((2 * n, 9))
    for i in range(n):
        game_results = game.sim_game(debug=False)
        cws_runs[i, :] = game_results[0, :]
        cws_runs[n + i, :] = game_results[1, :]

    print('CWS Runs (Adv) (BR) (MCMC):  %f +/- %f' % confidence_interval_99(np.sum(cws_runs, axis=1)))


def comparison_baserunning_19cws():
    cws = chicago_whitesox_2019()

    game = Game(home_team=cws, away_team=cws, league=mlb_2019())
    game.advanced_transition = True
    game.baserunning = False

    u = game.sim_game_markov()
    run_dist = u[0, 21 * 8:].T
    runs = np.arange(21)
    print('Braves Runs (MC): ', np.dot(runs, run_dist))

    n = 10000
    braves_runs = np.zeros((2 * n, 9))
    for i in range(n):
        game_results = game.sim_game(debug=False)
        braves_runs[i, :] = game_results[0, :]
        braves_runs[n + i, :] = game_results[1, :]

    print('Braves Runs (MCMC): ', np.mean(np.sum(braves_runs, axis=1)))

    game.baserunning = True

    n = 10000
    braves_runs = np.zeros((2 * n, 9))
    for i in range(n):
        game_results = game.sim_game(debug=False)
        braves_runs[i, :] = game_results[0, :]
        braves_runs[n + i, :] = game_results[1, :]

    print('Braves Runs With baserunning (MCMC): ', np.mean(np.sum(braves_runs, axis=1)))


def comparison_stealing_2019():
    cws = chicago_whitesox_2019()

    game = Game(home_team=cws, away_team=cws, league=mlb_2019())
    game.advanced_transition = True
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

        game.sim_half_inning(initial_setup=True, debug=False)
        cws_runs[i, :] = game.runs

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

        game.sim_half_inning(initial_setup=True, debug=False)
        cws_runs[i, :] = game.runs

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

        game.sim_half_inning(initial_setup=True, debug=False)
        cws_runs[i, :] = game.runs

    print('CWS runs 2019 (Caught Stealing) (MCMC): ', np.mean(cws_runs))
    print('CWS P(1 run) 2019 (MCMC): ', cws_runs[np.where(cws_runs > 0)].shape[0] / cws_runs.shape[0])
    # plt.hist(cws_runs)
    # plt.show()
    runs.append(cws_runs)

    ta_steal_prob = 68 / (68 + 16)

    runs.append(runs[1] * ta_steal_prob + runs[2] * (1 - ta_steal_prob))

    print('CWS runs 2019 (Stealing) (MCMC): ', np.mean(runs[-1]))
    print('CWS P(1 run) 2019 (MCMC): ',
          runs[1][np.where(runs[1] > 0)].shape[0] / runs[1].shape[0] * ta_steal_prob +
          runs[2][np.where(runs[2] > 0)].shape[0] / runs[2].shape[0] * (1 - ta_steal_prob))

    xx = np.array(runs).reshape((4, -1))
    plt.hist(xx.T, bins=[0, 1, 2, 3, 4, 5, 6], density=True, histtype='bar', align='left',
             label=['TA on 1st, 0 Outs', 'TA on 2nd, 0 Outs', 'No one on, 1 Outs', 'Stealing'])
    plt.legend()
    plt.xlabel('Runs in Inning')
    plt.ylabel('Probability')
    plt.show()


def comparison_stealing_2020():
    cws = chicago_whitesox_2020()

    game = Game(home_team=cws, away_team=cws, league=mlb_2019())
    game.advanced_transition = True
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

        game.sim_half_inning(initial_setup=True, debug=False)
        cws_runs[i, :] = game.runs

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

        game.sim_half_inning(initial_setup=True, debug=False)
        cws_runs[i, :] = game.runs

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

        game.sim_half_inning(initial_setup=True, debug=False)
        cws_runs[i, :] = game.runs

    print('CWS runs 2020 (Caught Stealing) (MCMC): ', np.mean(cws_runs))
    print('CWS P(1 run) 2020 (MCMC): ', cws_runs[np.where(cws_runs > 0)].shape[0] / cws_runs.shape[0])
    # plt.hist(cws_runs)
    # plt.show()
    runs.append(cws_runs)

    ta_steal_prob = 68 / (68 + 16)

    runs.append(runs[1] * ta_steal_prob + runs[2] * (1 - ta_steal_prob))

    print('CWS runs 2020 (Stealing) (MCMC): ', np.mean(runs[-1]))
    print('CWS P(1 run) 2020 (MCMC): ',
          runs[1][np.where(runs[1] > 0)].shape[0] / runs[1].shape[0] * ta_steal_prob +
          runs[2][np.where(runs[2] > 0)].shape[0] / runs[2].shape[0] * (1 - ta_steal_prob))

    xx = np.array(runs).reshape((4, -1))
    plt.hist(xx.T, bins=[0, 1, 2, 3, 4, 5, 6], density=True, histtype='bar', align='left',
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

    game_init = np.array([[0, 0, 0, 0, 0, 3, 3, 0, 0], [0, 0, 3, 0, 1, 4, 0, 0, 0]])
    pre_scenario_dict = {'game': game_init,
                         'runs': 0,
                         'first_base': away_team.players[3],
                         'second_base': None,
                         'third_base': None,
                         'outs': 1,
                         'top_half': True,
                         'inning': 7,
                         'away_index': 8,
                         'home_index': 6}

    suc_scenario_dict = {'game': game_init,
                         'runs': 0,
                         'first_base': None,
                         'second_base': away_team.players[3],
                         'third_base': None,
                         'outs': 1,
                         'top_half': True,
                         'inning': 7,
                         'away_index': 8,
                         'home_index': 6}

    fail_scenario_dict = {'game': game_init,
                          'runs': 0,
                          'first_base': None,
                          'second_base': None,
                          'third_base': None,
                          'outs': 2,
                          'top_half': True,
                          'inning': 7,
                          'away_index': 8,
                          'home_index': 6}

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

    game_init = np.array([[0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]])
    pre_scenario_dict = {'game': game_init,
                         'runs': 0,
                         'first_base': home_team.players[3],
                         'second_base': None,
                         'third_base': None,
                         'outs': 2,
                         'top_half': False,
                         'inning': 2,
                         'away_index': 0,
                         'home_index': 5}

    suc_scenario_dict = {'game': game_init,
                         'runs': 0,
                         'first_base': None,
                         'second_base': home_team.players[3],
                         'third_base': None,
                         'outs': 2,
                         'top_half': False,
                         'inning': 2,
                         'away_index': 0,
                         'home_index': 5}

    fail_scenario_dict = {'game': game_init,
                          'runs': 0,
                          'first_base': None,
                          'second_base': None,
                          'third_base': None,
                          'outs': 0,
                          'top_half': True,
                          'inning': 3,
                          'away_index': 0,
                          'home_index': 5}

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

    game_init = np.array([[1, 3, 1, 2, 0, 0, 0, 0, 0], [0, 0, 2, 0, 0, 0, 0, 0, 0]])
    pre_scenario_dict = {'game': game_init,
                         'runs': 0,
                         'first_base': home_team.players[3],
                         'second_base': None,
                         'third_base': None,
                         'outs': 2,
                         'top_half': False,
                         'inning': 6,
                         'away_index': 2,
                         'home_index': 5}

    suc_scenario_dict = {'game': game_init,
                         'runs': 0,
                         'first_base': None,
                         'second_base': home_team.players[3],
                         'third_base': None,
                         'outs': 2,
                         'top_half': False,
                         'inning': 6,
                         'away_index': 2,
                         'home_index': 5}

    fail_scenario_dict = {'game': game_init,
                          'runs': 0,
                          'first_base': None,
                          'second_base': None,
                          'third_base': None,
                          'outs': 0,
                          'top_half': True,
                          'inning': 7,
                          'away_index': 2,
                          'home_index': 5}

    steal_scenaro_2019(home_team, away_team, pre_scenario_dict, suc_scenario_dict, fail_scenario_dict, 100000)


def steal_scenaro_2019(home_team, away_team, pre_scenario_dict, suc_scenario_dict, fail_scenario_dict, n=10000):
    game = Game(home_team=home_team, away_team=away_team, league=mlb_2019())
    game.advanced_transition = True
    game.baserunning = True
    runs = []

    away_runs = np.zeros((n, 9))
    home_runs = np.zeros((n, 9))
    for i in range(n):
        game.set_scenario(**pre_scenario_dict)
        game_results = game.sim_scenario(debug=False)
        away_runs[i, :] = game_results[0, :]
        home_runs[i, :] = game_results[1, :]

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
        away_runs[i, :] = game_results[0, :]
        home_runs[i, :] = game_results[1, :]

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
        away_runs[i, :] = game_results[0, :]
        home_runs[i, :] = game_results[1, :]

    fail_away_exp_runs = confidence_interval_99(np.sum(away_runs, axis=1))
    fail_home_exp_runs = confidence_interval_99(np.sum(home_runs, axis=1))
    fail_away_win_probability = win_probability(away_runs, home_runs)
    print('----- Caught Stealing -------')
    print('Away (BR) (MCMC):  %f +/- %f' % fail_away_exp_runs)
    print('Home (BR) (MCMC):  %f +/- %f' % fail_home_exp_runs)
    print('Away Probability: %f' % fail_away_win_probability)

    ta_steal_prob = 68 / (68 + 16)

    steal_away_exp_runs = ta_steal_prob * suc_away_exp_runs[0] + (1 - ta_steal_prob) * fail_away_exp_runs[0]
    steal_home_exp_runs = ta_steal_prob * suc_home_exp_runs[0] + (1 - ta_steal_prob) * fail_home_exp_runs[0]
    steal_away_win_probability = ta_steal_prob * suc_away_win_probability + (
                1 - ta_steal_prob) * fail_away_win_probability
    print('----- Stealing -------')
    print('Away (BR) (MCMC):  %f' % steal_away_exp_runs)
    print('Home (BR) (MCMC):  %f' % steal_home_exp_runs)
    print('Away Probability: %f' % steal_away_win_probability)

    print('Steal Change in Away Runs: %f' % (steal_away_exp_runs - pre_away_exp_runs[0]))
    print('Steal Change in Home Runs: %f' % (steal_home_exp_runs - pre_home_exp_runs[0]))
    print('Steal Change in Win Probability: %f' % (steal_away_win_probability - pre_away_win_probability))


def simulate_season_for_team(team_name='CHA'):
    ros_path = './data/retrosheet_pbp/2019'
    eva_path = './data/retrosheet_pbp/2019'
    ros_filename = team_name + '2019.ROS'
    df_batters = pd.read_csv('./data/retrosheet_pbp/2019_batter.csv', index_col='player_id')
    df_pitchers = pd.read_csv('./data/retrosheet_pbp/2019_pitcher.csv', index_col='player_id')
    df_teams = pd.read_csv('./data/retrosheet_pbp/2019_team.csv', index_col='team_id')
    df_bga = load_retrosheet_bga_as_df('2019MLB.BGA', './data/retrosheet_pbp/2019')
    df_bev = load_retrosheet_bev_as_df('2019MLB.BEV', './data/retrosheet_pbp/2019')
    df_fatigue = pd.read_csv('./data/retrosheet_pbp/2019_fatigue.csv')
    event_num = 1
    team_id = 'CHA'
    # home_game_id_list = df_bga[df_bga.index.str.contains(team_id)].index.unique()
    # away_game_id_list = df_bga[df_bga.loc[:,'visiting_team'].str.contains(team_id)].index.unique()
    existing_league_dict = {}
    existing_team_dict = {}
    existing_player_dict = {}
    game_id_list = df_bga[
        df_bga.loc[:, 'visiting_team'].str.contains(team_id) | df_bga.index.str.contains(team_id)].index.unique()
    game_list = []
    for game_id in game_id_list:
        game = game_from_game_id(game_id, event_num, df_bev, df_bga, df_batters, df_pitchers, df_teams, df_fatigue,
                                 ros_path, eva_path, existing_league_dict, existing_team_dict, existing_player_dict)
        game.advanced_transition = True
        game.baserunning = True
        game.diagnostics = False
        game_list.append(game)

    max_seasons = 1000
    results = np.zeros((3, max_seasons))
    for season_idx in range(max_seasons):
        wins = 0
        runs = 0
        runs_against = 0
        for game in game_list:
            game_copy = copy.deepcopy(game)
            game_results = game_copy.sim_game(reset=False, allow_extra_innings=True)
            away_runs = np.sum(game_results[0, :])
            home_runs = np.sum(game_results[1, :])
            if game.home_team.name == team_id:
                runs += home_runs
                runs_against += away_runs
                if home_runs > away_runs:
                    wins += 1
            else:
                runs += away_runs
                runs_against += home_runs
                if away_runs > home_runs:
                    wins += 1
        results[0, season_idx] = wins
        results[1, season_idx] = runs / 162
        results[2, season_idx] = runs_against / 162
    pprint(np.sum(results, axis=1))

PLAYER_COLUMN_NAMES = ['player_id',
					   'singles',
					   'doubles',
					   'triples',
					   'homeruns',
					   'walks',
					   'hbps',
					   'errors',
					   'outs',
					   's31st',
					   'dh1st',
					   'sh2nd',
					   'productive_outs',
					   'double_plays',
					   'runs']

def simulate_season_for_all():
    ros_path = './data/retrosheet_pbp/2019'
    eva_path = './data/retrosheet_pbp/2019'

    df_batters = pd.read_csv('./data/retrosheet_pbp/2019_batter.csv', index_col='player_id')
    df_pitchers = pd.read_csv('./data/retrosheet_pbp/2019_pitcher.csv', index_col='player_id')
    df_teams = pd.read_csv('./data/retrosheet_pbp/2019_team.csv', index_col='team_id')
    df_bga = load_retrosheet_bga_as_df('2019MLB.BGA', './data/retrosheet_pbp/2019')
    df_bev = load_retrosheet_bev_as_df('2019MLB.BEV', './data/retrosheet_pbp/2019')
    df_fatigue = pd.read_csv('./data/retrosheet_pbp/2019_fatigue.csv')
    event_num = 1
    team_id = 'CHA'
    # home_game_id_list = df_bga[df_bga.index.str.contains(team_id)].index.unique()
    # away_game_id_list = df_bga[df_bga.loc[:,'visiting_team'].str.contains(team_id)].index.unique()
    existing_league_dict = {}
    existing_team_dict = {}
    existing_player_dict = {}
    # game_id_list = df_bga[df_bga.loc[:,'visiting_team'].str.contains(team_id) | df_bga.index.str.contains(team_id)].index.unique()
    full_game_id_list = df_bga.index.unique()
    game_list = []
    print('Building Seasons')
    bar = progressbar.ProgressBar(maxval=len(full_game_id_list),
                                  widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()

    for counter, game_id in enumerate(full_game_id_list):
        bar.update(counter)
        game = game_from_game_id(game_id, event_num, df_bev, df_bga, df_batters, df_pitchers, df_teams, df_fatigue,
                                 ros_path, eva_path, existing_league_dict, existing_team_dict, existing_player_dict)
        game.advanced_transition = True
        game.advanced_league = True
        game.baserunning = True
        game.diagnostics = False
        game.collect_stats = True
        game.collect_player_stats = True
        game_list.append(game)
    bar.finish()

    max_seasons = 100
    print('Simulating Seasons')
    bar = progressbar.ProgressBar(maxval=max_seasons,
                                  widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    results = {}
    results2 = {}
    team_id_list = df_bga.loc[:, 'visiting_team'].unique()
    for team_id in team_id_list:
        results[team_id] = np.zeros((3, max_seasons))
        results2[team_id] = np.zeros((3))

    results_list = [results2]*100

    stats = {'singles': np.zeros((max_seasons)),
             'doubles': np.zeros((max_seasons)),
             'triples': np.zeros((max_seasons)),
             'homeruns': np.zeros((max_seasons)),
             'walks': np.zeros((max_seasons)),
             'hbps': np.zeros((max_seasons)),
             'errors': np.zeros((max_seasons)),
             'outs': np.zeros((max_seasons)),
             's31st': np.zeros((max_seasons)),
             'dh1st': np.zeros((max_seasons)),
             'sh2nd': np.zeros((max_seasons)),
             'productive_outs': np.zeros((max_seasons)),
             'double_plays': np.zeros((max_seasons)),
             'runs': np.zeros((max_seasons)), }

    stats_list = [{'singles': 0,
             'doubles':0,
             'triples': 0,
             'homeruns': 0,
             'walks': 0,
             'hbps': 0,
             'errors': 0,
             'outs': 0,
             's31st': 0,
             'dh1st': 0,
             'sh2nd': 0,
             'productive_outs': 0,
             'double_plays': 0,
             'runs': 0, }]*max_seasons

    batter_stats = pd.DataFrame(columns=PLAYER_COLUMN_NAMES)
    batter_stats = batter_stats.set_index('player_id')
    pitcher_stats = pd.DataFrame(columns=PLAYER_COLUMN_NAMES)
    pitcher_stats = pitcher_stats.set_index('player_id')

    batter_stats_list = []
    pitcher_stats_list = []
    for i in range(max_seasons):
        batter_stats_list.append(copy.deepcopy(batter_stats))
        pitcher_stats_list.append(copy.deepcopy(pitcher_stats))

    def _simulate_season(season_idx, game_list, batter_stats, pitcher_stats, results, stats):
        for game in game_list:
            game_copy = copy.deepcopy(game)
            game_copy.batter_stats = batter_stats #batter_stats_list[season_idx]
            game_copy.pitcher_stats = pitcher_stats #pitcher_stats_list[season_idx]

            game_results = game_copy.sim_game(reset=False, allow_extra_innings=True)

            batter_stats = game_copy.batter_stats
            pitcher_stats = game_copy.pitcher_stats

            away_runs = np.sum(game_results[0, :])
            home_runs = np.sum(game_results[1, :])

            home_team_results = results[game_copy.home_team.name]
            away_team_results = results[game_copy.away_team.name]

            home_team_results[0] += 1 if home_runs > away_runs else 0 # home_team_results[0, season_idx]
            away_team_results[0] += 1 if away_runs > home_runs else 0 # away_team_results[0, season_idx]

            home_team_results[1] += home_runs
            away_team_results[1] += away_runs

            home_team_results[2] += away_runs
            away_team_results[2] += home_runs

            for key in game_copy.home_stats.keys():
                stats[key] += game_copy.home_stats[key] # stats[key][season_idx]

            for key in game_copy.away_stats.keys():
                stats[key] += game_copy.away_stats[key]

        return (season_idx, batter_stats, pitcher_stats, stats, results)

    def _process_async_results(results_tuple_list):
        batter_stats_list = []
        pitcher_stats_list = []

        stats = {}
        for key in results_tuple_list[0][3].keys():
            stats[key] = np.zeros(len(results_tuple_list))

        results = {}
        for team_id in results_tuple_list[0][4].keys():
            results[team_id] = np.zeros((3, len(results_tuple_list)))

        for season_idx in range(len(results_tuple_list)):
            batter_stats_list.append(results_tuple_list[season_idx][1])
            pitcher_stats_list.append(results_tuple_list[season_idx][2])

            for key in stats.keys():
                stats[key][season_idx] = results_tuple_list[season_idx][3][key]

            for team_id in results.keys():
                results[team_id][:, season_idx] = results_tuple_list[season_idx][4][team_id]

        return batter_stats_list, pitcher_stats_list, stats, results



    
    pool = mp.Pool(mp.cpu_count())
    # pool = mp.Pool(2)
    results = pool.starmap_async(_simulate_season,
                                 [(i,
                                   game_list,
                                   batter_stats_list[i],
                                   pitcher_stats_list[i],
                                   results_list[i],
                                   stats_list[i]) for i in range(max_seasons)]).get()

    pool.close()
    pool.join()
    batter_stats_list, pitcher_stats_list, stats, results = _process_async_results(results)

    # for season_idx in range(max_seasons):
    #     bar.update(season_idx)
    #     wins = 0
    #     runs = 0
    #     runs_against = 0
    #     for game in game_list:
    #
    #         game_copy = copy.deepcopy(game)
    #         game_copy.batter_stats = batter_stats_list[season_idx]
    #         game_copy.pitcher_stats = pitcher_stats_list[season_idx]
    #
    #         game_results = game_copy.sim_game(reset=False, allow_extra_innings=True)
    #
    #         batter_stats_list[season_idx] = game_copy.batter_stats
    #         pitcher_stats_list[season_idx] = game_copy.pitcher_stats
    #
    #         away_runs = np.sum(game_results[0, :])
    #         home_runs = np.sum(game_results[1, :])
    #
    #         home_team_results = results[game_copy.home_team.name]
    #         away_team_results = results[game_copy.away_team.name]
    #
    #         home_team_results[0, season_idx] += 1 if home_runs > away_runs else 0
    #         away_team_results[0, season_idx] += 1 if away_runs > home_runs else 0
    #
    #         home_team_results[1, season_idx] += home_runs
    #         away_team_results[1, season_idx] += away_runs
    #
    #         home_team_results[2, season_idx] += away_runs
    #         away_team_results[2, season_idx] += home_runs
    #
    #         for key in game_copy.home_stats.keys():
    #             stats[key][season_idx] += game_copy.home_stats[key]
    #
    #         for key in game_copy.away_stats.keys():
    #             stats[key][season_idx] += game_copy.away_stats[key]



        # print(results[game_copy.home_team.name][:, season_idx], home_team_results[:, season_idx])
        # print(results[game_copy.away_team.name][:, season_idx], away_team_results[:, season_idx])
        #
        # results[game_copy.home_team.name] = home_team_results
        # results[game_copy.away_team.name] = away_team_results

    mean_results = {}
    bar.finish()
    for team_id in team_id_list:
        results[team_id][1:, :] /= 162
        mean_results[team_id] = np.mean(results[team_id], axis=1)
    pprint(mean_results)

    mean_stats = {}
    average_stats_2019 = {'singles': 42039 - 8531 - 785 - 6776,
                          'doubles': 8531,
                          'triples': 785,
                          'homeruns': 6776,
                          'walks': 15895,
                          'hbps': 1984,
                          'errors': 2898,
                          'outs': 166651 - 42039,
                          's31st': 2454,
                          'dh1st': 1037,
                          'sh2nd': 2903,
                          'productive_outs': 4372,
                          'double_plays': 3463,
                          'runs': 23467}
    fig, axs = plt.subplots(5, 3)
    i = 0
    j = 0
    for key in stats.keys():
        mean_stats[key] = np.mean(stats[key])
        axs[i, j].hist(stats[key])
        axs[i, j].axvline(x=mean_stats[key], linestyle='--', color='#FF0000')
        axs[i, j].axvline(x=average_stats_2019[key], linestyle=':', color='#000000')
        axs[i, j].set_title(key)
        j = j + 1
        if j > 2:
            j = 0
            i = i + 1
    pprint(mean_stats)
    plt.show()

    for df in batter_stats_list:
        df['batting_average'] = df.apply(lambda x: batting_average(x['singles'], x['doubles'], x['triples'], x['homeruns'], x['outs']), axis=1)
        df['on_base_percentage'] = df.apply(
            lambda x: on_base_percentage(x['singles'], x['doubles'], x['triples'], x['homeruns'], x['walks'], x['outs']), axis=1)
        df['at_bats'] = df.apply(lambda x: at_bats(x['singles'], x['doubles'], x['triples'], x['homeruns'], x['outs']), axis=1)
        df['plate_appearances'] = df.apply(lambda x: plate_appearances(x['singles'], x['doubles'], x['triples'], x['homeruns'], x['walks'], x['outs']), axis=1)

    for df in pitcher_stats_list:
        df['batting_average'] = df.apply(lambda x: batting_average(x['singles'], x['doubles'], x['triples'], x['homeruns'], x['outs']), axis=1)
        df['on_base_percentage'] = df.apply(
            lambda x: on_base_percentage(x['singles'], x['doubles'], x['triples'], x['homeruns'], x['walks'], x['outs']), axis=1)
        df['at_bats'] = df.apply(lambda x: at_bats(x['singles'], x['doubles'], x['triples'], x['homeruns'], x['outs']), axis=1)
        df['plate_appearances'] = df.apply(lambda x: plate_appearances(x['singles'], x['doubles'], x['triples'], x['homeruns'], x['walks'], x['outs']), axis=1)

    division_pennants = {}
    al_central = ['CHA', 'CLE', 'KCA', 'DET', 'MIN']
    al_central_wins = np.vstack([results[al_central[0]][0,:],
                                 results[al_central[1]][0,:],
                                 results[al_central[2]][0,:],
                                 results[al_central[3]][0,:],
                                 results[al_central[4]][0,:]])
    al_central_pennants = np.argmax(al_central_wins, axis=0)
    for team_id in al_central:
        division_pennants[team_id] = np.count_nonzero(
            np.argmax(al_central_wins, axis=0) == al_central.index(team_id))

    al_east = ['BOS', 'BAL', 'TOR', 'NYA', 'TBA']
    al_east_wins = np.vstack([results[al_east[0]][0, :],
                                 results[al_east[1]][0, :],
                                 results[al_east[2]][0, :],
                                 results[al_east[3]][0, :],
                                 results[al_east[4]][0, :]])
    al_east_pennants = np.argmax(al_east_wins, axis=0)
    for team_id in al_east:
        division_pennants[team_id] = np.count_nonzero(
            np.argmax(al_east_wins, axis=0) == al_east.index(team_id))
    
    al_west = ['TEX', 'ANA', 'OAK', 'HOU', 'SEA']
    al_west_wins = np.vstack([results[al_west[0]][0, :],
                                 results[al_west[1]][0, :],
                                 results[al_west[2]][0, :],
                                 results[al_west[3]][0, :],
                                 results[al_west[4]][0, :]])
    al_west_pennants = np.argmax(al_west_wins, axis=0)
    for team_id in al_west:
        division_pennants[team_id] = np.count_nonzero(
            np.argmax(al_west_wins, axis=0) == al_west.index(team_id))

    nl_central = ['CHN', 'CIN', 'SLN', 'MIL', 'PIT']
    nl_central_wins = np.vstack([results[nl_central[0]][0, :],
                                 results[nl_central[1]][0, :],
                                 results[nl_central[2]][0, :],
                                 results[nl_central[3]][0, :],
                                 results[nl_central[4]][0, :]])
    nl_central_pennants = np.argmax(nl_central_wins, axis=0)
    for team_id in nl_central:
        division_pennants[team_id] = np.count_nonzero(
            np.argmax(nl_central_wins, axis=0) == nl_central.index(team_id))
    
    nl_east = ['PHI', 'NYN', 'MIA', 'WAS', 'ATL']
    nl_east_wins = np.vstack([results[nl_east[0]][0, :],
                                 results[nl_east[1]][0, :],
                                 results[nl_east[2]][0, :],
                                 results[nl_east[3]][0, :],
                                 results[nl_east[4]][0, :]])
    nl_east_pennants = np.argmax(nl_east_wins, axis=0)
    for team_id in nl_east:
        division_pennants[team_id] = np.count_nonzero(
            np.argmax(nl_east_wins, axis=0) == nl_east.index(team_id))
    
    nl_west = ['ARI', 'LAN', 'COL', 'SDN', 'SFN']
    nl_west_wins = np.vstack([results[nl_west[0]][0, :],
                                 results[nl_west[1]][0, :],
                                 results[nl_west[2]][0, :],
                                 results[nl_west[3]][0, :],
                                 results[nl_west[4]][0, :]])
    nl_west_pennants = np.argmax(nl_west_wins, axis=0)
    for team_id in nl_west:
        division_pennants[team_id] = np.count_nonzero(
            np.argmax(nl_west_wins, axis=0) == nl_west.index(team_id))
    
    pprint(division_pennants)


def get_table_data():
    ros_path = './data/retrosheet_pbp/2019'
    eva_path = './data/retrosheet_pbp/2019'

    df_batters = pd.read_csv('./data/retrosheet_pbp/2019_batter.csv', index_col='player_id')
    df_pitchers = pd.read_csv('./data/retrosheet_pbp/2019_pitcher.csv', index_col='player_id')
    df_teams = pd.read_csv('./data/retrosheet_pbp/2019_team.csv', index_col='team_id')
    df_bga = load_retrosheet_bga_as_df('2019MLB.BGA', './data/retrosheet_pbp/2019')
    df_bev = load_retrosheet_bev_as_df('2019MLB.BEV', './data/retrosheet_pbp/2019')
    df_fatigue = pd.read_csv('./data/retrosheet_pbp/2019_fatigue.csv')
    batter_id = 'andet001'
    good_pitcher_r_id = 'coleg001'
    good_pitcher_l_id = 'ryu-h001'
    bad_pitcher_r_id = 'loper003'
    bad_pitcher_l_id = 'kikuy001'
    league = build_league_from_game_id(df_teams)
    tim_anderson = build_player_from_retrosheet_data(batter_id, df_batters, df_pitchers)

    gerrit_cole = build_player_from_retrosheet_data(good_pitcher_r_id, df_batters, df_pitchers)
    hyun_jin_ryu = build_player_from_retrosheet_data(good_pitcher_l_id, df_batters, df_pitchers)

    reynaldo_lopez = build_player_from_retrosheet_data(bad_pitcher_r_id, df_batters, df_pitchers)
    yusei_kikuchi = build_player_from_retrosheet_data(bad_pitcher_l_id, df_batters, df_pitchers)

    game = Game()
    game.advanced_transition = True
    game.advanced_league = True
    game.baserunning = True
    game.league = league
    game.batter = tim_anderson

    game.pitcher = gerrit_cole
    game.update_transition()
    print('GC', game.single, game.double, game.triple, game.homerun, game.walk, game.out,
          (game.single + game.double + game.triple + game.homerun),
          (game.single + game.double + game.triple + game.homerun + game.walk))

    game.pitcher = hyun_jin_ryu
    game.update_transition()
    print('HJR', game.single, game.double, game.triple, game.homerun, game.walk, game.out,
          (game.single + game.double + game.triple + game.homerun),
          (game.single + game.double + game.triple + game.homerun + game.walk))

    game.pitcher = reynaldo_lopez
    game.update_transition()
    print('RL', game.single, game.double, game.triple, game.homerun, game.walk, game.out,
          (game.single + game.double + game.triple + game.homerun),
          (game.single + game.double + game.triple + game.homerun + game.walk))

    game.pitcher = yusei_kikuchi
    game.update_transition()
    print('YK', game.single, game.double, game.triple, game.homerun, game.walk, game.out,
          (game.single + game.double + game.triple + game.homerun),
          (game.single + game.double + game.triple + game.homerun + game.walk))


if __name__ == '__main__':
    # comparison_MC_MCMC_89Braves()
    # comparison_advanced_2019CWS()
    # tim_anderson_stats()
    # comparison_stealing_2019()
    # comparison_stealing_2020()
    # steal_scenario_1()
    # steal_scenario_2()
    # steal_scenario_3()
    # simulate_season_for_team(team_name='CHA')
    simulate_season_for_all()
