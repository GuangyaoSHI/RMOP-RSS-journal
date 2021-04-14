# https://stackoverflow.com/questions/11479624/is-there-a-way-to-guarantee-hierarchical-output-from-networkx
import networkx as nx
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
import matplotlib.pyplot as plt

G = nx.DiGraph()

G.add_node("ROOT")

for i in range(5):
    G.add_node("Child_%i" % i)
    G.add_node("Grandchild_%i" % i)
    G.add_node("Greatgrandchild_%i" % i)

    G.add_edge("ROOT", "Child_%i" % i)
    G.add_edge("Child_%i" % i, "Grandchild_%i" % i)
    G.add_edge("Grandchild_%i" % i, "Greatgrandchild_%i" % i)
G.add_node('pos:' + str({1: (1, 1)}) + '\n' +' UCT:' + str(23))
# write dot file to use with graphviz
# run "dot -Tpng test.dot >test.png"
write_dot(G, 'test.dot')
# dot -Tpng test.dot >test.png
from graphviz import Source

s = Source.from_file('test.dot')
s.view()

# same layout using matplotlib with no labels
plt.title('draw_networkx')
pos = graphviz_layout(G, prog='dot')
nx.draw(G, pos, with_labels=True, arrows=True)
plt.show()
plt.savefig('nx_test.png')

plt.title('test tree')
pos = graphviz_layout(MCTS.digraph, prog='dot')
nx.draw(MCTS.digraph, pos, with_labels=True, arrows=True)
plt.show()
write_dot(MCTS.digraph, 'MCTS.dot')

# read dot file
# https://stackoverflow.com/questions/41942109/plotting-the-digraph-with-graphviz-in-python-from-dot-file
from graphviz import Source

s = Source.from_file('MCTS.dot')
s.view()


import matplotlib.pyplot as plt
import numpy as np
all_data = [np.random.normal(0, std, size=100) for std in range(1, 4)]

# https://www.geeksforgeeks.org/box-plot-in-python-using-matplotlib/
# https://matplotlib.org/stable/gallery/statistics/boxplot_color.html#sphx-glr-gallery-statistics-boxplot-color-py


import matplotlib.pyplot as plt
from PIL import Image
img = Image.open('0.png').convert('LA')
img.save('tunnel.png')
img = plt.imread('tunnel.png')

from skimage import io
img = io.imread('0.png', as_gray=True)
img1 = img[10:1000, 600:1120]
fig, ax = plt.subplots()
ax.imshow(img1, cmap=plt.get_cmap('gray'), vmin=0, vmax=1)
# ax.scatter([600, 750], [400, 100])
plt.show()

for node in game.G.nodes:
    pos = coordinates[index2coordinates[node]-1]
    game.G.nodes[node]['position'] = (pos[0], 950-pos[1])

