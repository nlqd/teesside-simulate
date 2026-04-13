import math
import itertools
import numpy as np

# import tkinter
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import time
import os
import matplotlib.colors as mcolors

def fermi(focal, neighbor, K=0.3):
    return 1 / (1 + pow(math.e, (focal - neighbor) / K))

def calculate_fitness(population, payoff_matrix):
    size_x, size_y = population.shape
    fitnesses = np.zeros((size_x, size_y))

    for i in range(size_x):
        for j in range(size_y):
            strategy = population[i, j]
            total_payoff = 0
            neighbors = []
            if i > 0:
                neighbors.append((i - 1, j))
            if i < size_x - 1:
                neighbors.append((i + 1, j))
            if j > 0:
                neighbors.append((i, j - 1))
            if j < size_y - 1:
                neighbors.append((i, j + 1))

            for x, y in neighbors:
                neighbor_strategy = population[x, y]
                total_payoff += payoff_matrix[strategy][neighbor_strategy]

            fitnesses[i, j] = total_payoff

    return fitnesses

def calculate_fitness_pgg(population, r=3.0):
    """
    Multi-group spatial PGG following Flores & Han (2024),
    doi:10.1016/j.amc.2024.128646, detail: ./pgg-lattice

    Each agent participates in all groups it belongs to: one centred on itself
    and one centred on each von Neumann neighbour. For each group g of size G_g:
        share = r * k_g / G_g
    Contribution cost of 1 is paid once per group the agent cooperates in.
    Boundary handling is non-periodic, consistent with calculate_fitness (PD).
    """
    size_x, size_y = population.shape
    fitnesses = np.zeros((size_x, size_y))

    def neighbors(i, j):
        nbrs = []
        if i > 0:           nbrs.append((i - 1, j))
        if i < size_x - 1:  nbrs.append((i + 1, j))
        if j > 0:           nbrs.append((i, j - 1))
        if j < size_y - 1:  nbrs.append((i, j + 1))
        return nbrs

    def group_share(ci, cj):
        members = [(ci, cj)] + neighbors(ci, cj)
        k_g = sum(1 for x, y in members if population[x, y] == 'C')
        return r * k_g / len(members)

    for i, j in itertools.product(range(size_x), range(size_y)):
        groups = [(i, j)] + neighbors(i, j)
        total_share = sum(group_share(gi, gj) for gi, gj in groups)
        n_groups = len(groups)
        contribution_cost = n_groups if population[i, j] == 'C' else 0
        fitnesses[i, j] = total_share - contribution_cost

    return fitnesses

def visualize_population(population):
    color_map = {'C': 'blue', 'D': 'red'}
    color_grid = np.vectorize(color_map.get)(population)

    plt.imshow(color_grid, interpolation='nearest')
    plt.axis('off')
    save_figure(plt, filename=f"population_{int(time.time())}.png")


def save_figure(plt, filename="figure.png"):
    # Ensure target directory exists before saving the figure
    dirpath = os.path.dirname(filename)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)
    plt.savefig(filename)
    plt.close()
