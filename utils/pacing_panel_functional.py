def pacing_panel_functional(Config, probe_table):
    global pace_panel_para
    probe_amp = [0] * len(probe_table)

    if Config.pace_panel.is_active() and Config.pace_deliver.get():
        if pace_panel_para.state == 1:  # s1
            if pace_panel_para.s1n > 0:
                if pace_panel_para.s1 > 0:
                    pace_panel_para.s1 -= 1
                else:
                    pace_panel_para.s1 = int(Config.s1.get())
                    pace_panel_para.s1n -= 1
                    pace_panel_para.pace_state = 1
            else:
                pace_panel_para.state = 2
                pace_panel_para.s1 = int(Config.s1.get())
                pace_panel_para.s1n = int(Config.s1n.get())
        elif pace_panel_para.state == 2:
            if pace_panel_para.s2n > 0:
                if pace_panel_para.s2 > 0:
                    pace_panel_para.s2 -= 1
                else:
                    pace_panel_para.s2 = int(Config.s2.get())
                    pace_panel_para.s2n -= 1
                    pace_panel_para.pace_state = 1
            else:
                Config.pace_deliver.set(0)
                pace_panel_para.s1 = int(Config.s2.get())
                pace_panel_para.s1n = int(Config.s2n.get())

        if pace_panel_para.pace_state:
            if pace_panel_para.pulse_w > 0:
                pace_panel_para.pulse_w -= 1
                probe_amp[Config.pace_probe.get()] = int(Config.pulse_a.get())
            else:
                pace_panel_para.pace_state = 0
                pace_panel_para.pulse_w = int(Config.pulse_w.get())

    return probe_amp
