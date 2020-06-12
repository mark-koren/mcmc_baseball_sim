import numpy as np
import pdb
from pprint import pprint


class PlayerStats(object):
    def __init__(self, player_id=None
                 # , single=0, double=0, triple=0, homerun=0, walk=0, productive_out=0, s31st=0, dh1st=0, sh2nd=0, name='Player'):
                 ):
        self._single_v_left = 0
        self._double_v_left = 0
        self._triple_v_left = 0
        self._homerun_v_left = 0
        self._walk_v_left = 0
        self._hbp_v_left = 0
        self._out_v_left = 0
        self._productive_out_v_left = 0

        self._single_v_right = 0
        self._double_v_right = 0
        self._triple_v_right = 0
        self._homerun_v_right = 0
        self._walk_v_right = 0
        self._hbp_v_right = 0
        self._out_v_right = 0
        self._productive_out_v_right = 0

        # self.xbt = xbt
        self._s31st = 0
        self._dh1st = 0
        self._sh2nd = 0

        # self._min_single_v_left = 1/1000
        # self._min_double_v_left = 1/1000
        # self._min_triple_v_left = 1/2000
        # self._min_homerun_v_left = 1/2500
        # self._min_walk_v_left = 1/1000
        # self._min_out_v_left = 1/1000
        # self._min_productive_out_v_left = 1/1000
        #
        # self._min_single_v_right = 1/1000
        # self._min_double_v_right = 1/1000
        # self._min_triple_v_right = 1/2000
        # self._min_homerun_v_right = 1/2500
        # self._min_walk_v_right = 1/1000
        # self._min_out_v_right = 1/1000
        # self._min_productive_out_v_right = 1/1000

    @property
    def single_v_left(self):
        return self._single_v_left

    @single_v_left.setter
    def single_v_left(self, single_v_left):
        self._single_v_left = min(1, max(1 / 1000, single_v_left))

    @property
    def double_v_left(self):
        return self._double_v_left

    @double_v_left.setter
    def double_v_left(self, double_v_left):
        self._double_v_left = min(1, max(1 / 1000, double_v_left))

    @property
    def triple_v_left(self):
        return self._triple_v_left

    @triple_v_left.setter
    def triple_v_left(self, triple_v_left):
        self._triple_v_left = min(1, max(1 / 5000, triple_v_left))

    @property
    def homerun_v_left(self):
        return self._homerun_v_left

    @homerun_v_left.setter
    def homerun_v_left(self, homerun_v_left):
        self._homerun_v_left = min(1, max(1 / 2500, homerun_v_left))

    @property
    def walk_v_left(self):
        return self._walk_v_left

    @walk_v_left.setter
    def walk_v_left(self, walk_v_left):
        self._walk_v_left = min(1, max(1 / 1000, walk_v_left))

    @property
    def out_v_left(self):
        return self._out_v_left

    @out_v_left.setter
    def out_v_left(self, out_v_left):
        self._out_v_left = min(1, max(1 / 1000, out_v_left))

    @property
    def productive_out_v_left(self):
        return self._productive_out_v_left

    @productive_out_v_left.setter
    def productive_out_v_left(self, productive_out_v_left):
        self._productive_out_v_left = min(1, max(1 / 1000, productive_out_v_left))

    @property
    def single_v_right(self):
        return self._single_v_right

    @single_v_right.setter
    def single_v_right(self, single_v_right):
        self._single_v_right = min(1, max(1 / 1000, single_v_right))

    @property
    def double_v_right(self):
        return self._double_v_right

    @double_v_right.setter
    def double_v_right(self, double_v_right):
        self._double_v_right = min(1, max(1 / 1000, double_v_right))

    @property
    def triple_v_right(self):
        return self._triple_v_right

    @triple_v_right.setter
    def triple_v_right(self, triple_v_right):
        self._triple_v_right = min(1, max(1 / 5000, triple_v_right))

    @property
    def homerun_v_right(self):
        return self._homerun_v_right

    @homerun_v_right.setter
    def homerun_v_right(self, homerun_v_right):
        self._homerun_v_right = min(1, max(1 / 2500, homerun_v_right))

    @property
    def walk_v_right(self):
        return self._walk_v_right

    @walk_v_right.setter
    def walk_v_right(self, walk_v_right):
        self._walk_v_right = min(1, max(1 / 1000, walk_v_right))

    @property
    def hbp_v_left(self):
        return self._hbp_v_left

    @hbp_v_left.setter
    def hbp_v_left(self, hbp_v_left):
        self._hbp_v_left = min(1, max(1 / 1000, hbp_v_left))

    @property
    def hbp_v_right(self):
        return self._hbp_v_right

    @hbp_v_right.setter
    def hbp_v_right(self, hbp_v_right):
        self._hbp_v_right = min(1, max(1 / 1000, hbp_v_right))

    @property
    def out_v_right(self):
        return self._out_v_right

    @out_v_right.setter
    def out_v_right(self, out_v_right):
        self._out_v_right = min(1, max(1 / 1000, out_v_right))

    @property
    def productive_out_v_right(self):
        return self._productive_out_v_right

    @productive_out_v_right.setter
    def productive_out_v_right(self, productive_out_v_right):
        self._productive_out_v_right = min(1, max(1 / 1000, productive_out_v_right))

    @property
    def s31st(self):
        return self._s31st

    @s31st.setter
    def s31st(self, s31st):
        self._s31st = s31st

    @property
    def dh1st(self):
        return self._dh1st

    @dh1st.setter
    def dh1st(self, dh1st):
        self._dh1st = dh1st

    @property
    def sh2nd(self):
        return self._sh2nd

    @sh2nd.setter
    def sh2nd(self, sh2nd):
        self._sh2nd = sh2nd


class Player(object):
    def __init__(self, player_id=None
                 # , single=0, double=0, triple=0, homerun=0, walk=0, productive_out=0, s31st=0, dh1st=0, sh2nd=0, name='Player'):
                 ):
        self.player_id = player_id
        self.name = ''
        self.batter_hand = 'R'
        self.pitcher_hand = 'R'

        self._as_batter = PlayerStats()
        self._as_pitcher = PlayerStats()

        self.chance_of_substitution_as_rp = []
        self.chance_of_substitution_as_sp = []

    @property
    def as_batter(self):
        return self._as_batter

    @as_batter.setter
    def as_batter(self, batter):
        self._as_batter = batter

    @property
    def as_pitcher(self):
        return self._as_pitcher

    @as_pitcher.setter
    def as_pitcher(self, pitcher):
        self._as_pitcher = pitcher

    def __str__(self):
        return self.name + ' (' + self.player_id + ')'

    def __key(self):
        return (self.player_id)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Player):
            return self.__key() == other.__key()
        return NotImplemented
