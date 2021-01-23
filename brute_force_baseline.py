# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 11:26:43 2021

@author: sgyhi
"""

import networkx as nx
from gamestate import *
from utilities import *
import copy
import sys
import time

# change the game turn tomorrow and retest
starts = {0: [(0, 1), 0], 1: [(0, 1), 0], 2: [(0, 0), 0], 3: [(0, 0), 0]}

# start a game
board = setup_game()
game = GameState(board, starts)
# return all feasible paths
paths = all_paths(starts, game)
attacks = all_attacks(list(starts.keys()), game)

reward_max = 0
path_attack = ()

for choice in product(*list(paths.values())):
    # print('choice is {}'.format(choice))
    start = time.time()
    reward_min = sys.maxsize
    path_attack_min = ()
    for attack in attacks:
        # print('attack is {}'.format(attack))
        reward = compute_reward(game, choice, attack)
        # print('reward is {}'.format(reward))
        if reward < reward_min:
            reward_min = reward
            path_attack_min = (choice, attack)
    if reward_min > reward_max:
        reward_max = reward_min
        path_attack = path_attack_min
    end = time.time()
# print('one choice time spent is {}'.format(end-start))

print('worst-case reward is {}'.format(reward_max))
path_attack[0]
# 84
# np.array([94,88,86,88,88])

print('test github')
