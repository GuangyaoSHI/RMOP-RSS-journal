import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
from play_game import *
from brute_force_baseline import *
from utilities import *
import pickle

with open("graphs_adap.txt", "rb") as fp:  # Unpickling
    # graphs_adap = [results_adap]
    graphs_adap = pickle.load(fp)

for i in range(len(graphs_adap)):
    result_adap = graphs_adap[i]
    fig, axs = plt.subplots()
    # labels are about budgets
    budgets = [200, 400, 600, 800, 1000]
    all_data = []
    for budget in budgets:
        data = [game.collected_reward() for game in result_adap['AdversarialMCTS'][budget]]
        all_data.append(np.array(data))
    all_data.append(np.array(result_adap['bruteforce']))
    labels = budgets + ['BF']
    bp = axs.boxplot(all_data,
                     vert=True,
                     #  patch_artist=True,
                     labels=labels)
    axs.set_title('graph' + str(i))
    axs.set_xlabel('different groups')
    axs.set_ylabel('reward')
    plt.show()
    fig.savefig('graph' + str(i) + '-' + 'adaptivity' + '.pdf')

with open("compare_different_methods.txt", "rb") as fp:  # Unpickling
    graphs_compare = pickle.load(fp)

for i in range(len(graphs_compare)):
    result_compare = graphs_compare[i]
    fig, axs = plt.subplots()
    all_data = []
    max_reward = 0
    for key in result_compare:
        new_data = np.array([game.collected_reward() for game in result_compare[key]])
        if np.amax(new_data) > max_reward:
            max_reward = np.amax(new_data)
        all_data.append(new_data)
    all_data = [data/max_reward for data in all_data]
    labels = ['Ma-Ma', 'Ma-R', 'R-Ma', 'R-R', 'M-Ma', 'M-R']
    bp = axs.boxplot(all_data,
                     vert=True,
                     # patch_artist=True,
                     labels=labels)
    axs.set_title('graph' + str(i))
    axs.set_xlabel('different groups')
    axs.set_ylabel('reward')
    plt.show()
    fig.savefig('graph' + str(i) + '-' + 'comparison' + '.pdf')
