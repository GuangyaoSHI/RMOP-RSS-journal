# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 10:36:52 2020

@author: sgyhit
"""

from gamestate import *
from policies import *
import networkx as nx
import sys
import copy
from utilities import *
import matplotlib.pyplot as plt
import random

# starts = {0:[(0,0), 0], 1:[(0,0),0], 2:[(0,0), 0],3:[(0,0),0]}

starts = {0: [(0, 1), 0], 1: [(0, 1), 0], 2: [(0, 0), 0], 3: [(0, 0), 0]}

# start a game
board = setup_game()
game = GameState(board, starts)

# keep track of paths
# it will be a directed line, a special tree
game_traj = nx.DiGraph()

# computational budget
budget = 1000

# game_traj.add_node(starts, attri_dict={'state':game})
# last_node = starts 
path = [starts]

while not game.is_terminal():
    # initialize a MCTS obje ct
    MCTS = MCTSPolicy(game)
    assert game.turn == 'robot', 'it should be robots turn'
    for i in range(budget):
        # select the node to expand in search tree
        node_exp = MCTS.selection(0)
        # expand the node and return the frontier node
        node_fron = MCTS.expansion(node_exp)
        # rollout from frontier node
        reward = MCTS.simulation(node_fron)
        # backpropgration
        MCTS.backpropagation(node_fron, reward)
    # MCTS.digraph.nodes[node_exp]['state'].turn
    # nx.draw(MCTS.digraph, with_labels = True)
    # select one action based on Monte Carlo Tree
    # based on UTC
    # Todo: other criterion
    # {UTC:action}
    UCT_A = {}
    for node in MCTS.digraph.successors(0):
        reward = MCTS.digraph.nodes[node]['reward'] / MCTS.digraph.nodes[node]['n']
        UCT_A[reward] = \
            MCTS.digraph.edges[0, node]['action']
    next_node = UCT_A[max(UCT_A)]
    game.move(next_node)
    path.append(next_node)
    # game_traj.add_node(action, state=copy.deepcopy(game))
    # game_traj.add_edge(last_node, action)
    # last_node = action
    assert game.turn == 'attacker', 'it should be attackers turn'
    # legal_moves = [{robot:indicator}]
    # legal_moves = game.legal_moves(game.currNode)
    # move = random.sample(legal_moves,1)[0]
    # next_node_att = copy.deepcopy(game.currNode)
    # for robot in game.currNode:
    #     next_node_att[robot][1] = move[robot] 
    # game.move(next_node_att)
    # path.append(next_node_att)

    # initialize a MCTS object for attackers
    MCTS = MCTSPolicy(game)
    B_adverial = 1000
    for i in range(B_adverial):
        # select the node to expand in search tree
        node_exp = MCTS.selection(0)
        # expand the node and return the frontier node
        node_fron = MCTS.expansion(node_exp)
        # rollout from frontier node
        reward = MCTS.simulation(node_fron)
        # backpropgration
        # reward will be negative
        MCTS.backpropagation(node_fron, -reward)
    # MCTS.digraph.nodes[node_exp]['state'].turn
    # nx.draw(MCTS.digraph, with_labels = True)
    # select one action based on Monte Carlo Tree
    # based on UTC
    # Todo: other criterion
    # {UCT:action}
    UCT_A = {}
    for node in MCTS.digraph.successors(0):
        assert MCTS.digraph.nodes[node]['reward'] <= 0, 'attacker reward is positive'
        reward = MCTS.digraph.nodes[node]['reward'] / MCTS.digraph.nodes[node]['n']
        UCT_A[reward] = \
            MCTS.digraph.edges[0, node]['action']
    next_node = UCT_A[max(UCT_A)]
    game.move(next_node)
    path.append(next_node)

fig, axs = plt.subplots(2, 2)

# test
# path = [(0,0),(0,1),(1,1),(1,2),(2,2),(2,3)]
style = {0: 'ro-', 1: 'y*-', 2: 'm^-', 3: 'ko-'}
trajs = {}
for robot in path[0]:
    traj = [node[robot][0] for node in path]
    print('robot {} trajectory:'.format(robot))
    print(traj)
    trajs[robot] = traj
    if robot < 2:
        plot_reward_map(game, axs[0, robot])
        plot_path(traj, axs[0, robot], style[robot])
    else:
        plot_reward_map(game, axs[1, robot - 2])
        plot_path(traj, axs[1, robot - 2], style[robot])
print('reward is {}'.format(game.collected_reward()))
