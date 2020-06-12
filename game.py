import numpy as np
import pdb
from pprint import pprint
import pandas as pd

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

class Game(object):
	def __init__(self, home_team=None, away_team=None, league=None):
		self.home_team = home_team
		self.away_team = away_team
		self.league = league

		self.inning = 0
		self.top_half = True
		self.outs = 0

		self.first_base = None
		self.second_base = None
		self.third_base = None

		self.runs = 0
		self.game = None
		self.markov_game = None

		self.advanced_transition = False
		self.baserunning = False
		self.advanced_league = False
		self.stop = 0.9999
		self.max_runs = 21

		self.diagnostics = False
		self.single_probs = []
		self.double_probs = []
		self.triple_probs = []
		self.homerun_probs = []
		self.walk_probs = []
		self.out_probs = []

		self.collect_stats = False
		self.home_stats = {'singles':0,
						   'doubles':0,
						   'triples':0,
						   'homeruns':0,
						   'walks':0,
						   'hbps':0,
						   'errors':0,
						   'outs':0,
						   's31st':0,
						   'dh1st':0,
						   'sh2nd':0,
						   'productive_outs':0,
						   'double_plays':0,
						   'runs':0}
		self.away_stats = {'singles': 0,
						   'doubles': 0,
						   'triples': 0,
						   'homeruns': 0,
						   'walks': 0,
						   'hbps': 0,
						   'errors': 0,
						   'outs': 0,
						   's31st':0,
						   'dh1st':0,
						   'sh2nd':0,
						   'productive_outs':0,
						   'double_plays':0,
						   'runs':0}

		self.collect_player_stats = False
		self.batter_stats = pd.DataFrame(columns = PLAYER_COLUMN_NAMES)
		self.batter_stats = self.batter_stats.set_index('player_id')
		self.pitcher_stats = pd.DataFrame(columns=PLAYER_COLUMN_NAMES)
		self.pitcher_stats = self.pitcher_stats.set_index('player_id')
		

	def morey_z(self, p_b, p_p, p_l):
		return (((p_b - p_l)/np.sqrt(p_l*(1-p_l)) + (p_p - p_l)/np.sqrt(p_l*(1-p_l))) 
			/ np.sqrt(2) * np.sqrt(p_l*(1-p_l)) + p_l)

	def update_transition(self):
		# self.walk = 3.27 / 38.40
		# self.single = (8.65 - 1.76 - 0.16 - 1.39) / 38.40
		# self.double = 1.76 / 38.40
		# self.triple = 0.16 / 38.40
		# self.homerun = 1.39 / 38.40
		# self.out = 1 - (walk + single + double + triple + homerun)
		if self.advanced_transition and self.league is not None:

			if self.pitcher is None:
				self.pitcher = self.league.league_avg_pitcher

			if self.pitcher.pitcher_hand == 'R':
				batter_single = self.batter.as_batter.single_v_right
				batter_double = self.batter.as_batter.double_v_right
				batter_triple = self.batter.as_batter.triple_v_right
				batter_homerun = self.batter.as_batter.homerun_v_right
				batter_walk = self.batter.as_batter.walk_v_right
				self.productive_out = self.batter.as_batter.productive_out_v_right

			else:
				batter_single = self.batter.as_batter.single_v_left
				batter_double = self.batter.as_batter.double_v_left
				batter_triple = self.batter.as_batter.triple_v_left
				batter_homerun = self.batter.as_batter.homerun_v_left
				batter_walk = self.batter.as_batter.walk_v_left
				self.productive_out = self.batter.as_batter.productive_out_v_left

			if self.batter.batter_hand == 'R' or (
				self.batter.batter_hand == 'B' and self.pitcher.pitcher_hand == 'L'
			):
				pitcher_single = self.pitcher.as_pitcher.single_v_right
				pitcher_double = self.pitcher.as_pitcher.double_v_right
				pitcher_triple = self.pitcher.as_pitcher.triple_v_right
				pitcher_homerun = self.pitcher.as_pitcher.homerun_v_right
				pitcher_walk = self.pitcher.as_pitcher.walk_v_right
				pitcher_hbp = self.pitcher.as_pitcher.hbp_v_right
			else:
				pitcher_single = self.pitcher.as_pitcher.single_v_left
				pitcher_double = self.pitcher.as_pitcher.double_v_left
				pitcher_triple = self.pitcher.as_pitcher.triple_v_left
				pitcher_homerun = self.pitcher.as_pitcher.homerun_v_left
				pitcher_walk = self.pitcher.as_pitcher.walk_v_left
				pitcher_hbp = self.pitcher.as_pitcher.hbp_v_left

			if self.advanced_league:
				if self.pitcher.pitcher_hand == 'R':
					if self.batter.batter_hand == 'R':
						league_single = self.league.single_r_v_r
						league_double = self.league.double_r_v_r
						league_triple = self.league.triple_r_v_r
						league_homerun = self.league.homerun_r_v_r
						league_walk = self.league.walk_r_v_r
					else:
						league_single = self.league.single_r_v_l
						league_double = self.league.double_r_v_l
						league_triple = self.league.triple_r_v_l
						league_homerun = self.league.homerun_r_v_l
						league_walk = self.league.walk_r_v_l

				else:
					if self.batter.batter_hand == 'L':
						league_single = self.league.single_l_v_l
						league_double = self.league.double_l_v_l
						league_triple = self.league.triple_l_v_l
						league_homerun = self.league.homerun_l_v_l
						league_walk = self.league.walk_l_v_l
					else:
						league_single = self.league.single_l_v_r
						league_double = self.league.double_l_v_r
						league_triple = self.league.triple_l_v_r
						league_homerun = self.league.homerun_l_v_r
						league_walk = self.league.walk_l_v_r

			else:
				league_single = self.league.single
				league_double = self.league.double
				league_triple = self.league.triple
				league_homerun = self.league.homerun
				league_walk = self.league.walk

			self.single = max(1/1000, self.morey_z(batter_single, pitcher_single, league_single))
			self.double = max(1/1000, self.morey_z(batter_double, pitcher_double, league_double))
			self.triple = max(1/2000, self.morey_z(batter_triple, pitcher_triple, league_triple))
			self.homerun = max(1/2500, self.morey_z(batter_homerun, pitcher_homerun, league_homerun))
			self.walk = max(1 / 1000, self.morey_z(batter_walk, pitcher_walk, league_walk))
			self.hbp = pitcher_hbp
			self.error = self.league.error
			self.out = 1.0 - (self.walk + self.single + self.double + self.triple + self.homerun + self.hbp + self.error)

		else:
			self.walk = self.batter.walk
			self.single = self.batter.single
			self.double = self.batter.double
			self.triple = self.batter.triple
			self.homerun = self.batter.homerun
			self.out = 1.0 - (self.walk + self.single + self.double + self.triple + self.homerun)

		if self.diagnostics:
			self.single_probs.append(self.single)
			self.double_probs.append(self.double)
			self.triple_probs.append(self.triple)
			self.homerun_probs.append(self.homerun)
			self.walk_probs.append(self.walk)
			self.out_probs.append(self.out)

		# self.productive_out = self.batter.productive_out

	def sim_atbat(self, debug=False):
		if self.collect_player_stats:
			if not (self.batter_stats.index == self.batter.player_id).any():
				new_row = pd.Series([0]*(len(PLAYER_COLUMN_NAMES) - 1),
									index=self.batter_stats.columns,
									name=self.batter.player_id)
				self.batter_stats = self.batter_stats.append(new_row)
			if not (self.pitcher_stats.index == self.pitcher.player_id).any():
				new_row = pd.Series([0]*(len(PLAYER_COLUMN_NAMES) - 1),
									index=self.pitcher_stats.columns,
									name=self.pitcher.player_id)
				self.pitcher_stats = self.pitcher_stats.append(new_row)

		u = np.random.uniform()
		if u <= self.single:
			#Base hit
			if debug: print('single')

			if self.collect_stats:
				if self.top_half: self.away_stats['singles'] += 1
				else: self.home_stats['singles'] += 1
			if self.collect_player_stats:
				self.batter_stats.loc[self.batter.player_id, 'singles'] += 1
				self.pitcher_stats.loc[self.pitcher.player_id, 'singles'] += 1

			if self.third_base:
				self.runs += 1
				self.third_base = None
			if self.second_base:
				# if self.baserunning and np.random.uniform() <= self.second_base.as_batter.sh2nd:
				if self.baserunning and np.random.uniform() <= 2672/(2672 + 1740):
					# Using league average for single home from 2nd for now due to small samlpe size problems
					self.runs += 1

					if self.collect_stats:
						if self.top_half:
							self.away_stats['sh2nd'] += 1
						else:
							self.home_stats['sh2nd'] += 1
					if self.collect_player_stats:
						self.batter_stats.loc[self.batter.player_id, 'sh2nd'] += 1
						self.pitcher_stats.loc[self.pitcher.player_id, 'sh2nd'] += 1

				elif self.baserunning:
					self.third_base = self.second_base
				else:
					self.runs += 1
				self.second_base = None
			if self.first_base:
				if self.baserunning and np.random.uniform() <= self.first_base.as_batter.s31st and self.third_base is None:
					self.third_base = self.first_base

					if self.collect_stats:
						if self.top_half:
							self.away_stats['s31st'] += 1
						else:
							self.home_stats['s31st'] += 1
					if self.collect_player_stats:
						self.batter_stats.loc[self.batter.player_id, 's31st'] += 1
						self.pitcher_stats.loc[self.pitcher.player_id, 's31st'] += 1

				else:
					self.second_base = self.first_base
			self.first_base = self.batter
			return
		u -= self.single

		if u <= self.double:
			# Double
			if debug: print('double')

			if self.collect_stats:
				if self.top_half: self.away_stats['doubles'] += 1
				else: self.home_stats['doubles'] += 1
			if self.collect_player_stats:
				self.batter_stats.loc[self.batter.player_id, 'doubles'] += 1
				self.pitcher_stats.loc[self.pitcher.player_id, 'doubles'] += 1

			if self.third_base:
				self.runs += 1
			
			if self.second_base:
				self.runs += 1
			if self.first_base:
				if self.baserunning and np.random.uniform() <= self.first_base.as_batter.dh1st:
					self.runs += 1
					self.third_base = None

					if self.collect_stats:
						if self.top_half:
							self.away_stats['dh1st'] += 1
						else:
							self.home_stats['dh1st'] += 1
					if self.collect_player_stats:
						self.batter_stats.loc[self.batter.player_id, 'dh1st'] += 1
						self.pitcher_stats.loc[self.pitcher.player_id, 'dh1st'] += 1

				else:
					self.third_base = self.first_base
			self.first_base = None
			self.second_base = self.batter
			return
		u -= self.double

		if u <= self.triple:
			# Triple
			if debug: print('triple')

			if self.collect_stats:
				if self.top_half: self.away_stats['triples'] += 1
				else: self.home_stats['triples'] += 1
			if self.collect_player_stats:
				self.batter_stats.loc[self.batter.player_id, 'triples'] += 1
				self.pitcher_stats.loc[self.pitcher.player_id, 'triples'] += 1

			if self.third_base:
				self.runs += 1
			self.third_base = self.batter
			if self.second_base:
				self.runs += 1
			if self.first_base:
				self.runs += 1
			self.second_base = None
			self.first_base = None
			return
		u -= self.triple

		if u <= self.homerun:
			# Homerun
			if debug: print('homerun')

			if self.collect_stats:
				if self.top_half: self.away_stats['homeruns'] += 1
				else: self.home_stats['homeruns'] += 1
			if self.collect_player_stats:
				self.batter_stats.loc[self.batter.player_id, 'homeruns'] += 1
				self.pitcher_stats.loc[self.pitcher.player_id, 'homeruns'] += 1

			if self.third_base:
				self.runs += 1
			if self.second_base:
				self.runs += 1
			if self.first_base:
				self.runs += 1
			self.runs += 1
			self.third_base = None
			self.second_base = None
			self.first_base = None
			return
		u -= self.homerun

		if u <= self.walk:
			# Walk
			if debug: print('walk')

			if self.collect_stats:
				if self.top_half: self.away_stats['walks'] += 1
				else: self.home_stats['walks'] += 1
			if self.collect_player_stats:
				self.batter_stats.loc[self.batter.player_id, 'walks'] += 1
				self.pitcher_stats.loc[self.pitcher.player_id, 'walks'] += 1

			if self.first_base:
				if self.second_base:
					if self.third_base:
						self.runs += 1
					self.third_base = self.second_base
				self.second_base = self.first_base
			self.first_base = self.batter
			return
		u -= self.walk

		if u <= self.hbp:
			# Hit by pitch
			if debug: print('hbp')

			if self.collect_stats:
				if self.top_half: self.away_stats['hbps'] += 1
				else: self.home_stats['hbps'] += 1
			if self.collect_player_stats:
				self.batter_stats.loc[self.batter.player_id, 'hbps'] += 1
				self.pitcher_stats.loc[self.pitcher.player_id, 'hbps'] += 1

			if self.first_base:
				if self.second_base:
					if self.third_base:
						self.runs += 1
					self.third_base = self.second_base
				self.second_base = self.first_base
			self.first_base = self.batter
			return
		u -= self.hbp

		if u <= self.error:
			# 	Error on the play
			if self.collect_stats:
				if self.top_half: self.away_stats['errors'] += 1
				else: self.home_stats['errors'] += 1
			if self.collect_player_stats:
				self.batter_stats.loc[self.batter.player_id, 'errors'] += 1
				self.pitcher_stats.loc[self.pitcher.player_id, 'errors'] += 1

			if self.third_base:
				self.runs += 1
				self.third_base = None
			if self.second_base:
				self.third_base = self.second_base
				self.second_base = None
			if self.first_base:
				self.second_base = self.first_base
			self.first_base = self.batter
			return
		u -= self.error


		# Out
		if debug: print('Out')

		if self.collect_stats:
			if self.top_half:
				self.away_stats['outs'] += 1
			else:
				self.home_stats['outs'] += 1
		if self.collect_player_stats:
			self.batter_stats.loc[self.batter.player_id, 'outs'] += 1
			self.pitcher_stats.loc[self.pitcher.player_id, 'outs'] += 1

		self.outs += 1
		if self.baserunning and self.outs < 3:
			if self.first_base and np.random.uniform() <= 0.11:
				# double play
				self.first_base = None
				self.outs += 1

				if self.collect_stats:
					if self.top_half:
						self.away_stats['outs'] += 1
						self.away_stats['double_plays'] += 1
					else:
						self.home_stats['double_plays'] += 1
						self.home_stats['outs'] += 1
				if self.collect_player_stats:
					self.batter_stats.loc[self.batter.player_id, 'outs'] += 1
					self.batter_stats.loc[self.batter.player_id, 'double_plays'] += 1
					self.pitcher_stats.loc[self.pitcher.player_id, 'outs'] += 1
					self.pitcher_stats.loc[self.pitcher.player_id, 'double_plays'] += 1

			if self.outs < 3 and np.random.uniform() <= self.productive_out:
				if self.third_base:
					self.runs += 1
					self.third_base = None
				self.third_base = self.second_base
				self.second_base = self.first_base
				self.first_base = None

				if self.collect_stats:
					if self.top_half:
						self.away_stats['productive_outs'] += 1
					else:
						self.home_stats['productive_outs'] += 1
				if self.collect_player_stats:
					self.batter_stats.loc[self.batter.player_id, 'productive_outs'] += 1
					self.pitcher_stats.loc[self.pitcher.player_id, 'productive_outs'] += 1

	def sim_half_inning(self, initial_setup = False, debug=False):
		if not initial_setup:
			self.outs = 0
			self.runs = 0
			self.first_base = None
			self.second_base = None
			self.third_base = None


		while self.outs < 3:
			if self.top_half:
				self.pitcher = self.home_team.get_pitcher()
				self.batter = self.away_team.get_batter()
			else:
				self.pitcher = self.away_team.get_pitcher()
				self.batter = self.home_team.get_batter()

			self.update_transition()

			if debug:
				first_base = None if self.first_base is None else self.first_base.player_id
				second_base = None if self.second_base is None else self.second_base.player_id
				third_base = None if self.third_base is None else self.third_base.player_id
				print('Outs: ', self.outs, ' Runs: ', self.runs, ' AB: ', self.batter.player_id, ' 1B:', first_base, ' 2B: ', second_base, ' 3B: ', third_base)
			self.sim_atbat(debug = debug)


	def sim_game(self, reset=True, allow_extra_innings=False, debug=False):
		if reset:
			self.game = np.zeros((2,9))
			self.inning = 0
		while True:
			self.top_half = True
			self.sim_half_inning(debug=debug)
			self.game[0,self.inning] = self.runs

			self.top_half = False
			self.sim_half_inning(debug=debug)
			self.game[1,self.inning] = self.runs

			self.inning += 1
			if self.inning >= 9:
				if not allow_extra_innings or np.sum(self.game[0, :]) != np.sum(self.game[1, :]):
					# No extra innings allowed or the game is not tied after 9, so over
					break
				else:
					# Still tied and extras allowed, add another inning
					self.game = np.hstack((self.game, np.zeros((2,1))))
			self.away_stats['runs'] = np.sum(self.game[0, :])
			self.home_stats['runs'] = np.sum(self.game[1, :])

		return self.game.copy()

	def sim_scenario(self, debug=False):
		while self.inning < 9:
			while self.outs < 3:
				if self.top_half:
					self.pitcher = self.home_team.pitcher
					self.batter = self.away_team.get_batter()
				else:
					self.pitcher = self.away_team.pitcher
					self.batter = self.home_team.get_batter()

				self.update_transition()

				if debug:
					first_base = None if self.first_base is None else self.first_base.player_id
					second_base = None if self.second_base is None else self.second_base.player_id
					third_base = None if self.third_base is None else self.third_base.player_id
					print('Outs: ', self.outs, ' Runs: ', self.runs, ' AB: ', self.batter.player_id, ' 1B:', first_base, ' 2B: ', second_base, ' 3B: ', third_base)
		
				self.sim_atbat(debug = debug)

			self.game[int(not self.top_half), self.inning] = self.runs
			# Reset to next half inning
			self.runs = 0
			self.first_base = None
			self.second_base = None
			self.third_base = None
			self.outs = 0

			self.top_half = not self.top_half
			self.inning += int(self.top_half)

		return self.game

	def set_scenario(self, game, runs, first_base, second_base, third_base, outs, top_half, inning, away_index, home_index):
		self.game = game

		self.runs = runs
		self.first_base = first_base
		self.second_base = second_base
		self.third_base = third_base
		self.outs = outs

		self.top_half = top_half
		self.inning = inning

		self.home_team.index = home_index
		self.away_team.index = away_index

	def update_markov_transition(self):
		self.update_transition()
		walk = self.walk
		single = self.single
		double = self.double
		triple = self.triple
		homerun = self.homerun
		out = self.out


		P = np.zeros((25,25))
		A = np.array([[homerun, single+walk, double, triple, 0, 0, 0, 0],
					  [homerun, 0, 0, triple, single+walk, 0, double, 0],
					  [homerun, single, double, triple, walk, 0, 0, 0],
					  [homerun, single, double, triple, 0, walk, 0, 0],
					  [homerun, 0, 0, triple, single, 0, double, walk],
					  [homerun, 0, 0, triple, single, 0, double, walk],
					  [homerun, single, double, triple, 0, 0, 0, walk],
					  [homerun, 0, 0, triple, single, 0, double, walk]])

		A0 = np.array([[0, single+walk, double, triple, 0, 0, 0, 0],
					  [0, 0, 0, 0, single+walk, 0, double, 0],
					  [0, 0, 0, 0, walk, 0, 0, 0],
					  [0, 0, 0, 0, 0, walk, 0, 0],
					  [0, 0, 0, 0, 0, 0, 0, walk],
					  [0, 0, 0, 0, 0, 0, 0, walk],
					  [0, 0, 0, 0, 0, 0, 0, walk],
					  [0, 0, 0, 0, 0, 0, 0, 0]])

		A1 = np.array([[homerun, 0, 0, 0, 0, 0, 0, 0],
					  [0, 0, 0, triple, 0, 0, 0, 0],
					  [0, single, double, triple, 0, 0, 0, 0],
					  [0, single, double, triple, 0, 0, 0, 0],
					  [0, 0, 0, 0, single, 0, double, 0],
					  [0, 0, 0, 0, single, 0, double, 0],
					  [0, 0, 0, 0, 0, 0, 0, 0],
					  [0, 0, 0, 0, 0, 0, 0, walk]])

		A2 = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
					  [homerun, 0, 0, 0, 0, 0, 0, 0],
					  [homerun, 0, 0, 0, 0, 0, 0, 0],
					  [homerun, 0, 0, 0, 0, 0, 0, 0],
					  [0, 0, 0, triple, 0, 0, 0, 0],
					  [0, 0, 0, triple, 0, 0, 0, 0],
					  [0, single, double, triple, 0, 0, 0, 0],
					  [0, 0, 0, 0, single, 0, double, 0]])

		A3 = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
					  [0, 0, 0, 0, 0, 0, 0, 0],
					  [0, 0, 0, 0, 0, 0, 0, 0],
					  [0, 0, 0, 0, 0, 0, 0, 0],
					  [homerun, 0, 0, 0, 0, 0, 0, 0],
					  [homerun, 0, 0, 0, 0, 0, 0, 0],
					  [homerun, 0, 0, 0, 0, 0, 0, 0],
					  [0, 0, 0, triple, 0, 0, 0, 0]])

		A4 = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
					  [0, 0, 0, 0, 0, 0, 0, 0],
					  [0, 0, 0, 0, 0, 0, 0, 0],
					  [0, 0, 0, 0, 0, 0, 0, 0],
					  [0, 0, 0, 0, 0, 0, 0, 0],
					  [0, 0, 0, 0, 0, 0, 0, 0],
					  [0, 0, 0, 0, 0, 0, 0, 0],
					  [homerun, 0, 0, 0, 0, 0, 0, 0]])
		B = np.identity(8) * out
		F = np.ones((8)) * out

		P[0:8,0:8] = np.copy(A)
		P[8:16, 8:16] = np.copy(A)
		P[16:24, 16:24] = np.copy(A)
		P[0:8, 8:16] = np.copy(B)
		P[8:16, 16:24] = np.copy(B)
		P[16:24, 24] = np.copy(F)
		P[24, 24] = 1

		P0 = np.copy(P)
		P0[0:8,0:8] = A0
		P0[8:16, 8:16] = A0
		P0[16:24, 16:24] = A0

		P1 = np.zeros((25,25))
		P1[0:8,0:8] = A1
		P1[8:16, 8:16] = A1
		P1[16:24, 16:24] = A1

		P2 = np.zeros((25,25))
		P2[0:8,0:8] = A2
		P2[8:16, 8:16] = A2
		P2[16:24, 16:24] = A2

		P3 = np.zeros((25,25))
		P3[0:8,0:8] = A3
		P3[8:16, 8:16] = A3
		P3[16:24, 16:24] = A3

		P4 = np.zeros((25,25))
		P4[0:8,0:8] = A4
		P4[8:16, 8:16] = A4
		P4[16:24, 16:24] = A4

		self.markov_transition = [P0, P1, P2, P3, P4]

		# return P, [P0, P1, P2, P3, P4]
	

	def sim_half_game_markov(self, offense_team, defense_team):
		offense_team.index = 0
		innings = []
		u = np.zeros((self.max_runs*9,25))
		run_expectancy = np.zeros((self.max_runs*9))
		u[0, 0] = 1
		atbat = 0

		u1_mask = np.ones((self.max_runs*9,25))
		u1_mask[::self.max_runs, :] = 0

		u2_mask = np.ones((self.max_runs*9,25))
		u2_mask[::self.max_runs, :] = 0
		u2_mask[1::self.max_runs, :] = 0

		u3_mask = np.ones((self.max_runs*9,25))
		u3_mask[::self.max_runs, :] = 0
		u3_mask[1::self.max_runs, :] = 0
		u3_mask[2::self.max_runs, :] = 0

		u4_mask = np.ones((self.max_runs*9,25))
		u4_mask[::self.max_runs, :] = 0
		u4_mask[1::self.max_runs, :] = 0
		u4_mask[2::self.max_runs, :] = 0
		u4_mask[3::self.max_runs, :] = 0

		
		self.pitcher = defense_team.pitcher
		while (np.sum(u[self.max_runs*8:,-1]) < self.stop and np.sum(u) > self.stop):

			# Create 4 shifted copies for eqn (2) from Bukiet, Harold, and Palacios (97)
			u1 = np.roll(u, 1, axis=0) * u1_mask
			u2 = np.roll(u, 2, axis=0) * u2_mask
			u3 = np.roll(u, 3, axis=0) * u3_mask
			u4 = np.roll(u, 4, axis=0) * u4_mask

			# Move to next batter
			self.batter = offense_team.get_batter()

			self.update_markov_transition()

			# eqn (2) from Bukiet, Harold, and Palacios (97)
			u = np.dot(u, self.markov_transition[0]) + np.dot(u1, self.markov_transition[1]) + np.dot(u2, self.markov_transition[2]) + np.dot(u3, self.markov_transition[3]) + np.dot(u4, self.markov_transition[4])

			# Move 3-out probabilitie to next inning
			run_expectancy[:8*self.max_runs] += u[:8*self.max_runs,-1]
			u[self.max_runs:,0] += u[:8*self.max_runs,-1]
		
			# For per-inning run expectancy, need to save the following results:
			u[:8*self.max_runs,-1] = 0

		run_expectancy += u[:,-1]
		return run_expectancy

	def sim_inning_markov(self):

		if self.top_half:
			offense_team = self.away_team
			defense_team=self.home_team
		else:
			offense_team = self.home_team
			defense_team=self.away_team
		offense_team.index = 0
		u = np.zeros((self.max_runs,25))
		u[0, 0] = 1
		while (np.sum(u[:,-1]) < self.stop and np.sum(u) > self.stop):
			zero_vector = np.zeros((1,25))

			u1 = np.concatenate((zero_vector, np.copy(u[:self.max_runs-1, :])))
			u2 = np.concatenate((zero_vector, zero_vector, np.copy(u[:self.max_runs-2, :])))
			u3 = np.concatenate((zero_vector, zero_vector, zero_vector, np.copy(u[:self.max_runs-3, :])))
			u4 = np.concatenate((zero_vector, zero_vector, zero_vector, zero_vector, np.copy(u[:self.max_runs-4, :])))

			# Move to next batter
			self.batter = offense_team.get_batter()

			self.update_markov_transition()
			
			u = np.dot(u, self.markov_transition[0]) + np.dot(u1, self.markov_transition[1]) + np.dot(u2, self.markov_transition[2]) + np.dot(u3, self.markov_transition[3]) + np.dot(u4, self.markov_transition[4])			# print(np.sum(u))



		return u

	def sim_game_markov(self):
		self.markov_game = np.zeros((2,self.max_runs*9))
		self.markov_game[0, :] = self.sim_half_game_markov(offense_team=self.away_team, defense_team=self.home_team)
		self.markov_game[1, :] = self.sim_half_game_markov(offense_team=self.home_team, defense_team=self.away_team)

		return self.markov_game

		