import numpy as np
from scipy.stats import norm

def functional_sensing(node_pos, path_table, probe_pos, probe_table, probe_amp):
    local_theta = 15
    far_theta = 80
    egm_data = np.zeros(1, len(probe_table))

    # local signal
    for i in range(len(probe_table)):
        temp = probe_table[i][1]
        act_probe = probe_pos[i]

        act_local = [x for x in temp if path_table[x][1] != 1]

        for j in range(len(act_local)):
            p1 = node_pos[path_table[act_local[j]][2]]
            p2 = node_pos[path_table[act_local[j]][3]]

            switch_val = path_table[act_local[j]][1]
            if switch_val == 2:  # Ante
                cur_timer = path_table[act_local[j]][7]
                def_timer = path_table[act_local[j]][8]
                wave_front = [p1[0] + (p2[0] - p1[0]) * (def_timer - cur_timer) / def_timer,
                              p2[1] + (p1[1] - p2[1]) * cur_timer / def_timer]
            elif switch_val == 3:  # Retro
                cur_timer = path_table[act_local[j]][9]
                def_timer = path_table[act_local[j]][10]
                wave_front = [p1[0] + (p2[0] - p1[0]) * cur_timer / def_timer,
                              p2[1] + (p1[1] - p2[1]) * (def_timer - cur_timer) / def_timer]
            elif switch_val == 5:  # double
                cur_timer = path_table[act_local[j]][7]
                def_timer = path_table[act_local[j]][8]
                wave_front = [[p1[0] + (p2[0] - p1[0]) * (def_timer - cur_timer) / def_timer,
                               p2[1] + (p1[1] - p2[1]) * cur_timer / def_timer],
                              [p1[0] + (p2[0] - p1[0]) * cur_timer / def_timer,
                               p2[1] + (p1[1] - p2[1]) * (def_timer - cur_timer) / def_timer]]
            else:
                wave_front = [np.inf, np.inf]

            for k in range(len(wave_front)):
                cur_dist = np.sqrt((act_probe[1] - wave_front[k][1]) ** 2 + (act_probe[0] - wave_front[k][0]) ** 2)
                ratio = norm.pdf(cur_dist, 0, local_theta)
                egm_data[i] += ratio * path_table[act_local[j]][4]

    # pacing artifact
    pacing_probe_ind = np.nonzero(probe_amp)[0]

    for k in range(len(pacing_probe_ind)):
        cur_dist = np.sqrt((act_probe[1] - probe_pos[pacing_probe_ind[k]][1]) ** 2 + (act_probe[0] - probe_pos[pacing_probe_ind[k]][0]) ** 2)
        ratio = 0.7 * norm.pdf(cur_dist, 0, far_theta)
        egm_data[i] += ratio * probe_amp[pacing_probe_ind[k]]

    return egm_data