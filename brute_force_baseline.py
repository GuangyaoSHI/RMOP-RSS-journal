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
import matplotlib.pyplot as plt

# change the game turn tomorrow and retest
#starts = {0: [(0, 1), 0], 1: [(0, 1), 0], 2: [(0, 0), 0], 3: [(0, 0), 0]}
starts = {0: [(0, 0), 0], 1: [(0, 0), 0], 2: [(0, 0), 0], 3: [(0, 0), 0]}

# start a game
board = setup_game()
# who take the first step
turn = 'attacker'
horizon = 4
alpha = 2
game = GameState(board, starts, turn, horizon, alpha)
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
print('one choice time spent is {}'.format(end-start))

print('worst-case reward is {}'.format(reward_max))
path_attack[0]
# 84
# np.array([94,88,86,88,88])
print('robots paths')
print(path_attack[0])
print('attacker choices')
print(path_attack[1])

fig, axs = plt.subplots(2, 2)
style = {0: 'ro-', 1: 'y*-', 2: 'm^-', 3: 'ko-'}

for robot in range(4):
    traj = path_attack[0][robot]
    print('robot {} trajectory:'.format(robot))
    print(traj)
    if robot < 2:
        plot_reward_map(game, axs[0, robot])
        plot_path(traj, axs[0, robot], style[robot])
    else:
        plot_reward_map(game, axs[1, robot - 2])
        plot_path(traj, axs[1, robot - 2], style[robot])
plt.show()