#!/usr/bin/env python3
"""
This is the main module
"""
from gui import GUI
from data.Data import Data
from model.HeartModel import HeartModel


def main():
    simData = Data()
    simModel = HeartModel(simData)
    app = GUI.GUI("VHM Simulation", "800x800", simModel)
    app.start()

if __name__ == "__main__":
    main()