import pickle
from utilities import *
import pydot

with open("trees.txt", "rb") as fp:  # Unpickling
    trees = pickle.load(fp)

with open("rewards.txt", "wb") as fp:   #Pickle
    pickle.dump([], fp)

for i in range(len(trees['attacker'])):
    visualize_MCTS(MCTS=trees['attacker'][i], fileName='attacker' + str(i) + '.dot')
    (graph,) = pydot.graph_from_dot_file('attacker' + str(i) + '.dot')
    graph.write_pdf('attacker' + str(i) + '.pdf')
    visualize_MCTS(MCTS=trees['robot'][i], fileName='robot' + str(i) + '.dot')
    (graph,) = pydot.graph_from_dot_file('robot' + str(i) + '.dot')
    graph.write_pdf('robot' + str(i) + '.pdf')

# brute force 1
24
# MCTS 1
import pickle
import numpy as np
import matplotlib.pyplot as plt
with open("rewards.txt", "rb") as fp:  # Unpickling
    rewards = pickle.load(fp)

fig, axs = plt.subplots(2, 2)

# frequency statistics
# https://www.w3resource.com/python-exercises/numpy/python-numpy-exercise-94.php
unique_elements, counts_elements = np.unique(rewards[100], return_counts=True)
axs[0, 0].bar(unique_elements, counts_elements)
axs[0, 0].set_ylabel('budget 100')

unique_elements, counts_elements = np.unique(rewards[400], return_counts=True)
axs[0, 1].bar(unique_elements, counts_elements)
axs[0, 1].set_ylabel('budget 400')

unique_elements, counts_elements = np.unique(rewards[800], return_counts=True)
axs[1, 0].bar(unique_elements, counts_elements)
axs[1, 0].set_ylabel('budget 800')

unique_elements, counts_elements = np.unique(rewards[1600], return_counts=True)
axs[1, 1].bar(unique_elements, counts_elements)
axs[1, 1].set_ylabel('budget 1600')

plt.show()
fig.savefig('different_budget.pdf')
# avg = np.mean(data) # 25.42
# std = np.std(data)  # 5.03




