import itertools
import matplotlib.pyplot as plt
import numpy as np

class Toplogy(object):
    def __init__(self, adjacenceMatrix, adjacenceTable):
        self.adjacenceMatrix = adjacenceMatrix
        self.adjacenceTable = adjacenceTable

    def printAjMatrix(self):
        print(self.adjacenceMatrix)

    def printAjTable(self):
        print(self.adjacenceTable)

adjMat = [[0, 1, 2], [1, 2, 3], [2, 3, 4]]
adjTab = [[1, 2, 0], [2, 3, 0]]
ins = Toplogy(adjMat, adjTab)
ins.printAjMatrix()
ins.printAjTable()

# inf = 9999
# NODECNT = 0
# treeCNT = 0
# avBranch = [[1, 3], [1, 4], [2, 3], [2, 4]]
# treeMat = []
# adjTab = []
#
# def dfs(node, map, nodeTotal):
#     print(str(node) + " ")
#     global NODECNT
#     NODECNT += 1
#     if NODECNT == 6:
#         return
#     for cnt in range(0, nodeTotal):
#         if (map[node][cnt] == 1) and (book[cnt] == 0):
#             book[cnt] = 1
#             dfs(cnt, map, nodeTotal)
#     return
#
# allComb = list(itertools.combinations(avBranch, 3))
# print(allComb)
# print(len(allComb))
#
#
# for item1 in allComb:
#     tmpMat = np.array([[inf] * 4] * 4)
#     for i in range(0, 4):
#         tmpMat[i, i] = 0
#     # print(tmpMat)
#     for idx in item1:
#         tmpMat[idx[0] - 1][idx[1] - 1] = 1
#         tmpMat[idx[1] - 1][idx[0] - 1] = 1
#     # print(tmpMat)
#     book = [0] * 4
#     book[0] = 1
#     dfs(0, tmpMat, 4)
#     if sum(book) == 4:
#         treeMat.append(tmpMat)
#         treeCNT += 1
#
#         for rCnt in range(0, 4):
#             for cCnt in range(0, 4 - rCnt):
#                 if tmpMat[rCnt, cCnt] == 1:
#                     tmpTab1 = [rCnt, cCnt, 0]
#                     tmpTab2 = [cCnt, rCnt, 0]
#                     adjTab.append(tmpTab1)
#                     adjTab.append(tmpTab2)
#
# print(treeMat)
# print(treeCNT)
