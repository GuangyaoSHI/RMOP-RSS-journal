from different_methods_simulation import *
import random

params = [0.3, 0.6]
grid_len = 15
grid_height = 15
graphs = []

# generate maps
# for param in params:
#     graph = generate_grid_map(grid_len, grid_height, param)
#     graph = generate_sparse_graph(graph)
#     graphs.append(graph)
# #  plot_grid_map(graph)
#
# with open("graphs" + ".txt", "wb") as fp:  # Pickle
#     pickle.dump(graphs, fp)

with open("graphs.txt", "rb") as fp:  # Unpickling
    # graphs_adap = [results_adap]
    graphs = pickle.load(fp)

# compare different methods
# robot parameters
horizon = 8
# number of robots
N = 4
# number of total attacks
alpha = 2
# iteration budget
budget = 1200


# generate starting positions of robots
starts = [random.sample(list(graphs[0].nodes), int(N / 2)) * 2 for i in range(3)]
filename = 'comparison-8'
compare_different_methods(graphs, horizon, N, alpha, budget, starts, filename)

# # generate starting positions of robots
# starts = [random.sample(list(graphs[0].nodes), int(N / 2)) * 2 for i in range(5)]
# filename = 'comparison-2-starting-position'
# compare_different_methods(graphs, horizon, N, alpha, budget, starts, filename)
#
#
# # generate starting positions of robots
# starts = []
# for i in range(5):
#     node0 = random.sample(list(graphs[0].nodes), 1)[0]
#     node1 = random.sample(list(graphs[0].neighbors(node0)), 1)[0]
#     node2 = random.sample(list(graphs[0].neighbors(node1)), 1)[0]
#     node3 = random.sample(list(graphs[0].neighbors(node2)), 1)[0]
#     starts.append([node0, node1, node2, node3])
#
# filename = 'comparison-random-starting'
# compare_different_methods(graphs, horizon, N, alpha, budget, starts, filename)
