import random

def node_automatron(node_para, path_ind, term_ind, path_table):
    """
    The function updates the status of a single node by considering the current status of the node.

    Inputs:
    node_para: List, parameters for the nodes
        format: ['node name', node_state_index, TERP_current, TERP_default, TRRP_current, TRRP_default, Trest_current, Trest_default, activation, [Terp_min, Terp_max], index_of_path_activate_the_node]
    path_ind: List, paths connecting to the node except the one activated the node
    term_ind: List, which terminal the node connecting to the paths (1 or 2)

    Outputs:
    The same as inputs, just updated values.
    """
    temp_act = 0

    if node_para[8]:  # if node is activated
        temp = node_para[9]
        match node_para[1]:
            case 1:  # Rest
                # set ERP to longest
                node_para[3] = temp[1]
                node_para[2] = node_para[3] + round((random.random() - 0.5) * 0 * node_para[3])

                # reset path conduction speed
                for i in range(len(path_ind)):
                    # if at terminal 1, only affect antegrade conduction; 2 for retrograde conduction
                    if term_ind[i] == 1:
                        path_table[path_ind[i]][8] = round((1 + (random.random() - 0.5) * 0) * path_table[path_ind[i]][11] / path_table[path_ind[i]][5])
                    else:
                        path_table[path_ind[i]][10] = round((1 + (random.random() - 0.5) * 0) * path_table[path_ind[i]][11] / path_table[path_ind[i]][6])

                # Reset Trest
                node_para[6] = round(node_para[7] * (1 + (random.random() - 0.5) * 0))
                # change state to ERP
                node_para[1] = 2
            case 2:  # ERP
                # set ERP to the lowest
                node_para[3] = temp[0]

                # set conduction speed to the slowest
                for i in range(len(path_ind)):
                    if term_ind[i] == 1:
                        path_table[path_ind[i]][8] = round((1 + (random.random() - 0.5) * 0) * path_table[path_ind[i]][11] / path_table[path_ind[i]][5] * (node_para[11] + 1))
                    else:
                        path_table[path_ind[i]][10] = round((1 + (random.random() - 0.5) * 0) * path_table[path_ind[i]][11] / path_table[path_ind[i]][6] * 3)

    return node_para, path_table

