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


non_Tree_Mat = f_find_all_non_tree(avBranch2, combination_num=5, vertex_num=6)
for item in non_Tree_Mat:
    print(item)
    print('-'*100)

# print(non_Tree_Mat[0])