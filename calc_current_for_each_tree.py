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


Tree_Mat = f_find_all_tree(avBranch2, combination_num=5, vertex_num=6)
# print(Tree_Mat[0])
# for idx, item in enumerate(Tree_Mat):
#     tmpObj = gcl_Topology()
#     tmpObj.swMat = undirected_adjMat2SwMat(item)
#     tmpObj.treeNum = idx + 1
#     tree.append(tmpObj)
    # print(undirected_adjMat2SwMat(item))
    # print('-' * 50)
# cur_vector = equ_branch_cur_vector_for_a_tree(undirected_adjMat2SwMat(Tree_Mat[0]))
# expr_iA = sum( cur_vector[0] * np.array([iAx, iAy, iAz, iBx, iBy, iBz, iCx, iCy, iCz]) )
s = equ_calc_cur_for_a_tree(Tree_Mat[0])
sm = branch_current_of_a_tree(Tree_Mat[0])

print(sm)




# var = [iAx, iAy, iAz, iBx, iCx]
# s = solve([eq1, eq2, eq3, eq4, eq5], var)

for key in s:
    print(str(key) + ':\t' + str(s[key]))

