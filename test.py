import treeGenerate2order
import itertools
phase_vector = [1, 1, 0, 0, 1, 1]
gl_short_branch = [[0, 4], [0, 5], [1, 4], [1, 5], [2, 3]]
gl_cap_branch = [[0, 3], [1, 3], [2, 4], [2, 5]]

vector_dict = {'V_AB': 0, 'V_BC': 1, 'V_CA': -1, 'V_ab': -1, 'V_bc': 0, 'V_ca': 1}

gl_short_branch_combi = list(itertools.combinations(gl_short_branch, 3))
gl_cap_branch_combi = list(itertools.combinations(gl_cap_branch, 2))

tmp_connection_table = treeGenerate2order.f_main_two_cap_employ_findall()

ans_list = list([])
for each_topology in tmp_connection_table:
    flag = 0
    for each_key in vector_dict:
        if each_topology[each_key] != vector_dict[each_key]:
            flag = 1
            break
    if flag == 0:
        ans_list.append(each_topology)

for each_item in ans_list:
    print(each_item)