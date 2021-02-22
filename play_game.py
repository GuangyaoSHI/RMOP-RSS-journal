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
import pickle

def generate_grid_map(grid_len, grid_height, parameters):
    # generate a grid graph with size=(grid_len, grid_height)
    # parameters are for probability distribution. Here we use exponential distribution
    graph = nx.grid_2d_graph(grid_len, grid_height)
    values = np.random.exponential(scale=parameters, size=(grid_len * grid_height,))
    values = np.around(values * 20)
    values = values.astype(int)
    reward = dict(zip(list(graph.nodes), values))
    nx.set_node_attributes(graph, reward, 'reward')
    return graph

def mcts_process(game, budget=400):
    '''
    game is gameState object
    budget is computational budget for Monte Carlo Tree Search
    '''
    MCTS = MCTSPolicy(game)
    for i in range(budget):
        # select the node to expand in search tree
        node_exp = MCTS.selection(0)
        # expand the node and return the frontier node
        node_fron = MCTS.expansion(node_exp)
        # rollout from frontier node
        reward = MCTS.simulation(node_fron)
        # backpropagation
        MCTS.backpropagation(node_fron, reward)
        # make a copy of the current tree
    # s = visualize_MCTS(MCTS)
    # s.view()
    nextNode = action_selection(MCTS)
    return (nextNode, MCTS)

def play_game(budget, start, board, horizon, alpha, robot_policy, attacker_policy):
    # starts = {0: [(0, 0), 0], 1: [(0, 0), 0], 2: [(0, 0), 0], 3: [(0, 0), 0]}
    # starts = {0: [(0, 1), 0], 1: [(0, 1), 0], 2: [(0, 0), 0], 3: [(0, 0), 0]}
    # start a game
    # board = setup_game()
    # who take the first step
    turn = 'attacker'
    # horizon = 4
    # alpha = 2
    game = GameState(board, start, turn, horizon, alpha)

    # computational budget
    # budget = 500

    # game_traj.add_node(starts, attri_dict={'state':game})
    # last_node = starts
    path = [start]

    # keep track of all trees
    # trees = {'attacker': [], 'robot': []}
    while not game.is_terminal():
        # check this is the right turn
        assert game.firstTurn == turn, 'it should be ' + turn + ' turn'
        if attacker_policy == 'mcts':
            next_node, mcts = mcts_process(game, budget)
            # print('current game state {}'.format(game.currNode))
            # print('attacker next move {}'.format(next_node))
            num_att = 0
            for robot in next_node:
                num_att += next_node[robot][1]
            assert num_att <= game.ALPHA, 'more than ALPHA robots are attacked'
        else:
            random_policy = RandomPolicy()
            next_node = random_policy.move(game)
            # print('current game state {}'.format(game.currNode))
            # print('attacker next move {}'.format(next_node))
            num_att = 0
            for robot in next_node:
                num_att += next_node[robot][1]
            assert num_att <= game.ALPHA, 'more than ALPHA robots are attacked'
        # trees[game.turn].append(mcts)
        game.move(next_node)
        # path.append(next_node)
        # check that it's another player's turn
        assert game.turn != turn, 'it should not be ' + turn + ' turn'
        # initialize a mcts object for attackers
        if robot_policy == 'mcts':
            next_node, mcts = mcts_process(game, budget)
            # trees[game.turn].append(mcts)
        else:
            random_policy = RandomPolicy()
            next_node = random_policy.move(game)
        game.move(next_node)
        path.append(next_node)
    # with open("trees"+str(game_round)+".txt", "wb") as fp:  # Pickle
    #     pickle.dump(trees, fp)
    # fig, axs = plt.subplots(2, 2)
    # # path = [(0,0),(0,1),(1,1),(1,2),(2,2),(2,3)]
    # style = {0: 'ro-', 1: 'y*-', 2: 'm^-', 3: 'ko-'}
    # trajs = {}
    # for robot in path[0]:
    #     traj = [node[robot][0] for node in path]
    #     print('robot {} trajectory:'.format(robot))
    #     print(traj)
    #     trajs[robot] = traj
    #     if robot < 2:
    #         plot_reward_map(game, axs[0, robot])
    #         plot_path(traj, axs[0, robot], style[robot])
    #     else:
    #         plot_reward_map(game, axs[1, robot - 2])
    #         plot_path(traj, axs[1, robot - 2], style[robot])
    # print('reward is {}'.format(game.collected_reward()))
    # with open("trajectories.txt", "wb") as fp:  # Pickle
    #     pickle.dump(trajs, fp)
    # # with open("rewards.txt", "rb") as fp:  # Unpickling
    # #     data = pickle.load(fp)
    # #     data.append(game.collected_reward())
    # # with open("rewards.txt", "wb") as fp:  # Pickle
    # #     pickle.dump(data, fp)
    # # plt.show()
    return game


if __name__ == "__main__":
    # budgets = [100, 400, 800, 1600]
    # rewards ={}
    # rounds = 100
    # for budget in budgets:
    #     rewards[budget] = []
    #     for game_round in range(rounds):
    #         rewards[budget].append(play_game(budget, game_round))
    # with open("rewards"+".txt", "wb") as fp:  # Pickle
    #     pickle.dump(rewards, fp)
    budget = 200
    start = {0: [(0, 1), 0], 1: [(5, 1), 0], 2: [(6, 6), 0], 3: [(10, 10), 0]}
    graph = generate_grid_map(15, 15, 1)
    horizon = 4
    alpha = 2
    robot_policy = 'random'
    attacker_policy = 'mcts'
    game = play_game(budget, start, graph, horizon, alpha, robot_policy, attacker_policy)
    print('reward is {}'.format(game.collected_reward()))




