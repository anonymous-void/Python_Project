import numpy as np
# u = [1, 3, 2, 3, 2, 4]
# v = [3, 1, 3, 2, 4, 2]
# w = [-1, 1, 0, 0, 0, 0]
# u = [2, 1, 1, 4, 3]
# v = [3, 2, 5, 5, 4]
# w = [2, -3, 5, 2, 3]
adjacenceTable = [[0, 2, 1], [2, 0, -1], [1, 2, 0], [2, 1, 0], [1, 3, 0], [3, 1, 0]]
dict_Table = []
for item in adjacenceTable:
    tmpDict = {'begin_node': item[0], 'end_node': item[1], 'weight': item[2]}
    dict_Table.append(tmpDict)
print(dict_Table)


def BellmanFord(adjacency_table, vertex_num, branch_num, startVertex=0):
    disTab = [INF] * (vertex_num + 1)
    disTab[startVertex] = 0
    # disTab[0] = "head"  # index start from 1, so filled index [0] with some string
    for k in range(0, vertex_num - 1):
        for i in range(0, branch_num):
            if disTab[adjacency_table[i][1]] > disTab[adjacency_table[i][0]] + adjacency_table[i][2]:
                disTab[adjacency_table[i][1]] = disTab[adjacency_table[i][0]] + adjacency_table[i][2]
    return disTab

vetxNum = 4
bchNum = 6

INF = 9999
# dis = [INF] * 5

# dis = BellmanFord(adjacenceTable, vetxNum, bchNum, startVertex=0)
#
# print(dis)
