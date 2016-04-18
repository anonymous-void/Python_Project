import numpy as np
import copy as cp
import itertools
from collections import OrderedDict
import matplotlib.pyplot as plt

def f_Graph_connect2point(point_1, point_2):
    plt.plot([point_1[0], point_2[0]], [point_1[1], point_2[1]], color='cornflowerblue')


def f_Graph_plot_node(node_list):
    for node_item in node_list:
        plt.scatter(node_item[0], node_item[1], s=100, alpha=0.9, color='cornflowerblue')


def f_Graph_plot_label(directed_adjacency_table_dict):
    # No.1 Plot A, B, C, a, b, c annotation
    phase_text = {'A [0]': (-0.8, 3.9), 'B [1]': (-0.8, 1.9), 'C [2]': (-0.8, -0.1),
                  '[3] a': (4.2, 3.9), '[4] b': (4.2, 1.9), '[5] c': (4.2, -0.1)}
    for key in phase_text:
        plt.text(phase_text[key][0], phase_text[key][1], key, size=20)

    # No.2 Plot Vin = V? Vout = V? on the title position
    plt.text(1.8, 4.5, directed_adjacency_table_dict['Vin'] + "–" + directed_adjacency_table_dict['Vout'], size = 15)
    # plt.text(0, 4.5, "Vin = " + directed_adjacency_table_dict['Vin'], size=20)
    # plt.text(2.7, 4.5, "Vout = " + directed_adjacency_table_dict['Vout'], size=20)

    # No.3 Plot Vin and Vout vector on both sides
    # plt.annotate(
    #     r"$ \begin{array}{ccc} a & b & c \\ d & e & f \\ g & h & i \end{array} $",
    #     (0.25, 0.25),
    #     textcoords='axes fraction', size=20)
    plt.text(-0.4, 5, r"$V_{in} = [" + str(directed_adjacency_table_dict['V_AB']) + "\ " \
             + str(directed_adjacency_table_dict['V_BC']) + "\ " \
             + str(directed_adjacency_table_dict['V_CA']) + "]$", size=15)
    plt.text(3, 5, r"$V_{out} = [" + str(directed_adjacency_table_dict['V_ab']) + "\ " \
             + str(directed_adjacency_table_dict['V_bc']) + "\ " \
             + str(directed_adjacency_table_dict['V_ca']) + "]$", size=15)

    # No.4 Plot tree Number
    plt.text(1.6, 5.8, "TopCNT" + " = " + directed_adjacency_table_dict['TopologyCNT'], size=10)


def f_Graph_plot_capacitor(directed_adjacency_table_item,
                           text_size=12, box_line_color=(1., 0.5, 0.5), box_face_color=(1., 0.8, 0.8)):
    start_point = directed_adjacency_table_item[0]
    end_point = directed_adjacency_table_item[1]
    capacitor_direction = directed_adjacency_table_item[2]
    if capacitor_direction > 0:
        capacitor_icon = "+ –"
    elif capacitor_direction < 0:
        capacitor_icon = "– +"
    else:  # if there is no capacitor, do noting.
        return

    which_capacitor2plot = (start_point, end_point)
    if which_capacitor2plot == (0, 3):
        plt.text(1, 4, capacitor_icon, size=text_size, rotation=0.0,
                 bbox=dict(boxstyle="square", ec=box_line_color, fc=box_face_color))
    elif which_capacitor2plot == (0, 4):
        plt.text(1, 3.5, capacitor_icon, size=text_size, rotation=-20,
                 bbox=dict(boxstyle="square", ec=box_line_color, fc=box_face_color))
    elif which_capacitor2plot == (0, 5):
        plt.text(1, 3, capacitor_icon, size=text_size, rotation=-38,
                 bbox=dict(boxstyle="square", ec=box_line_color, fc=box_face_color))
    elif which_capacitor2plot == (1, 3):
        plt.text(2, 3, capacitor_icon, size=text_size, rotation=20,
                 bbox=dict(boxstyle="square", ec=box_line_color, fc=box_face_color))
    elif which_capacitor2plot == (1, 4):
        plt.text(2, 2, capacitor_icon, size=text_size, rotation=0.0,
                 bbox=dict(boxstyle="square", ec=box_line_color, fc=box_face_color))
    elif which_capacitor2plot == (1, 5):
        plt.text(2, 1, capacitor_icon, size=text_size, rotation=-20,
                 bbox=dict(boxstyle="square", ec=box_line_color, fc=box_face_color))
    elif which_capacitor2plot == (2, 3):
        plt.text(3, 3, capacitor_icon, size=text_size, rotation=40,
                 bbox=dict(boxstyle="square", ec=box_line_color, fc=box_face_color))
    elif which_capacitor2plot == (2, 4):
        plt.text(3, 1.5, capacitor_icon, size=text_size, rotation=20,
                 bbox=dict(boxstyle="square", ec=box_line_color, fc=box_face_color))
    elif which_capacitor2plot == (2, 5):
        plt.text(3, 0, capacitor_icon, size=text_size, rotation=0.0,
                 bbox=dict(boxstyle="square", ec=box_line_color, fc=box_face_color))
    else:
        raise Exception('SYM: Error! The Capcitor' + str(which_capacitor2plot) + ' do not exist !')

    # capacitor_plot_dict = {(0, 3): branch_03, (0, 4): branch_04, (0, 4): branch_05,
    #                        (1, 3): branch_13, (1, 4): branch_14, (1, 5): branch_15,
    #                        (2, 3): branch_23, (2, 4): branch_24, (2, 5): branch_25}
    #
    # eval(capacitor_direction[(start_point, end_point)])


def f_Graph_plot_graph(directed_adjacency_table_dict):
    directed_adjacency_table = directed_adjacency_table_dict["DirectedTable"]
    position_dict = {0: (0, 4), 1: (0, 2), 2: (0, 0), 3: (4, 4), 4: (4, 2), 5: (4, 0)}
    shrink_directed_adj_table = directed_adjacency_table[::2]
    capacitor_directed_adj_table = [item for item in shrink_directed_adj_table if item[2] != 0]

    # No.1 Plot all six points
    f_Graph_plot_node([position_dict[key] for key in position_dict])
    # No.2 Plot all connected branches
    for branch_item in shrink_directed_adj_table:
        f_Graph_connect2point(position_dict[branch_item[0]], position_dict[branch_item[1]])
    # No.3 Plot all capacitor branches
    for cap_item in capacitor_directed_adj_table:
        f_Graph_plot_capacitor(cap_item)
    # No.4 Plot all labels
    f_Graph_plot_label(directed_adjacency_table_dict)

    # No.5 Miscolleneous
    plt.margins(0.2)
    plt.axis('off')


def f_Graph_plot_inPage(sorted_OrderedDict, which_vector='V0'):
    total_graph_count = len(sorted_OrderedDict[which_vector])
    if total_graph_count % 2 == 0:
        row_count = total_graph_count // 2
    else:
        row_count = total_graph_count // 2 + 1

    col_count = 2
    for total_count in range(0, total_graph_count):
        plt.subplot(row_count, col_count, total_graph_count + 1)
        f_Graph_plot_graph(sorted_OrderedDict[which_vector][total_count])