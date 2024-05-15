#!/usr/bin/env python3
import numpy as np
import random


class HeartModel:
    def __init__(self, data):
        self.simData = data


    def heart_model_run(self, node_table, path_table):
        temp_path_node = path_table.copy()
        temp_node = [0] * len(node_table)
        temp_path = [0] * len(path_table)
        temp_act_list = [0] * len(path_table)
        node_act_1 = 0
        node_act_2 = 0

        for i in range(len(node_table)):
            indices = []
            cur_act_path = node_table[i][10]
            for j in range(len(path_table)):
                if path_table[j][3] == i:
                    indices.append([j, [path_table[j][3], path_table[j][4]]])
            without_act_paths =[]
            for j in range(len(indices)):
                if cur_act_path != indices[j][0]:
                    without_act_paths.append(indices[j])
            path_ind = []
            term_ind = []
            for k in indices:
                path_ind.append(k[0])
                term_ind.append(k[1])
            node_table[i][10] = 0
            temp_node[i], temp_path_node = self.node_automatron(node_table[i], path_ind, term_ind, temp_path_node)
            temp_act_list[i] = temp_node[i][8]
            
        
        for i in range(len(path_table)):
            path_data = path_table[i]
            source_node_index = path_table[i][2]
            target_node_index = path_table[i][3]
            if source_node_index >= len(node_table):
                continue
            node_act_1 = node_table[source_node_index][8]
            if target_node_index >= len(node_table):
                continue
            node_act_2 = node_table[target_node_index][8]
            result = self.path_automatron(path_data, node_act_1, node_act_2)
            temp_path[i], self.node_act_1, self.node_act_2 = result
            if node_table[path_table[i][2]][1] != 2:
                temp_act_list[path_table[i][2]] = temp_act_list[path_table[i][2]] or node_act_1
                # -------------------------------------
                # store the path that activated the node
                if node_act_1 == 1:
                    temp_node[path_table[i][2]][10] = i
                # -------------------------------------
            else:
                temp_act_list[path_table[i][2]] = False
                node_table[path_table[i][2]][2] = node_table[path_table[i][2]][3]

            if node_table[path_table[i][3]][1] != 2:
                temp_act_list[path_table[i][3]] = temp_act_list[path_table[i][3]] or node_act_2
                # -------------------------------------
                # store the path that activated the node
                if node_act_2 == 1:
                    temp_node[path_table[i][3]][10] = i
                # -------------------------------------
            else:
                temp_act_list[path_table[i][3]] = False
                node_table[path_table[i][3]][2] = node_table[path_table[i][3]][3]
        node_table.clear()
        for i in range(len(temp_node)):
            node_row = temp_node[i][:8] + [temp_act_list[i]] + temp_node[i][9:]
            node_table.append(node_row)
        ind = []
        for i in range(len(temp_path_node)):
            if isinstance(temp_path_node[i], list) and isinstance(temp_path[i], list):
                if temp_path_node[i][8] != temp_path[i][8]:
                    ind.append(i)
        for i in ind:
            # update the value
            temp_path[i][10] = temp_path_node[i][10]
            
            # if the path is still in idle state, also update the current value
            if temp_path_node[i][1] == 1:
                temp_path[i][9] = temp_path[i][10]
        ind = []
        for i in range(len(temp_path_node)):
            if isinstance(temp_path_node[i], list) and isinstance(temp_path[i], list):
                if temp_path_node[i][10] != temp_path[i][10]:
                    ind.append(i)
        for i in ind:
            # update the value
            temp_path[i][10] = temp_path_node[i][10]
            
            # if the path is still in idle state, also update the current value
            if temp_path_node[i][1] == 1:
                temp_path[i][9] = temp_path[i][10]
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
        temp_act = 0

        if node_para[8]:  # if node is activated
            temp = node_para[9]
            if node_para[1] == 1:  # Rest
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
            elif node_para[1] == 2:  # ERP
                # set ERP to the lowest
                node_para[3] = temp[0]
                # set conduction speed to the slowest
                for i in range(len(path_ind)):
                    if term_ind[i] == 1:
                        path_table[path_ind[i]][8] = round((1 + (random.random() - 0.5) * 0) * path_table[path_ind[i]][11] / path_table[path_ind[i]][5] * (node_para[11] + 1))
                    else:
                        path_table[path_ind[i]][10] = round((1 + (random.random() - 0.5) * 0) * path_table[path_ind[i]][11] / path_table[path_ind[i]][6] * 3)
                # reset TERP
                node_para[2] = round((1 + (random.random() - 0.5) * 0) * node_para[3])
            elif node_para[1] == 3:  # RRP
                # calculate the ratio of early activation
                ratio = node_para[4] / node_para[5]
                
                # calculate the ERP timer for the next round
                if node_para[10] == 1:
                    node_para[3] = temp[1] + round((1 + (random.random() - 0.5) * 0) * (1 - (1 - ratio) ** 3) * (temp[0] - temp[1]))
                else:
                    node_para[3] = temp[0] + round((1 + (random.random() - 0.5) * 0) * (1 - ratio ** 3) * (temp[1] - temp[0]))
                node_para[2] = 2  # change state to ERP
                node_para[3] = round((1 + (random.random() - 0.5) * 0) * node_para[4])  # reset ERP

                for i in range(len(path_ind)):
                    if node_para[10] == 1:
                        if term_ind[i] == 1:
                            path_table[path_ind[i]][8] = round((1 + (random.random() - 0.5) * 0) * path_table[path_ind[i]][11] / path_table[path_ind[i]][5] * (1 + ratio * 3))
                        else:
                            path_table[path_ind[i]][10] = round((1 + (random.random() - 0.5) * 0) * path_table[path_ind[i]][11] / path_table[path_ind[i]][6] * (1 + ratio * 3))
                    else:
                        if term_ind[i] == 1:
                            path_table[path_ind[i]][8] = round((1 + (random.random() - 0.5) * 0) * path_table[path_ind[i]][11] / path_table[path_ind[i]][5] * (1 + ratio ** 2 * 3))
                        else:
                            path_table[path_ind[i]][10] = round((1 + (random.random() - 0.5) * 0) * path_table[path_ind[i]][11] / path_table[path_ind[i]][6] * (1 + ratio ** 2 * 3))

                # reset TRRP
                node_para[4] = round((1 + (random.random() - 0.5) * 0) * node_para[5])
                node_para[1] = 2
            if not node_para[0]:  # if node is not activated
                if node_para[1] == 1:  # Rest
                    if node_para[6] == 0:  # self depolarize
                        # change state to ERP
                        node_para[1] = 2
                        # reset Trest timer
                        node_para[6] = round((1 + (random.random() - 0.5) * 0) * node_para[7])
                        # activate the node
                        temp_act = 1
                    else:
                        # timer
                        node_para[6] -= 1
                elif node_para[1] == 2:  # ERP
                    if node_para[2] == 0:  # timer running out
                        # change state to RRP
                        node_para[1] = 3
                        # reset TERP timer
                        node_para[2] = round((1 + (random.random() - 0.5) * 0) * node_para[3])
                    else:
                        # timer
                        node_para[2] -= 1
                elif node_para[1] == 3:  # RRP
                    if node_para[4] == 0:  # timer running out
                        # change state to rest
                        node_para[1] = 1
                        # reset TRRP timer
                        node_para[4] = round((1 + (random.random() - 0.5) * 0) * node_para[5])
                    else:
                        # timer
                        node_para[4] -= 1

            #--------------------------------------
            temp = node_para[:8] + [temp_act] + node_para[9:]
        return node_para, path_table
    
    def path_automatron(self, path_para, node_act_1, node_act_2):
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

        