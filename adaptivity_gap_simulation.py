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

def generate_sparse_graph(graph):
    sparse_G = copy.deepcopy(graph)
    # try to remove some edges
    for i in range(int(len(list(graph))/2)):
        edge = random.sample(list(sparse_G.edges), 1)[0]
        G = copy.deepcopy(sparse_G)
        G.remove_edge(*edge)
        if nx.is_connected(G):
            sparse_G.remove_edge(*edge)
    return sparse_G

def plot_grid_map(grid_graph):
    pos = {}
    labels = {}
    for node in grid_graph.nodes:
        pos[node] = node
        labels[node] = grid_graph.nodes[node]['reward']
    nx.draw(grid_graph, pos=pos, labels=labels, with_labels=True)
    plt.show()


# params = [0.3, 0.6, 0.8, 1.2]
params = [0.6, 0.8]
grid_len = 15
grid_height = 15
graphs = []

# generate maps
for param in params:
    graph = generate_grid_map(grid_len, grid_height, param)
    graph = generate_sparse_graph(graph)
    graphs.append(graph)
    # plot_grid_map(graph)

# with open("graphs.txt", "rb") as fp:  # Unpickling
#     # graphs_adap = [results_adap]
#     graphs = pickle.load(fp)


# robot parameters
horizon = 3
# number of robots
N = 4
# number of total attacks
alpha = 2
# iteration budget
budgets = [100, 200, 400, 600, 800]
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
        # path_attack is a reward
        reward_worst = brute_force(start, graph, horizon, alpha)
        results_adap['bruteforce'].append(reward_worst)
        # MCTS methods with different budgets
        for budget in budgets:
            # change play_game with attacker behavior arg
            # each budget run for 5 times
            for i in range(5):
                game = play_game(budget, start, graph, horizon, alpha, 'mcts', 'mcts')
                results_adap['AdversarialMCTS'][budget].append(game)
    graphs_adap.append(results_adap)

with open("graphs_adap" + ".txt", "wb") as fp:  # Pickle
    pickle.dump(graphs_adap, fp)
