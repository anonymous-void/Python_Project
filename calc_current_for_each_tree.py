import itertools
import numpy as np
from sympy import *

iAx, iAy, iAz, iBx, iBy, iBz, iCx, iCy, iCz, iA, iB, iC, ix, iy, iz = \
symbols('iAx, iAy, iAz, iBx, iBy, iBz, iCx, iCy, iCz, iA, iB, iC, ix, iy, iz')

INF = 9999
NODECNT = 0

avBranch = [[0, 2], [0, 3], [1, 2], [1, 3]]
avBranch2 = [[0, 3], [0, 4], [0, 5], [1, 3], [1, 4], [1, 5], [2, 3], [2, 4], [2, 5]]

tree = list([])

class gcl_Topology:
    treeNum = 0
    swMat = 0
    cur_vector = np.array([INF] * 6)

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


def undirected_adjMat2SwMat(ob_undirected_adj_mat):
    sw4ret = np.array([ [INF]*3 ] * 3)
    for row in range(0, 3):
        for col in range(3, 6):
            if ob_undirected_adj_mat[row][col] == 1:
                sw4ret[row][col - 3] = 1
    return sw4ret


def equ_branch_cur_vector_for_a_tree(ob_undirected_sw_mat):
    branch_eq = np.array([[0] * 9] * 6)
    idx = 0
    for row in range(0, 3):
        for col in range(0, 3):
            if ob_undirected_sw_mat[row][col] == 1:
                branch_eq[idx][row * 3 + col] = 1
        idx += 1
    for col in range(0, 3):
        for row in range(0, 3):
            if ob_undirected_sw_mat[row][col] == 1:
                branch_eq[idx][row * 3 + col] = 1
        idx += 1
    return branch_eq


def equ_variable_for_a_tree(ob_undirected_sw_mat):
    var4ret = list([])
    input_dict = {(0, 0): iAx, (0, 1): iAy, (0, 2): iAz, (1, 0): iBx, (1, 1): iBy, (1, 2): iBz,
                  (2, 0): iCx, (2, 1): iCy, (2, 2): iCz}
    for row in range(0, 3):
        for col in range(0, 3):
            if ob_undirected_sw_mat[row][col] == 1:
                var4ret.append(input_dict[(row, col)])
    return  var4ret


def equ_calc_cur_for_a_tree(ob_undirected_adj_mat):
    # Description: Given an undirected adjacence matrix of a tree, a symbolic branch expression will be returned.
    tmp_sw_mat = undirected_adjMat2SwMat(ob_undirected_adj_mat)
    tmp_branch_current_expr = equ_branch_cur_vector_for_a_tree(tmp_sw_mat)
    tmp_variable = equ_variable_for_a_tree(tmp_sw_mat)
    tmp_branch_current_symbol_expr = list([])
    dependent_variable = [iA, iB, iC, ix, iy]
    tmp_eq = list([])
    for idx in range(0, 5):
        tmp_expr = sum( tmp_branch_current_expr[idx] * np.array([iAx, iAy, iAz, iBx, iBy, iBz, iCx, iCy, iCz]) )
        tmp_branch_current_symbol_expr.append(tmp_expr)
    for idx in range(0, 5):
        tmp_eq.append( Eq(dependent_variable[idx], tmp_branch_current_symbol_expr[idx]) )
    symbol_ans4ret = solve(tmp_eq, tmp_variable)
    return symbol_ans4ret


def branch_current_of_a_tree(ob_undirected_adj_mat):
    sym_dict_of_a_tree = equ_calc_cur_for_a_tree(ob_undirected_adj_mat)
    sym_idx_dict = {iAx: 0, iAy: 1, iAz: 2, iBx: 3, iBy: 4, iBz: 5, iCx: 6, iCy: 7, iCz: 8}
    current_dict4ret = np.zeros((9, 6)) # iAx, iAy... iCz as row, iA, iB, ... iz as column
    IABC_XYZ = np.eye(6)
    var = [iA, iB, iC, ix, iy, iz]
    for key in sym_dict_of_a_tree:
        tmp_f = lambdify(var, sym_dict_of_a_tree[key])
        current_dict4ret[sym_idx_dict[key], :] = \
            tmp_f(IABC_XYZ[0, :], IABC_XYZ[1, :], IABC_XYZ[2, :], IABC_XYZ[3, :], IABC_XYZ[4, :], IABC_XYZ[5, :])
    return current_dict4ret


