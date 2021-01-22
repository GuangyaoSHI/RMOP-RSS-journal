# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 19:42:15 2021

@author: sgyhi
"""
import networkx as nx
import matplotlib.pyplot as plt
from gamestate_no_attack import *
from policies_no_attack import *
import random
import copy
from itertools import combinations
from itertools import product 


 
def setup_game():
    #define a blank board
    #nx.draw(G, with_labels=True)
    grid_len = 5
    grid_height = 5
    G = nx.grid_2d_graph(grid_len, grid_height)
    values = [1,2,23,4,5,\
                  2,3,4,2,7,\
                  3,6,27,8,1,\
                  5,6,27,2,9,\
                  12,1,23,4,9]
    reward = dict(zip(list(G.nodes), values))
    nx.set_node_attributes(G, reward, 'reward')  
    
    return G 

# def setup_game():
#     #define a blank board
#     G = nx.Graph()
#     #{node:reward}
#     nodes = {(-4,0):0, (-3,0):0, (-2,0):0, (-2,1):0,\
#               (-2,2):0,(-1,0):0,(0,0):0,\
#               (1,0):1,(2,0):1,(2,1):2,(2,2):20,(3,0):2,(4,0):10}
#     for node in nodes:
#         G.add_node(node,reward=nodes[node], position=node)
#     edges = [((-4,0),(-3,0)),((-3,0),(-2,0)),((-2,0),(-2,1)),\
#               ((-2,1),(-2,2)),((-2,0),(-1,0)),\
#                   #((-1,0),(0,0)),\
#                   ((1,0),(2,0)),((2,0),(2,1)),((2,1),(2,2)),\
#                       ((2,0),(3,0)),((3,0),(4,0)),((0,0),(1,0))]
#     G.add_edges_from(edges)
#     return G
#pos = nx.get_node_attributes(G,'position')
#labels = nx.get_node_attributes(G,'reward')
#nx.draw(G, pos=pos, labels=labels, with_labels=True)

def plot_reward_map(gamestate, ax):
    pos = {}
    labels = {}
    for node in gamestate.G.nodes:
        pos[node] = node
        labels[node] = gamestate.G.nodes[node]['reward']
    nx.draw(gamestate.G, pos=pos, ax=ax, labels=labels, with_labels=True)
    
def plot_path(path, ax, style):
    X = []
    Y = []
    for node in path:
        X.append(node[0])
        Y.append(node[1])
    #style = random.sample(['ro-','b*-','go-','mo-','yo-','ko-'],1)[0]
    ax.plot(X,Y,style)
    
def reward_no_attack(starts_):
    starts = {}
    for robot in starts_:
        starts[robot] = starts_[robot][0]
    #!!!!change the game definition 
    board = setup_game()
    game = GameState_no_attack(board, starts)
    #computational budget
    budget = 400;
    
    # game_traj.add_node(starts, attri_dict={'state':game})
    # last_node = starts
    path = [starts]
    
    while not game.is_terminal():
        #initialize a MCTS object
        MCTS = MCTSPolicy_no_attack(game)
        for i in range(budget):
            #select the node to expand in search tree
            node_exp = MCTS.selection(0)
            #expand the node and return the frontier node
            node_fron = MCTS.expansion(node_exp)
            #rollout from frontier node
            reward = MCTS.simulation(node_fron)
            #backpropgration
            MCTS.backpropagation(node_fron, reward)
        #nx.draw(MCTS.digraph, with_labels = True)
        
        #select one action based on Monte Carlo tree 
        #based on UTC
        #Todo: other criterion
        # {UCT: action}
        UCT_A = {}
        for node in MCTS.digraph.successors(0):
            #print(node)
            UCT_A[MCTS.digraph.nodes[node]['uct']] = \
                MCTS.digraph.edges[0, node]['action']
        assert UCT_A, 'UCT_A is empty'
        action = UCT_A[max(UCT_A)]
        game.move(action)
        # game_traj.add_node(action, state=copy.deepcopy(game))
        # game_traj.add_edge(last_node, action)
        # last_node = action
        path.append(action)
    # fig, ax = plt.subplots()
    # plot_reward_map(game, ax)
    # #test
    # #path = [(0,0),(0,1),(1,1),(1,2),(2,2),(2,3)]
    # for robot in path[0]:
    #     traj = [node[robot] for node in path]
    #     plot_path(traj, ax)
    return game.collected_reward()

def all_paths(starts, game):
    trees = {}
    curr_nodes = {}
    node_counter = {}
    for robot in starts:
        node_counter[robot] = 0
        trees[robot] = nx.DiGraph()
        #keep track of the nodes at current depth
        #they are positions on the board
        curr_nodes[robot] = {node_counter[robot]:starts[robot][0]}
        trees[robot].add_node(node_counter[robot], pos = starts[robot][0])
        node_counter[robot] += 1
        
    for i in range(game.horizon):
        next_nodes = {}
        for robot in starts:
            #print('expand robot {}'.format(robot))
            next_nodes[robot] = {}
            #print('current frontier: {}'.format(curr_nodes[robot]))
            for node in curr_nodes[robot]:
                #print('consider node {}'.format(node))
                position = curr_nodes[robot][node]
                #print('its position is {}'.format(position))
                #print('its neighbor are {}'.format(list(game.G.neighbors(position))))
                for neighbor in game.G.neighbors(position):
                        #print('{} is added'.format(neighbor))
                        next_nodes[robot][node_counter[robot]] = neighbor
                        trees[robot].add_node(node_counter[robot], pos=neighbor)
                        trees[robot].add_edge(node, node_counter[robot])
                        node_counter[robot] += 1
        curr_nodes = copy.deepcopy(next_nodes) 
    
    #pos = nx.get_node_attributes(trees[0], 'pos') 
    # nx.draw(trees[0],  with_labels=True)
    paths = {}
    for r in starts:
        paths[r] = []
        for node in trees[r]:
            if trees[r].out_degree(node) == 0:
                sp = nx.shortest_path(trees[r], 0, node)
                path = [trees[r].nodes[node]['pos'] for node in sp]
                if len(list(set(path))) == len(path):
                    #print(path)
                    paths[r].append(path)
    return paths

def all_attacks(robots, game):
    '''

    Parameters
    ----------
    robots : list [0,1,2]
        DESCRIPTION.
    game : game state
        DESCRIPTION.

    Returns
    -------
    attacks : all posstible attacks to robots at any time
        DESCRIPTION.

    '''
    #return all attacks [{(robots):(time)}]
    H = game.horizon
    alpha = game.ALPHA
    attacks = []
    for pair in combinations(robots, alpha):
        #print('this time attack robots {}'.format(pair))
        L = len(pair)
        T = [list(range(1,H+1)) for i in range(L)]
        for att_time in product(*T):
            #print('attack time is {}'.format(att_time))
            attacks.append(dict(zip(pair, att_time)))
    return attacks
        
        
def compute_reward(game, path, attack):
    '''
    Parameters
    ----------
    game : game state
        DESCRIPTION.
    path : (path1, path2,) each path is a list [(0,1),(2,3)]
        DESCRIPTION.
    attacks : {robot:attack time} 
        DESCRIPTION.

    Returns
    -------
    reward

    '''
    visited_nodes = []
    
    for r in range(len(path)):
        if r in attack.keys():
            visited_nodes += path[r][0:attack[r]+1]
        else:
            visited_nodes += path[r]
    
    visited_nodes = list(set(visited_nodes))
    reward = 0
    for node in visited_nodes:
        reward += game.G.nodes[node]['reward']
    return reward

    
        
    
    