#!/usr/bin/env python3
"""
This module conatains Data class for storing simulation data.
"""
import scipy.io

class Data:
    def __init__(self):
        self.node_table = []
        self.path_table = []
        self.prope_table = []
        self.pace_para = []
        self.node_pos = []
        self.prope_pos = []
        self.egm_table = []
        self.pace_panel_para = []


    def load_model(self, filename):
        self.mat = scipy.io.loadmat(filename)
        self.node_table = self.convertMatToList(self.mat['node_table'])
        self.path_table = self.convertMatToList(self.mat['path_table'])
        self.prope_table = self.convertMatToList(self.mat['probe_table'])
        self.pace_para = self.convertMatToList(self.mat['pace_para'])
        self.node_pos = self.convertMatToList(self.mat['node_pos'])
        self.prope_pos = self.convertMatToList(self.mat['probe_pos'])
        self.egm_table = self.convertMatToList(self.mat['egm_table'])
        self.pace_panel_para = self.convertMatToList(self.mat['pace_panel_para'][0])
    
    def convertMatToList(self, mat_data):
        list_data = []
        for d in mat_data:
            row = []
            for i in range(len(d)):
                row.append(d[i].flatten()[0])
            list_data.append(row)
        return list_data
