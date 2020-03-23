import numpy as np
import pdb
from pprint import pprint

class Team(object):
	def __init__(self, name='Team'):
		self.name = name
		self.players = []
		self.order = []
		self.index = 0
		self.pitcher = None

		# Fielding stats
		self.productive_out = 0
		self.s31st = 0
		self.dh1st = 0
		self.sh2nd = 0

	def get_batter(self):
		# pdb.set_trace()
		batter = self.players[self.order[self.index]]
		self.index = (self.index + 1) % len(self.order)
		# print(batter.name)
		return batter