def branch_current_reduce(ob_np_matrix):
    for row in range(0, 9):
        if ob_np_matrix[row][0] == ob_np_matrix[row][1] and ob_np_matrix[row][0] != 0 and ob_np_matrix[row][2] == 0:
            ob_np_matrix[row][2] = -ob_np_matrix[row][0]
            ob_np_matrix[row][0] = 0
            ob_np_matrix[row][1] = 0
        elif ob_np_matrix[row][0] == ob_np_matrix[row][2] and ob_np_matrix[row][2] != 0 and ob_np_matrix[row][1] == 0:
            ob_np_matrix[row][1] = -ob_np_matrix[row][0]
            ob_np_matrix[row][0] = 0
            ob_np_matrix[row][2] = 0
        elif ob_np_matrix[row][1] == ob_np_matrix[row][2] and ob_np_matrix[row][1] != 0 and ob_np_matrix[row][0] == 0:
            ob_np_matrix[row][0] = -ob_np_matrix[row][2]
            ob_np_matrix[row][1] = 0
            ob_np_matrix[row][2] = 0
        elif ob_np_matrix[row][0] == ob_np_matrix[row][1] and ob_np_matrix[row][1] == ob_np_matrix[row][2]:
            ob_np_matrix[row][0] = 0
            ob_np_matrix[row][1] = 0
            ob_np_matrix[row][2] = 0

        if ob_np_matrix[row][3] == ob_np_matrix[row][4] and ob_np_matrix[row][3] != 0 and ob_np_matrix[row][5] == 0:
            ob_np_matrix[row][5] = -ob_np_matrix[row][3]
            ob_np_matrix[row][3] = 0
            ob_np_matrix[row][4] = 0
        elif ob_np_matrix[row][3] == ob_np_matrix[row][5] and ob_np_matrix[row][5] != 0 and ob_np_matrix[row][4] == 0:
            ob_np_matrix[row][4] = -ob_np_matrix[row][3]
            ob_np_matrix[row][3] = 0
            ob_np_matrix[row][5] = 0
        elif ob_np_matrix[row][4] == ob_np_matrix[row][5] and ob_np_matrix[row][4] != 0 and ob_np_matrix[row][3] == 0:
            ob_np_matrix[row][3] = -ob_np_matrix[row][5]
            ob_np_matrix[row][4] = 0
            ob_np_matrix[row][5] = 0
        elif ob_np_matrix[row][3] == ob_np_matrix[row][4] and ob_np_matrix[row][4] == ob_np_matrix[row][5]:
            ob_np_matrix[row][3] = 0
            ob_np_matrix[row][4] = 0
            ob_np_matrix[row][5] = 0


def branch_current_to_C_array(ob_many_trees):
    fp = open('branch_current_C_array.txt', 'w')
    fp.writelines('double current_array[81][9][6] = {')
    fp.writelines('\n')
    for idx, item in enumerate(ob_many_trees):
        tmp_branch_current = branch_current_of_a_tree(item)
        branch_current_reduce(tmp_branch_current)
        fp.writelines('{')
        for row in range(0, 6):
            fp.writelines('    {')
            for col in range(0, 6):
                fp.writelines(str(tmp_branch_current[row][col]))
                if col < 5:
                    fp.writelines(', ')
            if row < 5:
                fp.writelines('},\n')
            elif row == 5:
                fp.writelines('}')
        if idx < 81 - 1:
            fp.writelines(' },\n\n')
        elif idx == 81 - 1:
            fp.writelines(' }\n')
    fp.writelines('};')
    fp.close()


def tree_to_C_array(ob_many_trees):
    fp = open('tree_C_array.txt', 'w')
    fp.writelines('int gi_Tree[81][3][3] = {')
    fp.writelines('\n')
    for idx, item in enumerate(ob_many_trees):
        tmp_tree = undirected_adjMat2SwMat(item)
        fp.writelines('{')
        for row in range(0, 3):
            fp.writelines('    {')
            for col in range(0, 3):
                if tmp_tree[row][col] != 1:
                    fp.writelines('INF')
                else:
                    fp.writelines(str(tmp_tree[row][col]))
                if col < 2:
                    fp.writelines(', ')
            if row < 2:
                fp.writelines('}, \n')
            elif row == 2:
                fp.writelines(' }')
        if idx < 81 - 1:
            fp.writelines(' }, \n\n')
        elif idx == 81 - 1:
            fp.writelines(' }\n')
    fp.writelines('};')
    fp.close()


Tree_Mat = f_find_all_tree(avBranch2, combination_num=5, vertex_num=6)
VIN = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [0, 1, 1], [0, 0, 1], [1, 0, 1],
                   [2, 0, 1], [2, 1, 0], [1, 2, 0], [0, 2, 1], [0, 1, 2], [1, 0, 2],
                   [2, 0, 0], [2, 2, 0], [0, 2, 0], [0, 2, 2], [0, 0, 2], [2, 0, 2] ]
VOUT = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [0, 1, 1], [0, 0, 1], [1, 0, 1],
                   [2, 0, 1], [2, 1, 0], [1, 2, 0], [0, 2, 1], [0, 1, 2], [1, 0, 2],
                   [2, 0, 0], [2, 2, 0], [0, 2, 0], [0, 2, 2], [0, 0, 2], [2, 0, 2] ]

# for i in range(0, len(VIN)): # 用来测试是否会出现：蒙板把所有电容支路挡住的情况
#     for j in range(0, len(VOUT)):
#         availble_mat = np.zeros((3, 3))
#         for row in range(0, 3):
#             for col in range(0, 3):
#                 availble_mat[row][col] = VIN[i][row] - VOUT[j][col]
#
#         for idx, item in enumerate(Tree_Mat):
#             tree_mask = undirected_adjMat2SwMat(item)
#             sw_mat = np.zeros((3, 3))
#             non_zero_sum = 0
#             for row in range(0, 3):
#                 for col in range(0, 3):
#                     if tree_mask[row][col] == INF:
#                         sw_mat[row][col] = INF
#                     else:
#                         sw_mat[row][col] = tree_mask[row][col] * availble_mat[row][col]
#                         if sw_mat[row][col] != 0:
#                             non_zero_sum += 1
#
#             if non_zero_sum == 0:
#                 print("Vin = V%i, Vout = V%i, Tnum = %i\n" % (i, j, idx+1))





s = equ_calc_cur_for_a_tree(Tree_Mat[2])
sm = branch_current_of_a_tree(Tree_Mat[2])

# print(sm)
# branch_current_reduce(sm)
# print(sm)


for key in s:
    print(str(key) + ':\t' + str(s[key]))

# branch_current_to_C_array(Tree_Mat)
# tree_to_C_array(Tree_Mat)
