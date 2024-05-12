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