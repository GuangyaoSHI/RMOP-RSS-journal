import networkx as nx
import pickle
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import numpy as np

from skimage import io
from skimage.morphology import skeletonize
from skimage import data
from skimage.feature import corner_harris, corner_subpix, corner_peaks
import matplotlib.pyplot as plt
from skimage.util import invert

image = io.imread('1.png', as_gray=True)
# Invert the horse image
image = invert(image)

# # perform skeletonization
skeleton = skeletonize(image, method='lee')
skeleton = invert(skeleton)
coords = corner_peaks(corner_harris(skeleton), min_distance=16, threshold_rel=0.12)
coords_subpix = corner_subpix(skeleton, coords, window_size=20)

# create one abstract graph
# image = io.imread('1.png')
fig, ax = plt.subplots()
# ax.imshow(skeleton, cmap=plt.cm.gray, vmin=0, vmax=1, alpha=0.2)
scale_x = 1
scale_y = 1
graph = nx.Graph()
# values = np.random.exponential(scale=0.2, size=(coords.shape[0],))
# values = np.ceil(values * 20)
# values = values.astype(int)
values = np.array([2, 9, 6, 4, 5, 8, 9, 5, 1, 7, 3, 5, 3, 13, 5, 5, 1,
                   2, 4, 2, 1, 10, 2, 2, 13, 3, 2, 8, 5, 2, 11, 3, 1, 1,
                   9, 1, 1, 1, 3, 10, 1, 2, 15, 2, 14, 1, 12, 2, 4, 3, 2,
                   4, 4, 8, 1, 13, 3, 5, 3, 2, 2, 7, 9, 16, 3, 14, 13, 3,
                   2])
for i in range(coords.shape[0]):
    graph.add_node(i, position=(coords[i, 1] * scale_x, coords[i, 0] * scale_y), label=i, reward=values[i])

edges = [(53, 11), (11, 29), (29, 58), (29, 54), (54, 32), (57, 32), (58, 0), (32, 6), (6, 0), (6, 14),
         (0, 18), (0, 13), (18, 45), (13, 17), (14, 48), (14, 15), (14, 28), (15, 39), (39, 4), (4, 35), (35, 41),
         (35, 63), (15, 28), (4, 43), (28, 43), (28, 19), (19, 42), (19, 30), (42, 9), (9, 61), (61, 27), (27, 7),
         (27, 56), (7, 50), (7, 65), (7, 67), (9, 59), (59, 30), (30, 25), (25, 36), (25, 40), (40, 34), (40, 1),
         (34, 33), (33, 66), (1, 51), (1, 2), (2, 37), (37, 52), (33, 66), (34, 31), (31, 62), (62, 12), (12, 21),
         (21, 10), (10, 44), (44, 49), (10, 5), (5, 68), (21, 64), (64, 3), (3, 8), (8, 55), (3, 26), (26, 23),
         (23, 47), (23, 24), (24, 38), (64, 38), (38, 22), (22, 60), (63, 16), (16, 46), (16, 20), (8, 20), (20, 26),
         (33, 1), (13, 18), (46, 20), (3, 38)]
graph.add_edges_from(edges)
pos = nx.get_node_attributes(graph, 'position')
labels = nx.get_node_attributes(graph, 'label')
reward = nx.get_node_attributes(graph, 'reward')
node_sizes = [6 + graph.nodes[node]['reward'] * 3 for node in graph.nodes]
node_colors = [graph.nodes[node]['reward'] for node in graph.nodes]
ax.set_aspect('equal', 'box')
cm = plt.get_cmap('jet')
# ax.set_xlim(0, skeleton.shape[1]*scale_x)
# ax.set_ylim(0, skeleton.shape[0]*scale_y)
from matplotlib import pyplot

pyplot.gca().invert_yaxis()
# ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
nx.draw(graph, pos=pos, ax=ax, labels=labels, with_labels=False, font_size=3, node_size=node_sizes, cmap=cm,
        node_color=node_colors, font_color='w', font_weight='roman')
# sm = plt.cm.ScalarMappable(cmap=cm)
# sm._A = []
# plt.colorbar(sm)
plt.savefig('tunnel_graph' + '.pdf', bbox_inches='tight', pad_inches=0)
plt.show()

