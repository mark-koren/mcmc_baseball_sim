import numpy as np
import pdb
from pprint import pprint

class Team(object):
	def __init__(self, name='Team'):
		self.name = name
		self.players = {}
		self.bullpen = {}
		self.order = []
		self.index = 0
		self.pitcher = None

		# Fielding stats
		self.productive_out = 0
		self.s31st = 0
		self.dh1st = 0
		self.sh2nd = 0

		self.batters_faced = 0
		self.starting_pitcher = True

	def get_batter(self):
		# pdb.set_trace()
		batter = self.players[self.order[self.index]]
		self.index = (self.index + 1) % len(self.order)
		# print(batter.name)
		return batter

	def get_pitcher(self):
		# pdb.set_trace()
		if (np.random.uniform() < (
				self.pitcher.chance_of_substitution_as_sp[self.batters_faced]
				if self.starting_pitcher
				else self.pitcher.chance_of_substitution_as_rp[self.batters_faced])
		):
			# replace pitcher

			self.starting_pitcher = False
			self.batters_faced = 0
			if bool(self.bullpen):
				new_pitcher_id = np.random.choice(list(self.bullpen.keys()), 1, p=list(self.bullpen.values()))[0]
				# Remove used pitcher from BP and re-balance probability
				removed_probability = self.bullpen.pop(new_pitcher_id)
				for player_id in self.bullpen.keys():
					self.bullpen[player_id] = self.bullpen[player_id] / (1 - removed_probability)
				# print('Replacing ', self.pitcher.player_id, ' with ', new_pitcher_id)
				self.pitcher = self.players[new_pitcher_id]

		return self.pitcher

	def __str__(self):
		return self.name