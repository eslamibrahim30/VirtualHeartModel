#!/usr/bin/env python3
"""
This is the main module
"""
from gui import QTGUI, TKGUI
from data.Data import Data
from model.HeartModel import HeartModel
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


def main():
    simData = Data()
    simModel = HeartModel(simData)
    tkapp = TKGUI.TKGUI("VHM Simulation", "800x800", simModel)
    tkapp.start()
    simModel.heart_model_run(simData.node_table, simData.path_table)
    qtapp = QApplication(sys.argv)
    ex = QTGUI.QTGUI()
    ex.show()
    sys.exit(qtapp.exec_())


if __name__ == "__main__":
    main()