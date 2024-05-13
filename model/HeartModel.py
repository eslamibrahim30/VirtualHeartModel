#!/usr/bin/env python3
import numpy as np
import tkinter as tk


class HeartModel:
    def __init__(self, data):
        self.simData = data
        self.path_ind = [ 'Idle','Ante','Retro','Double','Conflict' ]


    def heart_model_run(node_table, path_table):
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
    
    def heart_react_pace(probe_table, path_table, probe_pos, node_pos, probe_amp):
        """
        Determine how the heart will react to pacing signals.

        Args:
            probe_table: List of lists, each inner list contains 'probe name', 'corresponding path', 'far-field path'.
            path_table: List of lists, each inner list contains path parameters.
            probe_pos: List of lists, each inner list contains the position of a probe.
            node_pos: List of lists, each inner list contains the position of a node.
            probe_amp: List, amplitude of the probes.

        Returns:
            path_table: Updated path table.
        """

        # a persistent variable memorizing the last amplitude to determine rising edge
        last_amp = []

        # initialize
        if not last_amp:
            last_amp = probe_amp.copy()

        # the probes with pacing signals
        pacing_ind = [i for i in range(len(probe_amp)) if probe_amp[i] > last_amp[i]]

        # renew the variable since the rest of the code will not use it
        last_amp = probe_amp.copy()

        # for every probe with pacing signals
        for i in pacing_ind:
            # corresponding path which will be activated by the pacing signal
            cur_path = probe_table[i][1]
            # The position of the probe
            p0 = probe_pos[i]

            # one node connecting to the path
            p1 = node_pos[path_table[cur_path[0]][2]]

            # calculating the distance from one point on path and the perpendicular point of the probe on path
            l = ((p1[0] - p0[0]) ** 2 + (p1[1] - p0[1]) ** 2) ** 0.5
            a = path_table[cur_path[0]][12]
            b = -1
            c = p1[1] - a * p1[0]
            d = abs(a * p0[0] + b * p0[1] + c) / ((a ** 2 + b ** 2) ** 0.5)
            ratio = ((l ** 2 - d ** 2) ** 0.5) / path_table[cur_path[0]][11]

            # calculate the corresponding timer reading
            switch = path_table[cur_path[0]][1]
            if switch == 1:  # Idle
                # go to "double" state
                path_table[cur_path[0]][1] = 5
                # change the current timer of Tante and Tretro according to the pacing position
                path_table[cur_path[0]][7] = round(ratio * path_table[cur_path[0]][8])
                path_table[cur_path[0]][9] = round((1 - ratio) * path_table[cur_path[0]][10]) + 1
            elif switch == 2:  # Ante
                # if the pacing signal exceed the activation wavefront
                if ratio > path_table[cur_path[0]][7] / path_table[cur_path[0]][8]:
                    # keep antegrade conduction and change wavefront to the pacing site since the other direction will conflict
                    path_table[cur_path[0]][7] = round(ratio * path_table[cur_path[0]][8])
                # else the pacing signal will fall into ERP tissue and blocked
            elif switch == 3:  # Retro
                if ratio < path_table[cur_path[0]][9] / path_table[cur_path[0]][10]:
                    path_table[cur_path[0]][9] = round(ratio * path_table[cur_path[0]][10])
            elif switch == 4:  # Conflict
                # pacing signal will fall into ERP tissue
                pass
            elif switch == 5:  # Double
                # the combination of the situation in Ante and Retro
                if ratio > path_table[cur_path[0]][7] / path_table[cur_path[0]][8]:
                    path_table[cur_path[0]][7] = round(ratio * path_table[cur_path[0]][8])
                elif ratio < path_table[cur_path[0]][9] / path_table[cur_path[0]][10]:
                    path_table[cur_path[0]][9] = round(ratio * path_table[cur_path[0]][10])

        return path_table
    
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
    
    def pacing_panel_functional(self, probe_table):
        self.probe_amp = np.zeros(1, probe_table.shape[0])
        