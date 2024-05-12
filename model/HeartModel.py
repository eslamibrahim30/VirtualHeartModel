#!/usr/bin/env python3
import numpy as np


class HeartModel:
    def __init__(self, data):
        self.simData = data

    def heart_model(node_table, path_table):
        """
        This function updates the parameters for nodes and paths in one time stamp.

        Args:
            node_table: List of lists, each inner list contains parameters for one node.
            path_table: List of lists, each inner list contains parameters for one path.

        Returns:
            node_table: Updated list containing node parameters.
            path_table: Updated list containing path parameters.
        """

        # Local temporary node & path tables
        temp_node = []
        temp_path = []

        # Temporary path table for node automata updates
        temp_path_node = path_table.copy()

        for i in range(len(node_table)):
            # Find paths connected to the node
            path_ind = [idx for idx, row in enumerate(path_table) if row[2] == i or row[3] == i]
            term_ind = [0, 1] * int(len(path_ind) / 2)

            # Exclude the activating path
            if node_table[i][11] in path_ind:
                path_ind = [p for p in path_ind if p != node_table[i][11]]
                term_ind = [t for t in term_ind if t != node_table[i][11]]
            node_table[i][11] = 0  # Reset activation path index

            # Update node parameters
            node, temp_path_node = node_automatron(node_table[i], path_ind, term_ind, temp_path_node)
            temp_node.append(node)

        for i in range(len(path_table)):
            # Update path parameters
            path, node_act_1, node_act_2 = path_automatron(path_table[i], node_table[path_table[i][2]][9], node_table[path_table[i][3]][9])
            temp_path.append(path)

            # Update node activation signals (OR operation)
            if node_table[path_table[i][2]][2] != 2:
                node_table[path_table[i][2]][9] = node_table[path_table[i][2]][9] or node_act_1
                if node_act_1:
                    node_table[path_table[i][2]][11] = i
            else:
                node_table[path_table[i][2]][3] = node_table[path_table[i][2]][4]

            if node_table[path_table[i][3]][2] != 2:
                node_table[path_table[i][3]][9] = node_table[path_table[i][3]][9] or node_act_2
                if node_act_2:
                    node_table[path_table[i][3]][11] = i
            else:
                node_table[path_table[i][3]][3] = node_table[path_table[i][3]][4]

        # Update node table with temporary data
        node_table = [node[:8] + [node[9]] + node[10:] for node in temp_node]

        # Update path table with changes in default conduction states
        for i in range(len(temp_path_node)):
            if temp_path_node[i][9] != temp_path[i][9]:
                temp_path[i][9] = temp_path_node[i][9]
                if temp_path_node[i][2] == 1:
                    temp_path[i][8] = temp_path[i][9]
            if temp_path_node[i][11] != temp_path[i][11]:
                temp_path[i][11] = temp_path_node[i][11]
                if temp_path_node[i][2] == 1:
                    temp_path[i][10] = temp_path[i][11]

        # Update path table
        path_table = temp_path

        return node_table, path_table
    
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
    
    def pacing_panel_functional(self, probe_table):
        self.probe_amp = np.zeros(1, probe_table.shape[0])

        if 'pace_panel' in Config and Config['pace_deliver']['Value']:
            if pace_panel_para['state'] == 1:  # s1
                if pace_panel_para['s1n'] > 0:
                    if pace_panel_para['s1'] > 0:
                        pace_panel_para['s1'] -= 1
                    else:
                        pace_panel_para['s1'] = int(Config['s1']['String'])
                        pace_panel_para['s1n'] -= 1
                        pace_panel_para['pace_state'] = 1
                else:
                    pace_panel_para['state'] = 2
                    pace_panel_para['s1'] = int(Config['s1']['String'])
                    pace_panel_para['s1n'] = int(Config['s1n']['String'])

            elif pace_panel_para['state'] == 2:
                if pace_panel_para['s2n'] > 0:
                    if pace_panel_para['s2'] > 0:
                        pace_panel_para['s2'] -= 1
                    else:
                        pace_panel_para['s2'] = int(Config['s2']['String'])
                        pace_panel_para['s2n'] -= 1
                        pace_panel_para['pace_state'] = 1
                else:
                    Config['pace_deliver']['Value'] = 0
                    pace_panel_para['s1'] = int(Config['s2']['String'])
                    pace_panel_para['s1n'] = int(Config['s2n']['String'])

            if pace_panel_para['pace_state']:
                if pace_panel_para['pulse_w'] > 0:
                    pace_panel_para['pulse_w'] -= 1
                    probe_amp[Config['pace_probe']['Value']] = int(Config['pulse_a']['String'])
                else:
                    pace_panel_para['pace_state'] = 0
                    pace_panel_para['pulse_w'] = int(Config['pulse_w']['String'])

        return probe_amp
