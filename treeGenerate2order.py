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


def f_employ_2same_capacitor(undirected_adjacency_table):
    all_combination = list(itertools.combinations(undirected_adjacency_table, 2))
    directed_table2ret = list([])
    for combination_index, combination in enumerate(all_combination):
        tmp_undirected_adjacency_table = cp.deepcopy(undirected_adjacency_table)
        tmp_undirected_adjacency_table.remove(combination[0])
        tmp_undirected_adjacency_table.remove(combination[1])

        tmp_directed_table_short_circuit = []
        for item in tmp_undirected_adjacency_table:
            tmp_directed_table_short_circuit.append(item)
            tmp_directed_table_short_circuit.append([item[1], item[0], item[2]])
        # print(tmp_directed_table_short_circuit)

        # print('combination index: ', combination_index)

        for branch1 in [1, -1]:
            for branch2 in [1, -1]:
                tmp_directed_table_capacitor = list([])
                tmp_directed_table_capacitor.append([combination[0][0], combination[0][1], branch1])
                tmp_directed_table_capacitor.append([combination[0][1], combination[0][0], -branch1])
                tmp_directed_table_capacitor.append([combination[1][0], combination[1][1], branch2])
                tmp_directed_table_capacitor.append([combination[1][1], combination[1][0], -branch2])

                tmp_pack = list([])
                for x in tmp_directed_table_short_circuit:
                    tmp_pack.append(x)
                for y in tmp_directed_table_capacitor:
                    tmp_pack.append(y)
                directed_table2ret.append(np.array(tmp_pack))
                # print(directed_table2ret)

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
        V_AB = f_bellman_ford(directed_adjacency_table, vertex_num=4, branch_num=6, startVertex=0)[1]
        V_ab = f_bellman_ford(directed_adjacency_table, vertex_num=4, branch_num=6, startVertex=2)[3]
        vector2ret = {'V_AB': V_AB, 'V_ab': V_ab, 'DirectedTable': directed_adjacency_table.tolist()}
    elif phase_num == 3:
        V_AB = f_bellman_ford(directed_adjacency_table, vertex_num=6, branch_num=10, startVertex=0)[1]
        V_BC = f_bellman_ford(directed_adjacency_table, vertex_num=6, branch_num=10, startVertex=1)[2]
        V_CA = f_bellman_ford(directed_adjacency_table, vertex_num=6, branch_num=10, startVertex=2)[0]
        V_ab = f_bellman_ford(directed_adjacency_table, vertex_num=6, branch_num=10, startVertex=3)[4]
        V_bc = f_bellman_ford(directed_adjacency_table, vertex_num=6, branch_num=10, startVertex=4)[5]
        V_ca = f_bellman_ford(directed_adjacency_table, vertex_num=6, branch_num=10, startVertex=5)[3]
        vector2ret = OrderedDict([('V_AB', V_AB), ('V_BC', V_BC), ('V_CA', V_CA), ('V_ab', V_ab), ('V_bc', V_bc), ('V_ca', V_ca),
                              ('DirectedTable', directed_adjacency_table.tolist())])
    else:
        print("SYM: Error, wrong phase_num in f_vector_calc !")
        vector2ret = 0

    # print(vector)
    return vector2ret


# main code start here

Tree_Mat = f_find_all_combination_matrix(avBranch2, combination_num=5, vertex_num=6)

# Main loop for finding all structure of 2 cap employment
def f_main_two_cap_employ_findall():
    total_counter = 0
    two_cap_employ_table = list([])
    for tree_index, tree_item in enumerate(Tree_Mat):
        undirected_table_of_a_tree = f_undirected_adjMatrix2Tab(tree_item)
        directed_table_after_cap_employ = f_employ_2same_capacitor(undirected_table_of_a_tree)
        print('Tree No. ' + str(tree_index))
        for each_directed_table in directed_table_after_cap_employ:
            each_vector = f_vector_calc(each_directed_table, phase_num=3)
            each_vector['Tree Num'] = str(tree_index)
            each_vector['TopologyCNT'] = str(total_counter)
            each_vector['Vin'] = str('None')
            each_vector['Vout'] = str('None')
            two_cap_employ_table.append(each_vector)
            total_counter += 1

    print("total counter = " + str(total_counter))
    # print(TWO_CAP_EMPLOY_TABLE)
    print('Length of WHOLE Table ' + str(len(two_cap_employ_table)))
    return two_cap_employ_table


