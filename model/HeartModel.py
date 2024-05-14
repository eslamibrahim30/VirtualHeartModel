#!/usr/bin/env python3
import numpy as np
import random


class HeartModel:
    def __init__(self, data):
        self.simData = data
        self.path_ind = [ 'Idle','Ante','Retro','Double','Conflict' ]
        self.pacing_ind = None
        self.temp_act = 0


    def heart_model_run(self):
        temp_node = self.simData.node_table.copy()
        temp_path = self.simData.path_table.copy()
        temp_path_node = self.simData.path_table.copy()

        for i in range(len(self.simData.node_table)):
            # Find paths connecting to the node
            result = np.where(np.array(self.simData.path_table)[:, 2:4] == i)
            if not result or len(result) == 0:
                # Handle empty results (e.g., set path_ind and term_ind to empty lists)
                path_ind, term_ind = [], []
                continue  # Optional: Skip to the next iteration if needed
            elif len(result) == 2:
                path_ind, term_ind = tuple(result)
                path_ind = path_ind[path_ind != self.simData.node_table[i][10]]
                term_ind = term_ind[path_ind != self.simData.node_table[i][10]]

            # Update parameters for each node
            temp_node_row, temp_path_node = self.node_automatron(node_table[i], path_ind, term_ind, temp_path_node)
            temp_node.append(temp_node_row)
            temp_act = temp_node_row[8]

        for i in range(len(self.simData.path_table)):
            # Update parameters for each path
            temp_path_row, node_act_1, node_act_2 = self.simData.path_automatron(self.simData.path_table[i], node_table[path_table[i][2]][8], node_table[path_table[i][3]][8])
            temp_path.append(temp_path_row)

            # Update the local node activation signals of the two nodes
            if node_table[self.simData.path_table[i][2]][1] != 2:
                temp_act = temp_act or node_act_1
                if node_act_1 == 1:
                    temp_node[self.simData.path_table[i][2]][10] = i
            else:
                temp_act = False
                node_table[self.simData.path_table[i][2]][2] = node_table[self.simData.path_table[i][2]][3]

            if node_table[self.simData.path_table[i][3]][1] != 2:
                temp_act = temp_act or node_act_2
                if node_act_2 == 1:
                    temp_node[self.simData.path_table[i][3]][10] = i
            else:
                temp_act = False
                node_table[self.simData.path_table[i][3]][2] = node_table[self.simData.path_table[i][3]][3]

        # Update the parameters to global variables
        node_table = [row[:8] + [temp_node[i][8]] + row[9:] for i, row in enumerate(self.simData.node_table)]

        return node_table, temp_path

    
    def node_automatron(self, node_para, path_ind, term_ind, path_table):
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
        self.temp_act = 0

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
    
    def path_automatron(path_para, node_act_1, node_act_2):
        """
        This function updates the status of a single path.

        Inputs:
        path_para: List, parameters for the paths
        
            format: ['path_name', path_state_index, entry_node_index,
            exit_node_index, amplitude_factor, forward_speed,
            backward_speed, forward_timer_current, forward_timer_default,
            backward_timer_current, backward_timer_default, path_length,
            path_slope]
        node_act_1: bool, activation status of the entry node
        node_act_2: bool, activation status of the exit node

        Outputs:
        temp_act_1: bool, local temporary node activation of the entry node
        temp_act_2: bool, local temporary node activation of the exit node
        """
        temp_act_1 = False
        temp_act_2 = False

        if path_para[1] == 1:  # Idle
            # if activation coming from entry node
            if node_act_1:
                # Antegrade conduction
                path_para[1] = 2
            # if activation coming from exit node
            elif node_act_2:
                # Retrograde conduction
                path_para[1] = 3
        elif path_para[1] == 2:  # Antegrade conduction
            # if activation coming from exit node
            if node_act_2:
                # double
                path_para[1] = 5
            else:
                # if timer running out
                if path_para[7] == 0:
                    # reset timer
                    path_para[7] = path_para[8]
                    # activate exit node
                    temp_act_2 = True
                    # go to conflict state
                    path_para[1] = 4
                else:
                    # timer
                    path_para[7] -= 1
        elif path_para[1] == 3:  # Retro
            # if activation coming from entry node
            if node_act_1:
                # conflict
                path_para[1] = 5
            else:
                # if timer runs out
                if path_para[9] == 0:
                    # reset timer
                    path_para[9] = path_para[10]
                    # activate the entry node
                    temp_act_1 = True
                    # change state to conflict
                    path_para[1] = 4
                else:
                    # timer
                    path_para[9] -= 1
        elif path_para[1] == 4:  # Conflict
            # go to Idle state
            path_para[1] = 1
        elif path_para[1] == 5:  # double
            if path_para[9] == 0:
                # reset timer
                path_para[9] = path_para[10]
                # activate the entry node
                temp_act_1 = True
                # change state to conflict
                path_para[1] = 2
                return
            if path_para[7] == 0:
                # reset timer
                path_para[7] = path_para[8]
                # activate exit node
                temp_act_2 = True
                # go to conflict state
                path_para[1] = 3
                return
            if abs(1 - path_para[7] / path_para[8] - path_para[9] / path_para[10]) < 0.9 / min([path_para[8], path_para[10]]):
                path_para[9] = path_para[10]
                path_para[7] = path_para[8]
                path_para[1] = 4
            else:
                path_para[7] -= 1
                path_para[9] -= 1

        return path_para, temp_act_1, temp_act_2
    
        