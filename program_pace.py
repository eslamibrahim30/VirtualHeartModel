import numpy as np

def program_pace(node_ind, s1_n, s1_t, s2_t):
    global pace_panel_para
    global node_table
    
    last_s1 = 0
    last_s2 = 0
    
    # initialize
    if not hasattr(pace_panel_para, 's1'):
        pace_panel_para = {
            's1': s1_t,
            's1n': s1_n,
            'state': 1,
            's2': s2_t,
            's': 1
        }
        node_table[0, 8] = True
    
    if pace_panel_para['s']:
        if pace_panel_para['state'] == 1:  # s1
            if pace_panel_para['s1n'] > 0:
                if pace_panel_para['s1'] > 0:
                    pace_panel_para['s1'] -= 1
                else:
                    pace_panel_para['s1'] = s1_t
                    pace_panel_para['s1n'] -= 1
                    node_table[node_ind, 8] = True
            else:
                pace_panel_para['state'] = 2
                pace_panel_para['s1'] = s1_t
                pace_panel_para['s1n'] = s1_n
                last_s1 = 1
        elif pace_panel_para['state'] == 2:
            if pace_panel_para['s2'] > 0:
                pace_panel_para['s2'] -= 1
            else:
                node_table[node_ind, 8] = True
                last_s2 = 1
                pace_panel_para['s'] = 0
    
    return last_s1, last_s2