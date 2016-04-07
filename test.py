import numpy as np
# u = [1, 3, 2, 3, 2, 4]
# v = [3, 1, 3, 2, 4, 2]
# w = [-1, 1, 0, 0, 0, 0]
# u = [2, 1, 1, 4, 3]
# v = [3, 2, 5, 5, 4]
# w = [2, -3, 5, 2, 3]
adjacenceTable = [[1, 3, 1], [3, 1, -1], [2, 3, 0], [3, 2, 0], [2, 4, 0], [4, 2, 0]]

def BellmanFord(adjacenTab, vertexN, branchN, disTab, startVertex=1):
    dis[startVertex] = 0
    dis[0] = "head"  # index start from 1, so filled index [0] with some string
    for k in range(0, vertexN - 1):
        for i in range(0, branchN):
            if disTab[adjacenTab[i][1]] > disTab[adjacenTab[i][0]] + adjacenTab[i][2]:
                disTab[adjacenTab[i][1]] = disTab[adjacenTab[i][0]] + adjacenTab[i][2]

vetxNum = 4
bchNum = 6

inf = 9999
dis = [inf] * 5

BellmanFord(adjacenceTable, vetxNum, bchNum, dis, startVertex=3)

print(dis)
