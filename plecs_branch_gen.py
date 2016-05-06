import numpy as np
from collections import OrderedDict

VI = np.array([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [0, 1, 1], [0, 0, 1], [1, 0, 1]])
VII = np.array([[0, 0, 0], [1, -1, 0], [1, 0, -1], [0, 1, -1], [-1, 1, 0], [-1, 0, 1], [0, -1, 1]])
VIII = np.array([[0, 0, 0], [1, -1, -1], [1, 1, -1], [-1, 1, -1], [-1, 1, 1], [-1, -1, 1], [1, -1, 1]])

INF = np.inf

def gf_adj_matrix_gen(input_vect, output_vect):
    tmp_array = np.array([[INF, INF, INF], [INF, INF, INF], [INF, INF, INF]])
    tmp_cap2list = list([])
    tmp_cap1list = list([])
    tmp_dict = {"cap2": [], "cap1": []}
    for row in range(0, 3):
        for col in range(0, 3):
            tmp_array[row][col] = input_vect[row] - output_vect[col]
            if np.abs(tmp_array[row][col]) == 2:
                tmp_cap2list.append((row, col))
            elif np.abs(tmp_array[row][col]) == 1:
                tmp_cap1list.append((row, col))
    tmp_dict["cap2"] = tmp_cap2list
    tmp_dict["cap1"] = tmp_cap1list
    for cap2idx, cap2item in  enumerate(tmp_cap2list):
        
    return tmp_dict


tmp_get = gf_adj_matrix_gen(VII[1], VIII[6])
print(tmp_get)

