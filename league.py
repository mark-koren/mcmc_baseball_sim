import numpy as np
import pdb
from pprint import pprint

from player import Player

class League(object):
	def __init__(self, single, double, triple, homerun, walk, name='League'):
		self.name = name
		self.single = single
		self.double = double
		self.triple = triple
		self.homerun = homerun
		self.walk = walk
		self.error = 0
		self.out = 1 - (self.single + self.double + self.triple + self.homerun + self.walk)
		# TODO: Recreate league-average pitcher using new player design
		# self.league_avg_pitcher = Player(player_id=0, name='LeagueAVGPitcher', walk = self.walk, single=self.single,
		# 		  double=self.double, triple=self.triple, homerun=self.homerun)

		self.single_l_v_l = 0
		self.double_l_v_l = 0
		self.triple_l_v_l = 0
		self.homerun_l_v_l = 0
		self.walk_l_v_l = 0
		self.out_l_v_l = 1 - (self.single_l_v_l + self.double_l_v_l + self.triple_l_v_l + self.homerun_l_v_l + self.walk_l_v_l)

		self.single_l_v_r = 0
		self.double_l_v_r = 0
		self.triple_l_v_r = 0
		self.homerun_l_v_r = 0
		self.walk_l_v_r = 0
		self.out_l_v_r = 1 - (
					self.single_l_v_r + self.double_l_v_r + self.triple_l_v_r + self.homerun_l_v_r + self.walk_l_v_r)

		self.single_r_v_l = 0
		self.double_r_v_l = 0
		self.triple_r_v_l = 0
		self.homerun_r_v_l = 0
		self.walk_r_v_l = 0
		self.out_r_v_l = 1 - (
					self.single_r_v_l + self.double_r_v_l + self.triple_r_v_l + self.homerun_r_v_l + self.walk_r_v_l)

		self.single_r_v_r = 0
		self.double_r_v_r = 0
		self.triple_r_v_r = 0
		self.homerun_r_v_r = 0
		self.walk_r_v_r = 0
		self.out_r_v_r = 1 - (
					self.single_r_v_r + self.double_r_v_r + self.triple_r_v_r + self.homerun_r_v_r + self.walk_r_v_r)