# plot the tunnel and selected points
fig, ax = plt.subplots()
ax.imshow(invert(image), cmap=plt.cm.gray, alpha=0.6)
# ax.plot(coords[:, 1], coords[:, 0], color='cyan', marker='o',
#         linestyle='None', markersize=3)
ax.scatter(coords[:, 1], coords[:, 0], c=node_colors, s=node_sizes, marker='o', cmap=plt.cm.jet)
# for i in range(coords.shape[0]):
#     ax.text(coords[i, 1], coords[i, 0], str(i))
# ax.plot(coords_subpix[:, 1], coords_subpix[:, 0], '+r', markersize=15)
# ax.axis((0, 310, 200, 0))
normlizer = matplotlib.colors.Normalize(vmin=0, vmax=1)
cbar = plt.colorbar(matplotlib.cm.ScalarMappable(norm=normlizer,
                                                 cmap=plt.cm.jet))
cbar.ax.get_yaxis().labelpad = 10
cbar.ax.set_ylabel('Normalized Reward', rotation=270)
ax.axis('off')
plt.savefig('tunnel' + '.pdf', bbox_inches='tight', pad_inches=0)
plt.show()



# find shortest distance
# for i in range(coords.shape[0]):
#     if not skeleton[coords[i, 0], coords[i, 1]] > 0:
#         print(coords[i, :])

plt.imshow(skeleton, cmap=plt.cm.gray)
plt.show()

G_image = nx.Graph()
for i in range(2, skeleton.shape[1] - 1):
    for j in range(2, skeleton.shape[0] - 1):
        G_image.add_node((i, j), value=skeleton[j, i])
        if not skeleton[j, i] > 0:
            continue
        neighbors = [(i - 1, j), (i + 1, j), (i, j + 1), (i, j - 1)]
        for neighbor in neighbors:
            if skeleton[neighbor[1], neighbor[0]] > 0:
                G_image.add_edge((i, j), neighbor)

# sp = nx.shortest_path(G_image, source=(coords[1, 1], coords[1, 0]), target=(coords[10, 1], coords[10, 0]))
# X = [point[0] for point in sp]
# Y = [point[1] for point in sp]
plt.imshow(skeleton, cmap=plt.cm.gray)
# plt.plot(X, Y, marker='x', color='r')
plt.savefig('skeleton' + '.pdf', bbox_inches='tight', pad_inches=0)
plt.show()

# add edge weight
for edge in graph.edges:
    i, j = edge
    source = (coords[i, 1], coords[i, 0])
    target = (coords[j, 1], coords[j, 0])
    sp = nx.shortest_path(G_image, source=source, target=target)
    # print('path length {}'.format(len(sp)))
    # nx.set_edge_attributes(graph, values=len(sp), name='weight')
    graph.edges[i, j]['weight'] = len(sp)

# save the graph
with open("graph_tunnel" + ".txt", "wb") as fp:  # Pickle
    pickle.dump(graph, fp)

# for visualization
fig, ax = plt.subplots(1, 2)
background = io.imread('1.png', as_gray=True)
ax[0].imshow(background, cmap=plt.cm.gray)
ax[0].scatter(coords[:, 1], coords[:, 0], c='cyan', s=3, marker='o')
for i in range(coords.shape[0]):
    ax[0].text(coords[i, 1], coords[i, 0], str(i), size=4, color='red', fontweight='roman')
ax[0].axis('off')
ax[1].set_aspect('equal', 'box')
from matplotlib import pyplot

pyplot.gca().invert_yaxis()
# ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
weighted_edges = nx.draw_networkx_edge_labels(graph, pos=pos, edge_labels=nx.get_edge_attributes(graph, 'weight'),
                                              font_size=4, verticalalignment='top', horizontalalignment='left')

nx.draw(graph, pos=pos, ax=ax[1], labels=labels, with_labels=True, font_size=4, node_size=30)
plt.savefig('tunnel_graph_visualization' + '.pdf', bbox_inches='tight', pad_inches=0)
plt.show()