connection_table = f_main_two_cap_employ_findall()

def f_filter_sorted_table(connection_table, side = 'InputSide'):
    # No.1 Find all valid table
    VII = OrderedDict([
        ('V0', [0, 0, 0]),
        ('V1', [2, -1, -1]), ('V2', [1, 1, -2]), ('V3', [-1, 2, -1]),
        ('V4', [-2, 1, 1]), ('V5', [-1, -1, 2]), ('V6', [1, -2, 1])
    ])
    for each_topology in connection_table:
        for vector_key in VII:
            # Vin compare
            if (VII[vector_key][0] == each_topology['V_AB']) \
                    and (VII[vector_key][1] == each_topology['V_BC'])\
                    and (VII[vector_key][2] == each_topology['V_CA']):
                each_topology['Vin'] = vector_key
            # Vout compare
            if (VII[vector_key][0] == each_topology['V_ab']) \
                    and (VII[vector_key][1] == each_topology['V_bc']) \
                    and (VII[vector_key][2] == each_topology['V_ca']):
                each_topology['Vout'] = vector_key

    valid_table = {'V0': [], 'V1': [], 'V2': [], 'V3': [], 'V4': [], 'V5': [], 'V6': []}
    for each_item in connection_table:
        if (each_item['Vin'] != 'None') and (each_item['Vout'] != 'None'):
            if (each_item['Vin'] == 'V0'):
                valid_table['V0'].append(each_item)
            elif (each_item['Vin'] == 'V1'):
                valid_table['V1'].append(each_item)
            elif (each_item['Vin'] == 'V2'):
                valid_table['V2'].append(each_item)
            elif (each_item['Vin'] == 'V3'):
                valid_table['V3'].append(each_item)
            elif (each_item['Vin'] == 'V4'):
                valid_table['V4'].append(each_item)
            elif (each_item['Vin'] == 'V5'):
                valid_table['V5'].append(each_item)
            elif (each_item['Vin'] == 'V6'):
                valid_table['V6'].append(each_item)

    # No.2 Sort the whole table according to the other side.
    sorted_valid_OrderedDict = OrderedDict([('V0', []), ('V1', []), ('V2', []), ('V3', []), ('V4', []), ('V5', []), ('V6', [])])
    for each_key in sorted_valid_OrderedDict:
        sorted_valid_OrderedDict[each_key] = sorted(valid_table[each_key], key=lambda k: k['Vout'])

    return sorted_valid_OrderedDict


tmp_sorted_OrderedDict = f_filter_sorted_table(connection_table)
for key in tmp_sorted_OrderedDict:
    print("Len = " + str(len(tmp_sorted_OrderedDict[key])), end=" ")
    print(tmp_sorted_OrderedDict[key])


which_vector2print = 'V0'
dict_cnt_limit = len(tmp_sorted_OrderedDict[which_vector2print])
subplot_cnt = 1
dict_cnt = 0
figure_cnt = 1


while True:
    if dict_cnt >= dict_cnt_limit:
        plt.show()
        break
    else:
        if subplot_cnt > 12:
            subplot_cnt = 1
            figure_cnt += 1
            plt.show()
            plt.figure(figure_cnt)
        else:
            plt.subplot(4, 3, subplot_cnt)
            topology.f_Graph_plot_graph(tmp_sorted_OrderedDict[which_vector2print][dict_cnt])
            subplot_cnt += 1
            dict_cnt += 1










# plt.show()
