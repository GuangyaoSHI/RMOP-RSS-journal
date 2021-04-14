import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
from play_game import *
from brute_force_baseline import *
from utilities import *
from basic_path_planning import *
import copy
import random
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

from different_methods_simulation import *

# params = [0.3, 0.6]
# grid_len = 15
# grid_height = 15
# graphs = []

# generate maps
# graph = generate_grid_map(grid_len, grid_height, params[0])
# graph = generate_sparse_graph(graph)
# plot_grid_map(graph)
# with open("graphs_vis" + ".txt", "wb") as fp:  # Pickle
#     pickle.dump(graphs, fp)

with open("graph_tunnel" + ".txt", "rb") as fp:  # Unpickling
    graph = pickle.load(fp)

# robot parameters
horizon = 8
# number of robots
N = 4
# number of total attacks
alpha = 2
# iteration budget
budget = 4000

# start = random.sample(list(graph.nodes), int(N))
start = [(-1.5, 2)] * N
start = [[pos, 0] for pos in start]
start = dict(zip(range(N), start))
# game = play_game(budget, start, graph, horizon, alpha, 'mcts', 'mcts')

# with open("game_tunnel" + ".txt", "wb") as fp:  # Pickle
#     pickle.dump(game, fp)

with open("game_tunnel"+".txt", "rb") as fp:  # Unpickling
    game = pickle.load(fp)

img = plt.imread('0.png')



styles = ['rs-', 'gD-', 'mp-', 'y*-']
fig1, axs1 = plt.subplots()
plot_reward_map(game, axs1)
robot = 0
X = [game.G.nodes[pos]['position'][0] for pos in game.paths_robots[robot]]
Y = [game.G.nodes[pos]['position'][1] for pos in game.paths_robots[robot]]
axs1.plot(X, Y, styles[robot], linewidth=4.5, alpha=0.7)
X = np.array(X)
Y = np.array(Y)
axs1.quiver(X[:-1], Y[:-1], X[1:]-X[:-1], Y[1:]-Y[:-1], scale_units='xy', angles='xy', scale=1.2)
axs1.plot(X[0], Y[0], styles[robot], markersize=15, alpha=0.8)
axs1.text(X[0]+12, Y[0]-15, r'$v_{s_0}$', fontsize=15)
fig1.savefig('robot-'+str(robot)+'-'+'path'+'.pdf', bbox_inches='tight', pad_inches=0)
plt.show()


fig2, axs2 = plt.subplots()
plot_reward_map(game, axs2)
robot = 1
X = [game.G.nodes[pos]['position'][0] for pos in game.paths_robots[robot]]
Y = [game.G.nodes[pos]['position'][1] for pos in game.paths_robots[robot]]
axs2.plot(X, Y, styles[robot], linewidth=4.5, alpha=0.7)
X = np.array(X)
Y = np.array(Y)
axs2.quiver(X[:-1], Y[:-1], X[1:]-X[:-1], Y[1:]-Y[:-1], scale_units='xy', angles='xy', scale=1.2)
axs2.plot(X[0], Y[0], styles[robot], markersize=15, alpha=0.8)
axs2.text(X[0]+12, Y[0]-15, r'$v_{s_1}$', fontsize=15)
axs2.plot(X[-1], Y[-1], 'rX', markersize=25)
fig2.savefig('robot-'+str(robot)+'-'+'path'+'.pdf', bbox_inches='tight', pad_inches=0)
plt.show()


fig3, axs3 = plt.subplots()
plot_reward_map(game, axs3)
robot = 2
X = [game.G.nodes[pos]['position'][0] for pos in game.paths_robots[robot]]
Y = [game.G.nodes[pos]['position'][1] for pos in game.paths_robots[robot]]
axs3.plot(X, Y, styles[robot], linewidth=4.5, alpha=0.7)
X = np.array(X)
Y = np.array(Y)
axs3.quiver(X[:-1], Y[:-1], X[1:]-X[:-1], Y[1:]-Y[:-1], scale_units='xy', angles='xy', scale=1.2)
axs3.plot(X[0], Y[0], styles[robot], markersize=15, alpha=0.8)
axs3.text(X[0]+12, Y[0]-15, r'$v_{s_2}$', fontsize=15)
axs3.plot(X[-1], Y[-1], 'rX', markersize=25)
fig3.savefig('robot-'+str(robot)+'-'+'path'+'.pdf', bbox_inches='tight', pad_inches=0)
plt.show()


fig4, axs4 = plt.subplots()
plot_reward_map(game, axs4)
robot = 3
X = [game.G.nodes[pos]['position'][0] for pos in game.paths_robots[robot]]
Y = [game.G.nodes[pos]['position'][1] for pos in game.paths_robots[robot]]
axs4.plot(X, Y, styles[robot], linewidth=4.5, alpha=0.7)
X = np.array(X)
Y = np.array(Y)
axs4.quiver(X[:-1], Y[:-1], X[1:]-X[:-1], Y[1:]-Y[:-1], scale_units='xy', angles='xy', scale=1.2)
axs4.plot(X[0], Y[0], styles[robot], markersize=15, alpha=0.8)
axs4.text(X[0]+12, Y[0]-15, r'$v_{s_3}$', fontsize=15)
fig4.savefig('robot-'+str(robot)+'-'+'path'+'.pdf', bbox_inches='tight', pad_inches=0)
plt.show()


fig, axs = plt.subplots(2, 2)
for axis in list(product(list(range(2)), list(range(2)))):
    i, j = axis
    plot_reward_map(game, axs[i, j])

for axis in list(product(list(range(2)), list(range(2)))):
    i, j = axis
    robot = 2 * i + j
    X = [game.G.nodes[pos]['position'][0] for pos in game.paths_robots[robot]]
    Y = [game.G.nodes[pos]['position'][1] for pos in game.paths_robots[robot]]
    axs[i, j].plot(X, Y, styles[robot])
plt.show()


# T = len(game.paths_robots[0])
# for robot in range(N):
#     X = [pos[0] for pos in game.paths_robots[robot]]
#     Y = [pos[1] for pos in game.paths_robots[robot]]
#     axs.plot(X, Y, styles[robot])


