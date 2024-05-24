import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from tests import test_graphs_from_generate


def paint(x, y, Z):

    X, Y = np.meshgrid(x, y)

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    ax.plot_surface(X, Y, Z,cmap='viridis')

    ax.set_xlabel('Nodes')
    ax.set_ylabel('Edges')
    ax.set_zlabel('Seconds')

    plt.show()


if __name__ == "__main__":
    nodes = np.arange(50, 501, 50)
    edges = np.arange(1000, 10001, 1000)
    result_edmonds = np.empty((10, 10))
    result_dinic = np.empty((10, 10))
    for j in range(10):
        for i in range(10):
            result = test_graphs_from_generate(nodes[i], 100, edges[j], 20)
            result_edmonds[j][i] = result["edmonds_worse_time"]
            result_dinic[j][i] = result["dinic_worse_time"]
    paint(nodes, edges, result_edmonds)
    paint(nodes, edges, result_dinic)