'''
Time: 2016/04/05 20:56 UTC 12:57
    This prog is used for spanning all the trees of graph of matrix converter.
    As for matrix converter, there would be 81 kinds of branch connections.
    This prog first generates all the connections(including trees and non-trees),
    after that, using deep-first search to testify which is tree or not.
    The connection will be given in the formation of Adjacency Matrix
'''
import itertools
import matplotlib.pyplot as plt
import numpy as np



def dfs(node, map, nodeTotal):
    print(str(node) + " ")
    global NODECNT
    NODECNT += 1
    if NODECNT == 6:
        return
    for cnt in xrange(0, nodeTotal):
        if (map[node][cnt] == 1) and (book[cnt] == 0):
            book[cnt] = 1
            dfs(cnt, map, nodeTotal)
    return

avBranch = [[1, 1], [1, 2], [1, 3], [2, 1], [2, 2], [2, 3], [3, 1], [3, 2], [3, 3]]
avBranch2 = [[1, 4], [1, 5], [1, 6], [2, 4], [2, 5], [2, 6], [3, 4], [3, 5], [3, 6]]

inf = 9999
treeCnt = 0
allComb = list(itertools.combinations(avBranch2, 5)) # Pick 5 branches out of 9 branches

for item1 in allComb:
    tmpMat = np.array([[inf] * 6] * 6)
    for i in range(0, 6):
        tmpMat[i, i] = 0
    print(tmpMat)
    for idx in item1:
        tmpMat[idx[0] - 1][idx[1] - 1] = 1
        tmpMat[idx[1] - 1][idx[0] - 1] = 1
    print(tmpMat)
    NODECNT = 0
    book = [0] * 6
    book[0] = 1
    dfs(0, tmpMat, 6)
    print(book)
    if sum(book) == 6:
        treeCnt += 1

print("tree Num = " + str(treeCnt))
















# a = np.arange(36).reshape(6, 6)
# print a
# a[1][2] = 9999
# print a
# print a
# fig = plt.figure()
# # ax = fig.add_subplot(1, 1, 1)
# # ax.set_aspect('equal')
# plt.imshow(a, interpolation='nearest', cmap='ocean')
# plt.colorbar()
# plt.show()
