# https://www.medcalc.org/manual/exponential_distribution_functions.php
# https://numpy.org/doc/stable/reference/random/generated/numpy.random.exponential.html
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
from play_game import *
from brute_force_baseline import *
from utilities import *
from basic_path_planning import *

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


params = [0.1, 0.4, 0.8, 1.6]
grid_len = 15
grid_height = 15
graphs = []

# generate maps
for param in params:
    graph = generate_grid_map(grid_len, grid_height, param)
    graphs.append(graph)
    # plot_grid_map(graph)

# with open("graphs.txt", "rb") as fp:  # Unpickling
#     # graphs_adap = [results_adap]
#     graphs = pickle.load(fp)

# compare different methods
# robot parameters
horizon = 8
# number of robots
N = 4
# number of total attacks
alpha = 2
# iteration budget
budget = 500
# generate starting positions of robots
starts = [random.sample(list(graphs[0].nodes), N) for i in range(10)]

graphs_comparison = []
for graph in graphs:
    # Todo: policy of robots that doesn't consider attacks
    results_compare = {'AMCTS_VS_AMCTS': [],
                       'AMCTS_VS_random': [],
                       'random_VS_AMCTS': [],
                       'random_VS_random': [],
                       'MCTS_VS_AMCTS': [],
                       'MCTS_VS_random': []
                       }
    for start_ in starts:
        state = [[pos, 0] for pos in start_]
        start = dict(zip(range(N), state))
        # MCTS methods with different budgets
        for i in range(6):
            # naive planning
            world_map, game = naive_planning(budget, start, graph, horizon, alpha, 'mcts')
            results_compare['MCTS_VS_AMCTS'].append(game)
            # print(results_compare)
            world_map, game = naive_planning(budget, start, graph, horizon, alpha, 'random')
            results_compare['MCTS_VS_random'].append(game)
            # change play_game with attacker behavior arg
            game = play_game(budget, start, graph, horizon, alpha, 'mcts', 'mcts')
            results_compare['AMCTS_VS_AMCTS'].append(game)
            game = play_game(budget, start, graph, horizon, alpha, 'mcts', 'random')
            results_compare['AMCTS_VS_random'].append(game)
            game = play_game(budget, start, graph, horizon, alpha, 'random', 'mcts')
            results_compare['random_VS_AMCTS'].append(game)
            game = play_game(budget, start, graph, horizon, alpha, 'random', 'random')
            results_compare['random_VS_random'].append(game)

    graphs_comparison.append(results_compare)

with open("compare_different_methods" + ".txt", "wb") as fp:  # Pickle
    pickle.dump(graphs_comparison, fp)

with open("graphs" + ".txt", "wb") as fp:  # Pickle
    pickle.dump(graphs, fp)