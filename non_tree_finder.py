import itertools
import numpy as np
import copy as cp
from collections import OrderedDict
import matplotlib.pyplot as plt
import topology

INF = 9999
NODECNT = 0

avBranch = [[0, 2], [0, 3], [1, 2], [1, 3]]
avBranch2 = [[0, 3], [0, 4], [0, 5], [1, 3], [1, 4], [1, 5], [2, 3], [2, 4], [2, 5]]

def dfs(node, undirected_adjacency_matrix, book, vertex_num):
    global NODECNT
    NODECNT += 1
    if NODECNT == vertex_num:
        return
    for cnt in range(0, vertex_num):
        if (undirected_adjacency_matrix[node][cnt] == 1) and (book[cnt] == 0):
            book[cnt] = 1
            dfs(cnt, undirected_adjacency_matrix, book, vertex_num)
    return

def f_undirected_adjMatrix2Tab(undirected_adjacency_matrix):
    # Convert undirected adjacency matrix to undirected adjacency table
    if undirected_adjacency_matrix.shape[0] != undirected_adjacency_matrix.shape[1]:
        print("Error! SYM: Not a square matrix !")
        return
    else:
        dimension = undirected_adjacency_matrix.shape[0]
        undirected_tab2ret = []
        for rCnt in range(0, dimension):
            for cCnt in range(rCnt, dimension):
                if undirected_adjacency_matrix[rCnt][cCnt] == 1:
                    tmp_tab = [rCnt, cCnt, 0]
                    undirected_tab2ret.append(tmp_tab)
        return undirected_tab2ret

def f_find_all_non_tree(available_branch, combination_num, vertex_num):
    non_tree_mat = []
    non_tree_cnt = 0
    all_combination = list(itertools.combinations(available_branch, combination_num))
    print("Find " + str(len(all_combination)) + " kinds of combinations")  # Debug only
    for item in all_combination:
        tmp_mat = np.array([[INF] * vertex_num] * vertex_num)
        for i in range(0, vertex_num):
            tmp_mat[i][i] = 0
        for idx in item:
            tmp_mat[idx[0]][idx[1]] = 1
            tmp_mat[idx[1]][idx[0]] = 1
        BOOK = [0] * vertex_num
        BOOK[0] = 1
        dfs(0, tmp_mat, BOOK, vertex_num)
        if sum(BOOK) != vertex_num:
            non_tree_mat.append(tmp_mat)
            non_tree_cnt += 1
    print("There are " + str(non_tree_cnt) + " kinds of non-trees")  #Debug only
    return non_tree_mat


def f_find_all_tree(available_branch, combination_num, vertex_num):
    non_tree_mat = []
    non_tree_cnt = 0
    all_combination = list(itertools.combinations(available_branch, combination_num))
    print("Find " + str(len(all_combination)) + " kinds of combinations")  # Debug only
    for item in all_combination:
        tmp_mat = np.array([[INF] * vertex_num] * vertex_num)
        for i in range(0, vertex_num):
            tmp_mat[i][i] = 0
        for idx in item:
            tmp_mat[idx[0]][idx[1]] = 1
            tmp_mat[idx[1]][idx[0]] = 1
        BOOK = [0] * vertex_num
        BOOK[0] = 1
        dfs(0, tmp_mat, BOOK, vertex_num)
        if sum(BOOK) == vertex_num:
            non_tree_mat.append(tmp_mat)
            non_tree_cnt += 1
    print("There are " + str(non_tree_cnt) + " kinds of non-trees")  #Debug only
    return non_tree_mat


def f_Graph_plot_undirected_table(input_undirected_tab):
    position_dict = {0: (0, 4), 1: (0, 2), 2: (0, 0), 3: (4, 4), 4: (4, 2), 5: (4, 0)}
    for items in input_undirected_tab:
        topology.f_Graph_connect2point(position_dict[items[0]], position_dict[items[1]])


def f_Graph_sub_plot_undirected_adjMatrix(input_adjmatrix, sub_row, sub_col):
    total_plot = sub_row * sub_col
    plot_cnt = 1
    fig_handler = plt.figure(1, figsize=(16, 9), dpi=100)
    for each_matrix in input_adjmatrix:
        each_undirected_tab = f_undirected_adjMatrix2Tab(each_matrix)
        plt.subplot(sub_row, sub_col, plot_cnt)
        f_Graph_plot_undirected_table(each_undirected_tab)
        topology.f_Graph_plot_node([(0, 4), (0, 2), (0, 0), (4, 4), (4, 2), (4, 0)])
        plt.title(str(plot_cnt))
        # plt.margins(0.1)
        plt.axis('off')
        plot_cnt = plot_cnt + 1
        if plot_cnt > total_plot:
            break


# non_Tree_Mat = f_find_all_non_tree(avBranch2, combination_num=5, vertex_num=6)
# Tree_Mat = f_find_all_tree(avBranch2, combination_num=5, vertex_num=6)
# print(Tree_Mat)
# f_Graph_sub_plot_undirected_adjMatrix(Tree_Mat, 9, 9)
# plt.show()
# plt.close()
