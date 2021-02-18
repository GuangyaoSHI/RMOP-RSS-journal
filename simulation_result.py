# https://www.medcalc.org/manual/exponential_distribution_functions.php
# https://numpy.org/doc/stable/reference/random/generated/numpy.random.exponential.html
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
from play_game import *

def generate_grid_map(grid_len, grid_height, parameters):
    # generate a grid graph with size=(grid_len, grid_height)
    # parameters are for probability distribution. Here we use exponential distribution
    graph = nx.grid_2d_graph(grid_len, grid_height)
    values = np.random.exponential(scale=parameters, size=(grid_len * grid_height,))
    values = np.around(values*20)
    values = values.astype(int)
    reward = dict(zip(list(graph.nodes), values))
    nx.set_node_attributes(graph, reward, 'reward')
    return graph


def plot_grid_map(grid_graph):
    pos = {}
    labels = {}
    for node in grid_graph.nodes:
        pos[node] = node
        labels[node] = grid_graph.nodes[node]['reward']
    nx.draw(grid_graph, pos=pos, labels=labels, with_labels=True)
    plt.show()


params = [0.5, 1, 2, 4]
grid_len = 15
grid_height = 15
graphs = []

# generate maps
for param in params:
    graph = generate_grid_map(grid_len, grid_height, param)
    graphs.append(graph)
    plot_grid_map(graph)

# robot parameters
horizon = 4
# number of robots
N = 4
# number of total attacks
alpha = 2
# iteration budget
budgets = [200, 400, 600, 800, 1000]
# generate starting positions of robots
starts = [random.sample(list(graphs[0].nodes), N) for i in range(5)]

# results to show adaptivity gap
results_adap ={'AdversarialMCTS': dict(zip(budgets, [[]]*len(budgets))), 'bruteforce':[]}
for graph in graphs:
    for start in starts:
        # brute_force non-adaptive method
        # MCTS methods with different budgets
        for budget in budgets:
            game = play_game(budget, start, graph, horizon, alpha)
            results_adap['AdversarialMCTS'][budget].append(game)

# compare different methods
# change play_game with attacker behavior arg






