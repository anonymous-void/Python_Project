import itertools
import numpy as np
import copy as cp

INF = 9999
NODECNT = 0

avBranch = [[0, 2], [0, 3], [1, 2], [1, 3]]
avBranch2 = [[1, 4], [1, 5], [1, 6], [2, 4], [2, 5], [2, 6], [3, 4], [3, 5], [3, 6]]


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


def f_undirected_adjTab2Matrix(undirected_adjacency_table, dimension):
    # Convert undirected adjacency table to undirected adjacency matrix,
    # element 1 is used for representing connected branches
    matrix2ret = np.array([[INF] * dimension] * dimension)
    for i in range(dimension):
        matrix2ret[i][i] = 0

    for item in undirected_adjacency_table:
        matrix2ret[item[0]][item[1]] = 1
        matrix2ret[item[1]][item[0]] = 1

    return matrix2ret


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


def f_find_all_combination_matrix(available_branch, combination_num, vertex_num):
    tree_mat = []
    tree_cnt = 0
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
            tree_mat.append(tmp_mat)
            tree_cnt += 1
    print("There are " + str(tree_cnt) + " kinds of trees")  #Debug only
    return tree_mat


def f_employ_capacitor(undirected_adjacency_table):
    # Given an undirected adjacency table and its dimension,
    # this prog enumerate every possible capcitor employmentation,
    # then, return the directed adjacency table
    directed_table2ret = []

    tree_table = np.array(undirected_adjacency_table * 2)
    for i in range(len(undirected_adjacency_table), 2*len(undirected_adjacency_table)):
        tmp = cp.deepcopy(tree_table[i][0])
        tree_table[i][0] = cp.deepcopy(tree_table[i][1])
        tree_table[i][1] = cp.deepcopy(tmp)

    # tree_table_len = tree_table.shape[0]  # How many rows are there in it
    for i in range(0, len(undirected_adjacency_table)):
        tmp_table1 = cp.deepcopy(tree_table)
        tmp_table2 = cp.deepcopy(tree_table)

        tmp_table1[i][-1] = 1
        tmp_table1[i + len(undirected_adjacency_table)][-1] = -1
        tmp_table2[i][-1] = -1
        tmp_table2[i + len(undirected_adjacency_table)][-1] = 1

        directed_table2ret.append(tmp_table1)
        directed_table2ret.append(tmp_table2)
    return directed_table2ret


def f_bellman_ford(adjacency_table, vertex_num, branch_num, startVertex=0):
    # Bellman-Ford method
    disTab = [INF] * vertex_num
    disTab[startVertex] = 0
    # disTab[0] = "head"  # index start from 1, so filled index [0] with some string
    for k in range(0, vertex_num - 1):
        for i in range(0, branch_num):
            if disTab[adjacency_table[i][1]] > disTab[adjacency_table[i][0]] + adjacency_table[i][2]:
                disTab[adjacency_table[i][1]] = disTab[adjacency_table[i][0]] + adjacency_table[i][2]
    return disTab

def f_vector_calc(directed_adjacency_table, phase_num=2):
    if phase_num == 2:

    elif phase_num == 3:

# main code start here

# Tree_Mat = f_find_all_combination_matrix(avBranch2, combination_num=5, vertex_num=6)
Tree_Mat = f_find_all_combination_matrix(avBranch, combination_num=3, vertex_num=4)
print(Tree_Mat[0])
table = f_undirected_adjMatrix2Tab(Tree_Mat[0])
print(table)
# matrix_restore = f_undirected_adjTab2Matrix(table, 4)
# print(matrix_restore)
directed_table = f_employ_capacitor(table)
print(directed_table)
print(f_bellman_ford(directed_table[0], vertex_num=4, branch_num=6, startVertex=2))
# ------------------------------- Obsolete Code --------------------------------------------------

# allComb = list(itertools.combinations(avBranch, 3))
# print(allComb)
# print(len(allComb))


# treeMat = []
# adjTab = []
#
#
# for item1 in allComb:
#     tmpMat = np.array([[INF] * 4] * 4)
#     for i in range(0, 4):
#         tmpMat[i][i] = 0
#     for idx in item1:
#         tmpMat[idx[0] - 1][idx[1] - 1] = 1
#         tmpMat[idx[1] - 1][idx[0] - 1] = 1
#     book = [0] * 4
#     book[0] = 1
#     dfs(0, tmpMat, 4, book, 4)
#     if sum(book) == 4:
#         treeMat.append(tmpMat)
#
# print(treeMat)

