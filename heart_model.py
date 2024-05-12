import numpy as np

def heart_model(node_table, path_table):
    """
    The function updates the parameters for nodes and paths in one time stamp.

    Inputs:
    node_table: List of lists, each inner list contains parameters for one node.
        Format: ['node name', node_state_index, TERP_current, TERP_default, TRRP_current, TRRP_default, Trest_current, Trest_default, node_activation, [Terp_min, Terp_max], index_of_path_activate_the_node]
    path_table: List of lists, each inner list contains parameters for one path.
        Format: ['path_name', path_state_index, entry_node_index, exit_node_index, amplitude_factor, forward_speed, backward_speed, forward_timer_current, forward_timer_default, backward_timer_current, backward_timer_default, path_length, path_slope]
    """
    temp_node = []
    temp_path = []
    temp_path_node = path_table.copy()

    for i in range(len(node_table)):
        # Find paths connecting to the node
        path_ind, term_ind = np.where(np.array(path_table)[:, 2:4] == i)
        path_ind = path_ind[path_ind != node_table[i][10]]
        term_ind = term_ind[path_ind != node_table[i][10]]
        node_table[i][10] = 0

        # Update parameters for each node
        temp_node_row, temp_path_node = node_automatron(node_table[i], path_ind, term_ind, temp_path_node)
        temp_node.append(temp_node_row)
        temp_act = temp_node_row[8]

    for i in range(len(path_table)):
        # Update parameters for each path
        temp_path_row, node_act_1, node_act_2 = path_automatron(path_table[i], node_table[path_table[i][2]][8], node_table[path_table[i][3]][8])
        temp_path.append(temp_path_row)

        # Update the local node activation signals of the two nodes
        if node_table[path_table[i][2]][1] != 2:
            temp_act = temp_act or node_act_1
            if node_act_1 == 1:
                temp_node[path_table[i][2]][10] = i
        else:
            temp_act = False
            node_table[path_table[i][2]][2] = node_table[path_table[i][2]][3]

        if node_table[path_table[i][3]][1] != 2:
            temp_act = temp_act or node_act_2
            if node_act_2 == 1:
                temp_node[path_table[i][3]][10] = i
        else:
            temp_act = False
            node_table[path_table[i][3]][2] = node_table[path_table[i][3]][3]

    # Update the parameters to global variables
    node_table = [row[:8] + [temp_node[i][8]] + row[9:] for i, row in enumerate(node_table)]

    return node_table, temp_path