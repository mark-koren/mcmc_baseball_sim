import numpy as np
import pdb
from pprint import pprint

class Player(object):
	def __init__(self, player_id, single, double, triple, homerun, walk, productive_out=0, s31st=0, dh1st=0, sh2nd=0, name='Player'):
		self.player_id = player_id
		self.name = name
		self.single = max(1/1000, single)
		self.double = max(1/1000, double)
		self.triple = max(1/2000, triple)
		self.homerun = max(1/2500, homerun)
		self.walk = max(1/1000, walk)
		self.out = 1 - (self.single + self.double + self.triple + self.homerun + self.walk)
		self.productive_out = productive_out

		# self.xbt = xbt
		self.s31st = s31st
		self.dh1st = dh1st
		self.sh2nd = sh2nd