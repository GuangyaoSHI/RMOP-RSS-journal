# https://www.medcalc.org/manual/exponential_distribution_functions.php
# https://numpy.org/doc/stable/reference/random/generated/numpy.random.exponential.html
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
from play_game import *
from brute_force_baseline import *
from utilities import *


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
    # plot_grid_map(graph)

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

# results for all graphs
graphs_adap = []

for graph in graphs:
    # results to show adaptivity gap
    results_adap = {'AdversarialMCTS': dict(zip(budgets, [[]] * len(budgets))), 'bruteforce': []}
    for start_ in starts:
        state = [[pos, 0] for pos in start_]
        start = dict(zip(range(N), state))
        # brute_force non-adaptive method
        # path_attack is a tuple (path, attacks)
        path_attack = brute_force(start, graph, horizon, alpha)
        results_adap['bruteforce'].append(path_attack)
        # MCTS methods with different budgets
        for budget in budgets:
            # change play_game with attacker behavior arg
            # each budget run for 5 times
            for i in range(5):
                game = play_game(budget, start, graph, horizon, alpha, 'mcts')
                results_adap['AdversarialMCTS'][budget].append(game)
    graphs_adap.append(results_adap)

with open("graphs_adap" + ".txt", "wb") as fp:  # Pickle
    pickle.dump(graphs_adap, fp)

# compare different methods
# robot parameters
horizon = 10
# number of robots
N = 4
# number of total attacks
alpha = 2
# iteration budget
budgets = [800] * 3

graphs_comparison =[]
for graph in graphs:
    # Todo: policy of robots that doesn't consider attacks
    results_compare = {'AMCTS_VS_AMCTS': dict(zip(budgets, [[]] * len(budgets))),
                       'AMCTS_VS_random': dict(zip(budgets, [[]] * len(budgets))),
                       'random_VS_AMCTS': dict(zip(budgets, [[]] * len(budgets))),
                       'random_VS_random': dict(zip(budgets, [[]] * len(budgets)))
                       }
    for start in starts:
        # MCTS methods with different budgets
        for budget in budgets:
            # change play_game with attacker behavior arg
            game = play_game(budget, start, graph, horizon, alpha, 'mcts', 'mcts')
            results_compare['AMCTS_VS_AMCTS'][budget].append(game)
            game = play_game(budget, start, graph, horizon, alpha, 'mcts', 'random')
            results_compare['AMCTS_VS_random'][budget].append(game)
            game = play_game(budget, start, graph, horizon, alpha, 'random', 'mcts')
            results_compare['random_VS_AMCTS'][budget].append(game)
            game = play_game(budget, start, graph, horizon, alpha, 'random', 'random')
            results_compare['random_VS_random'][budget].append(game)
    graphs_comparison.append(results_compare)

with open("compare_different_methods" + ".txt", "wb") as fp:  # Pickle
    pickle.dump(graphs_comparison, fp)