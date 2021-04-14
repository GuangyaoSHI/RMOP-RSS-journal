import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import random
from play_game import *
from brute_force_baseline import *
from utilities import *
import pickle
import copy

# with open("graphs_adap.txt", "rb") as fp:  # Unpickling
#     # graphs_adap = [results_adap]
#     graphs_adap = pickle.load(fp)
#
# for i in range(len(graphs_adap)):
#     result_adap = graphs_adap[i]
#     fig, axs = plt.subplots()
#     # labels are about budgets
#     budgets = [100, 200, 400, 600, 800]
#     all_data = []
#     for budget in budgets:
#         data = [game.collected_reward() for game in result_adap['AdversarialMCTS'][budget]]
#         all_data.append(np.array(data))
#     all_data.append(np.array(result_adap['bruteforce']))
#     labels = budgets + ['BF']
#     bp = axs.boxplot(all_data,
#                      vert=True,
#                      #  patch_artist=True,
#                      labels=labels)
#     axs.set_title('graph' + str(i))
#     axs.set_xlabel('different groups')
#     axs.set_ylabel('reward')
#     plt.show()
#     fig.savefig('graph' + str(i) + '-' + 'adaptivity' + '.pdf',bbox_inches = 'tight',
#     pad_inches = 0)


filename = 'comparison-6'
with open(filename+".txt", "rb") as fp:  # Unpickling
    graphs_compare = pickle.load(fp)

for i in range(len(graphs_compare)):
    result_compare = graphs_compare[i]
    fig, axs = plt.subplots()
    all_data = []
    max_reward = 0
    keys = [# 'random_VS_AMCTS',
            # 'random_VS_random',
            'MCTS_VS_AMCTS',
            'AMCTS_VS_AMCTS',
            'MCTS_VS_random',
            'AMCTS_VS_random']
    for key in keys:
        new_data = np.array([game.collected_reward() for game in result_compare[key]])
        if np.amax(new_data) > max_reward:
            max_reward = np.amax(new_data)
        all_data.append(new_data)
    original_data = copy.deepcopy(all_data)
    # all_data = [data/max_reward for data in all_data]
    all_data = [data for data in all_data]
    labels = ['M-Ma', 'Ma-Ma', 'M-R','Ma-R']
    bp = axs.boxplot(all_data,
                     vert=True,
                     # patch_artist=True,
                     labels=labels)
    axs.set_title('Compare different strategies: robot-adversary')
    # axs.set_xlabel('different groups')
    axs.set_ylabel('Normalized reward')
    plt.show()
    fig.savefig(filename+'graph' + str(i) + '-' + '.pdf', bbox_inches = 'tight', pad_inches = 0)

    x = np.arange(len(labels))
    width = 0.8
    fig, axs = plt.subplots()
    error_kw = {'capthick' : 1.5, 'ecolor' : 'black', 'linestyle' : ':', 'alpha' : 0.7, 'capsize' : 6}
    axs.bar(x[0], np.mean(all_data[0]), width, label='M-Ma', yerr=np.std(all_data[0]), error_kw=error_kw)
    axs.bar(x[1], np.mean(all_data[1]), width, label='Ma-Ma', yerr=np.std(all_data[1]), error_kw=error_kw)
    axs.bar(x[2], np.mean(all_data[2]), width, label='M-R', yerr=np.std(all_data[2]), error_kw=error_kw)
    axs.bar(x[3], np.mean(all_data[3]), width, label='Ma-R', yerr=np.std(all_data[3]), error_kw=error_kw)
    axs.set_xticks(x)
    axs.set_xticklabels(labels)
    axs.set_title('Compare different strategies: robot-adversary')
    axs.set_ylabel('Reward')
    axs.set(ylim=(120, 300))
    plt.show()
    fig.savefig(filename+'-bar-'+'graph' + str(i) + '-' + '.pdf', bbox_inches='tight', pad_inches = 0)








