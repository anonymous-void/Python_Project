import treeGenerate2order
from collections import OrderedDict

def find_cap_should_employ(which_sector_IN, which_sector_OUT, which_side_have_max_d0, numOrstr='str'):
# which_side_have_max_d0 = din or dout
# numOrstr='str' or 'num' config in which format return the capacitor
#   'str' for string return, eg. ('A', 'c')
#   'num' for number retrun, eg. (0, 5) stands for ('A', 'c'), 0~2 stands for A, B, C, 3~5 stands for a, b, c
    cap2ret = 'None'
    d0_larger_dict = OrderedDict([(1, 'A'), (2, 'A'), (3, 'C'), (4, 'C'), (5, 'B'), (6, 'B'),
                                   (7, 'A'), (8, 'A'), (9, 'C'), (10, 'C'), (11, 'B'), (12, 'B')])
    y_shape = OrderedDict([(1, 'B'), (2, 'C'), (3, 'C'), (4, 'C'), (5, 'C'),
                                      (6, 'A'), (7, 'A'), (8, 'A'), (9, 'A'),
                                      (10, 'B'), (11, 'B'), (12, 'B')])
    benz_shape = OrderedDict([(1, 'A'), (2, 'A'), (3, 'A'),
                                     (4, 'B'), (5, 'B'), (6, 'B'), (7, 'B'),
                                     (8, 'C'), (9, 'C'), (10, 'C'), (11, 'C'),
                                     (12, 'A')])
    y_shape_list = [1, 2, 5, 6, 9, 10]
    benz_shape_list = [3, 4, 7, 8, 11, 12]
    if which_side_have_max_d0 == 'din':
        if which_sector_OUT in y_shape_list:
            cap2ret = (str.upper(y_shape[which_sector_IN]), str.lower(d0_larger_dict[which_sector_OUT]))
        elif which_sector_OUT in benz_shape_list:
            cap2ret = (str.upper(benz_shape[which_sector_IN]), str.lower(d0_larger_dict[which_sector_OUT]))
        else:
            raise Exception('SYM: Error, your Input sector code does not belong to neither Y-shape nor Benz-shape')
    elif which_side_have_max_d0 == 'dout':
        if which_sector_IN in y_shape_list:
            cap2ret = (str.upper(d0_larger_dict[which_sector_IN]), str.lower(y_shape[which_sector_OUT]))
        elif which_sector_IN in benz_shape_list:
            cap2ret = (str.upper(d0_larger_dict[which_sector_IN]), str.lower(benz_shape[which_sector_OUT]))
        else:
            raise Exception('SYM: Error, your Input sector code does not belong to neither Y-shape nor Benz-shape')
    else:
        raise Exception('SYM: Error, you did not config __which_side_have_max_d0__')

    if numOrstr == 'str':
        return cap2ret
    elif numOrstr == 'num':
        codec_dict = {'A': 0, 'B': 1, 'C': 2, 'a': 3, 'b': 4, 'c': 5}
        cap2ret = (codec_dict[cap2ret[0]], codec_dict[cap2ret[1]])
        return cap2ret


def find_cap_coinsistence(which_sector_IN, which_sector_OUT, input_vector_category='VI', output_vector_category='VII'):
    VI_dict = {1: 'VI_1',
                   2: 'VI_2', 3: 'VI_2',
                   4: 'VI_3', 5: 'VI_3',
                   6: 'VI_4', 7: 'VI_4',
                   8: 'VI_5', 9: 'VI_5',
                   10: 'VI_6', 11: 'VI_6',
                   12: 'VI_1'}
    VII_dict = {1: 'VII_1',
                   2: 'VII_2', 3: 'VII_2',
                   4: 'VII_3', 5: 'VII_3',
                   6: 'VII_4', 7: 'VII_4',
                   8: 'VII_5', 9: 'VII_5',
                   10: 'VII_6', 11: 'VII_6',
                   12: 'VII_1'}
    VIII_dict = {1: 'VIII_1',
                2: 'VIII_2', 3: 'VIII_2',
                4: 'VIII_3', 5: 'VIII_3',
                6: 'VIII_4', 7: 'VIII_4',
                8: 'VIII_5', 9: 'VIII_5',
                10: 'VIII_6', 11: 'VIII_6',
                12: 'VIII_1'}
    input_side
    return (medium_dict[which_sector_IN], medium_dict[which_sector_OUT])

# txt = open('test.txt', 'w')
# for input_side in ['V1', 'V2', 'V3', 'V4', 'V5', 'V6']:
#     for output_side in ['V1', 'V2', 'V3', 'V4', 'V5', 'V6']:
#         tmp_Topology_set = [item for item in treeGenerate2order.tmp_sorted_OrderedDict[input_side] if item['Vout'] == output_side]
#         for each_top in tmp_Topology_set:
#             print(each_top)
#             txt.write(str(each_top))
#             txt.write('\n')
#         print("-"*100)
#         txt.writelines("-"*100 + "\n")
# txt.close()


def find_if_consistent_cap_exist(sorted_ordered_dict, input_vector_category='VI', output_vector_category='VI'):
    for input_side in range(1, 13):
        for output_side in range(1, 13):
            cap_inputside = find_cap_coinsistence(input_side, output_side)[0]
            cap_outputside = find_cap_coinsistence(input_side, output_side)[1]
            cap_should_employ = find_cap_should_employ(input_side, output_side, 'din', 'num')
            tmp_Topology_set = [item for item in sorted_ordered_dict[cap_inputside] if item['Vout'] == cap_outputside]  # 当输入侧矢量确定后，找出给定的输出侧矢量的拓扑

            capacitor_should_exist_flag = 0
            for each_topology in tmp_Topology_set:
                tmp_capacitor_branch_set = [branch for branch in each_topology['DirectedTable'] if branch[2] != 0]
                for each_cap_branch in tmp_capacitor_branch_set:
                    if (each_cap_branch[0] == cap_should_employ[0]) and (each_cap_branch[1] == cap_should_employ[1]) and \
                            (each_cap_branch[2] != 0):  # each_cap_branch[2] != 0 means there exist a capacitor
                        print("Found for %s - %s" % (cap_inputside, cap_outputside))
                        capacitor_should_exist_flag = 1
                        continue

            if capacitor_should_exist_flag == 0:
                print("No match branch of Capacitor %s - %s for %s - %s" % (cap_should_employ[0], cap_should_employ[1],
                                                                            cap_inputside, cap_outputside))



find_if_consistent_cap_exist(treeGenerate2order.tmp_sorted_OrderedDict)
# find_if_consistent_cap_exist(test_topology_set)

