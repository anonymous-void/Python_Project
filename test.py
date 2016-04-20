# -*- coding: utf-8 -*-
import numpy as np
import copy as cp
import itertools
from collections import OrderedDict
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


test_undirected_adjacency_table = [[0, 3, 0], [0, 4, 0], [0, 5, 0], [1, 3, 0], [2, 3, 0]]


test_directed_table = np.array([[0, 3, 0], [3, 0, 0], [1, 4, 0], [4, 1, 0], [2, 5, 0], [5, 2, 0],
             [1, 3, -1], [3, 1, 1], [2, 4, -1], [4, 2, 1]])
# tmp_bellman = list([])
# for i in range(0, 6):
#     tmp_bellman.append(f_bellman_ford(tmp_table, vertex_num=6, branch_num=10, startVertex=i))
# print(tmp_bellman)
# ret_vector = f_vector_calc(tmp_table)
# print(ret_vector)

test_directed_table_dict = OrderedDict([('V_AB', -2), ('V_BC', 1), ('V_CA', 1), ('V_ab', -1), ('V_bc', 2), ('V_ca', -1),
             ('DirectedTable', [[0, 5, 0], [5, 0, 0], [1, 4, 0], [4, 1, 0], [2, 3, 0], [3, 2, 0], [2, 4, -1], [4, 2, 1], [2, 5, 1], [5, 2, -1]]), \
             ('Tree Num', '79'), ('TopologyCNT', '3198'), ('Vin', 'V4'), ('Vout', 'V3')])


"""
This is a demo of creating a pdf file with several pages,
as well as adding metadata and annotations to pdf files.
"""

x = np.arange(0, 5, 0.1)
y = [x, x**2]

with PdfPages('multipage_pdf.pdf') as pdf:
    for i in range(0, 2):
        plt.figure(i+1)
        plt.plot(x, y[i])
        pdf.savefig()
        plt.close()
