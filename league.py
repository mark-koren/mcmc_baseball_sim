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
		self.out = 1 - (self.single + self.double + self.triple + self.homerun + self.walk)

		self.league_avg_pitcher = Player(player_id=0, name='LeagueAVGPitcher', walk = self.walk, single=self.single,
				  double=self.double, triple=self.triple, homerun=self.homerun)