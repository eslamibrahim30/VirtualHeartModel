#!/usr/bin/env python3
"""
This module conatains GUI class for creating GUI object.
"""
import tkinter as tk
from tkinter.ttk import Treeview
from PIL import Image, ImageTk


class GUI:
    def __init__(self, title="My Application", geometry="300x200", heartModel=None):
        """
        Initializes the GUI window with a title and geometry.
        """
        self.heartModel = heartModel
        self.img_path = "/home/eslam/G4/second_term/control/project/myPythonCode/EP.png"
        self.root = tk.Tk()
        self.updateFigureChecked = tk.IntVar(value=0)
        self.updateTableChecked = tk.IntVar(value=0)
        self.pacemakerOnChecked = tk.IntVar(value=0)
        self.displayImageChecked = tk.IntVar(value=0)
        self.showUnipolarChecked = tk.IntVar(value=0)
        self.formalModeChecked = tk.IntVar(value=0)

        self.SA_CT_a_value = tk.IntVar(value=0)
        self.CA_value = tk.IntVar(value=0)

        self.root.title(title)
        self.root.geometry(geometry)

        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)
        for i in range(20):
            self.root.grid_rowconfigure(i, weight=1)
        self.image = ImageTk.PhotoImage(Image.open(self.img_path))
        self.img_label = tk.Label(image=self.image)
        self.img_label.grid(row=0, column=0, rowspan=10, columnspan=2, padx=10, sticky='w')

        self.buttonRun = tk.Button(self.root, text="Run", background='white')
        self.buttonRun.grid(row=1, column=2, sticky='nesw')
    
        self.buttonNodeTable = tk.Button(self.root, text="Node table", background='white', command=self.open_node_table)
        self.buttonNodeTable.grid(row=2, column=2, sticky='nesw')
        self.buttonPathTable = tk.Button(self.root, text="Path table", background='white', command=self.open_path_table)
        self.buttonPathTable.grid(row=3, column=2, sticky='nesw')
        self.buttonPaceParaTable = tk.Button(self.root, text="Pace Para table", background='white', command=self.open_pace_para_table)
        self.buttonPaceParaTable.grid(row=4, column=2, sticky='nesw')

        self.buttonPacePanel = tk.Button(self.root, text="Pace panel", background='white', command=self.open_pace_panel)
        self.buttonPacePanel.grid(row=5, column=2, sticky='nesw')
        self.buttonSaveModel = tk.Button(self.root, text="Save model", background='white')
        self.buttonSaveModel.grid(row=6, column=2, sticky='nesw')
        self.buttonLoadModel = tk.Button(self.root, text="Load model", background='white', command=self.heartModel.simData.load_model)
        self.buttonLoadModel.grid(row=7, column=2, sticky='nesw')
        self.buttonShowEGM = tk.Button(self.root, text="Show EGM", background='white', command=self.openEGM)
        self.buttonShowEGM.grid(row=8, column=2, sticky='nesw')
        self.buttonSaveEGM = tk.Button(self.root, text="Save EGM", background='white')
        self.buttonSaveEGM.grid(row=9, column=2, sticky='nesw')

        self.buttonAddNode = tk.Button(self.root, text="Add node", background='white', command=self.open_add_node)
        self.buttonAddNode.grid(row=10, column=2,sticky='nesw')
        self.buttonAddPath = tk.Button(self.root, text="Add path", background='white', command=self.open_add_path)
        self.buttonAddPath.grid(row=11, column=2, sticky='nesw')
        self.buttonAddPrope = tk.Button(self.root, text="Add prope", background='white', command=self.open_add_prope)
        self.buttonAddPrope.grid(row=12, column=2, sticky='nesw')
        
        self.updateFigure = tk.Checkbutton(self.root, text='Update figure', variable=self.updateFigureChecked, onvalue=1, offvalue=0)
        self.updateFigure.grid(row=10, column=0, sticky='nesw')
        self.updateTable = tk.Checkbutton(self.root, text='Update table', variable=self.updateTableChecked, onvalue=1, offvalue=0)
        self.updateTable.grid(row=11, column=0, sticky='nesw')
        self.displayImage = tk.Checkbutton(self.root, text='Pacemaker on', variable=self.pacemakerOnChecked, onvalue=1, offvalue=0)
        self.displayImage.grid(row=12, column=0, sticky='nesw')
        self.displayImage = tk.Checkbutton(self.root, text='Display image', variable=self.displayImageChecked, onvalue=1, offvalue=0)
        self.displayImage.grid(row=10, column=1, sticky='nesw')
        self.showUnipolar = tk.Checkbutton(self.root, text='Show unipolar', variable=self.showUnipolarChecked, onvalue=1, offvalue=0)
        self.showUnipolar.grid(row=11, column=1, sticky='nesw')
        self.formalMode = tk.Checkbutton(self.root, text='Formal mode', variable=self.formalModeChecked, onvalue=1, offvalue=0)
        self.formalMode.grid(row=12, column=1, sticky='nesw')

    def start(self):
        """
        Starts the main loop of the GUI, displaying the window.
        """
        self.root.mainloop()

    def open_node_table(self):
        self.nodeTableWindow = tk.Toplevel(self.root)
        headings = ("Name", "State", "Trep_c", "Trep_d", "Trrp_c", "Trrp_d", "Trest_c", "Trest_d", "Act")
        tree = Treeview(self.nodeTableWindow, column=headings, show='headings', height=8)
        for i in range(len(headings)):
            tree.column(f"# {i + 1}", anchor=tk.CENTER)
            tree.heading(f"# {i + 1}", text=headings[i])

        # Insert the data in Treeview widget
        for d in self.heartModel.simData.node_table:
            tree.insert('', 'end', text="1", values=d)

        tree.pack()
    
    def open_pace_para_table(self):
        self.paceParaTableWindow = tk.Toplevel(self.root)
        headings = ("Name", "State", "Timer_cur", "Timer_def", "Act")
        tree = Treeview(self.paceParaTableWindow, column=headings, show='headings', height=3)
        for i in range(len(headings)):
            tree.column(f"# {i + 1}", anchor=tk.CENTER)
            tree.heading(f"# {i + 1}", text=headings[i])


        # Insert the data in Treeview widget
        for d in self.heartModel.simData.pace_para:
            tree.insert('', 'end', text="1", values=d)

        tree.pack()
    
    def open_path_table(self):
        self.pathTableWindow = tk.Toplevel(self.root)
        headings = ("Name", "State", "En", "Ex", "Amp", "An_s", "Re_s", "An_c", "An_d", "Re_c", "Re_d")
        tree = Treeview(self.pathTableWindow, column=("Name", "State", "En", "Ex", "Amp", "An_s", "Re_s", "An_c", "An_d", "Re_c", "Re_d"), show='headings', height=8)
        for i in range(len(headings)):
            tree.column(f"# {i + 1}", anchor=tk.CENTER)
            tree.heading(f"# {i + 1}", text=headings[i])

        # Insert the data in Treeview widget
        for d in self.heartModel.simData.path_table:
            tree.insert('', 'end', text="1", values=d)

        tree.pack()
    
    def open_pace_panel(self):
        self.pacePanelWindow = tk.Toplevel(self.root)
        for i in range(8):
            self.pacePanelWindow.grid_columnconfigure(i, weight=1)
        for i in range(10):
            self.pacePanelWindow.grid_rowconfigure(i, weight=1)
        tk.Label(self.pacePanelWindow, text='S1 period').grid(row=0, column=1)
        self.s1Period = tk.Entry(self.pacePanelWindow).grid(row=1, column=1)
        tk.Label(self.pacePanelWindow, text='S2 period').grid(row=0, column=3)
        self.s2Period = tk.Entry(self.pacePanelWindow).grid(row=1, column=3)
        tk.Label(self.pacePanelWindow, text='Pulse width').grid(row=0, column=5)
        self.pulseWidth = tk.Entry(self.pacePanelWindow).grid(row=1, column=5)
        tk.Label(self.pacePanelWindow, text='Amplitude').grid(row=0, column=7)
        self.amplitude = tk.Entry(self.pacePanelWindow).grid(row=1, column=7)
        tk.Label(self.pacePanelWindow, text='S1 period').grid(row=3, column=1)
        self.s1Number = tk.Entry(self.pacePanelWindow).grid(row=4, column=1)
        tk.Label(self.pacePanelWindow, text='S1 number').grid(row=3, column=3)
        self.s2Number = tk.Entry(self.pacePanelWindow).grid(row=4, column=3)
        tk.Label(self.pacePanelWindow, text='pace probe').grid(row=3, column=5)
        self.pacePrope = tk.Entry(self.pacePanelWindow).grid(row=4, column=5)
        # deliver should be a toggle button
        self.deliverPace = tk.Button(self.pacePanelWindow, text="Deliver", background='white')
        self.deliverPace.grid(row=4, column=7, sticky='nesw')

    
    def open_add_node(self):
        self.addNodeWindow = tk.Toplevel(self.root)
        for i in range(8):
            self.addNodeWindow.grid_columnconfigure(i, weight=1)
        for i in range(10):
            self.addNodeWindow.grid_rowconfigure(i, weight=1)
        tk.Label(self.addNodeWindow, text='S1 period').grid(row=0, column=1)
        self.s1Period = tk.Entry(self.addNodeWindow).grid(row=1, column=1)
        tk.Label(self.addNodeWindow, text='S2 period').grid(row=0, column=3)
        self.s2Period = tk.Entry(self.addNodeWindow).grid(row=1, column=3)
        tk.Label(self.addNodeWindow, text='Pulse width').grid(row=0, column=5)
        self.pulseWidth = tk.Entry(self.addNodeWindow).grid(row=1, column=5)
        tk.Label(self.addNodeWindow, text='Amplitude').grid(row=0, column=7)
        self.amplitude = tk.Entry(self.addNodeWindow).grid(row=1, column=7)
        tk.Label(self.addNodeWindow, text='S1 period').grid(row=3, column=1)
        self.s1Number = tk.Entry(self.addNodeWindow).grid(row=4, column=1)
        tk.Label(self.addNodeWindow, text='S1 number').grid(row=3, column=3)
        self.s2Number = tk.Entry(self.addNodeWindow).grid(row=4, column=3)
        tk.Label(self.addNodeWindow, text='pace probe').grid(row=3, column=5)
        self.pacePrope = tk.Entry(self.addNodeWindow).grid(row=4, column=5)
        self.deliverPace = tk.Button(self.addNodeWindow, text="Deliver", background='white')
        self.deliverPace.grid(row=4, column=7, sticky='nesw')
    
    def open_add_path(self):
        self.addPathWindow = tk.Toplevel(self.root)
        for i in range(8):
            self.addPathWindow.grid_columnconfigure(i, weight=1)
        for i in range(10):
            self.addPathWindow.grid_rowconfigure(i, weight=1)
        tk.Label(self.addPathWindow, text='S1 period').grid(row=0, column=1)
        self.s1Period = tk.Entry(self.addPathWindow).grid(row=1, column=1)
        tk.Label(self.addPathWindow, text='S2 period').grid(row=0, column=3)
        self.s2Period = tk.Entry(self.addPathWindow).grid(row=1, column=3)
        tk.Label(self.addPathWindow, text='Pulse width').grid(row=0, column=5)
        self.pulseWidth = tk.Entry(self.addPathWindow).grid(row=1, column=5)
        tk.Label(self.addPathWindow, text='Amplitude').grid(row=0, column=7)
        self.amplitude = tk.Entry(self.addPathWindow).grid(row=1, column=7)
        tk.Label(self.addPathWindow, text='S1 period').grid(row=3, column=1)
        self.s1Number = tk.Entry(self.addPathWindow).grid(row=4, column=1)
        tk.Label(self.addPathWindow, text='S1 number').grid(row=3, column=3)
        self.s2Number = tk.Entry(self.addPathWindow).grid(row=4, column=3)
        tk.Label(self.addPathWindow, text='pace probe').grid(row=3, column=5)
        self.pacePrope = tk.Entry(self.addPathWindow).grid(row=4, column=5)
        self.deliverPace = tk.Button(self.addPathWindow, text="Deliver", background='white')
        self.deliverPace.grid(row=4, column=7, sticky='nesw')
    
    def open_add_prope(self):
        self.addPropeWindow = tk.Toplevel(self.root)
        for i in range(8):
            self.addPropeWindow.grid_columnconfigure(i, weight=1)
        for i in range(15):
            self.addPropeWindow.grid_rowconfigure(i, weight=1)
        
        self.SA_CT_a = tk.Checkbutton(self.addPropeWindow, text='SA_CT_a', variable=self.SA_CT_a_value, onvalue=1, offvalue=0)
        self.SA_CT_a.grid(row=2, column=2)
        self.CA = tk.Checkbutton(self.addPropeWindow, text='CA', variable=self.CA_value, onvalue=1, offvalue=0)
        self.CA.grid(row=2, column=4)
        self.propeName = tk.Entry(self.addPropeWindow).grid(row=0, column=0)
        self.addPrope = tk.Button(self.addPropeWindow, text="Add", background='white')
        self.addPrope.grid(row=14, column=3, sticky='nesw')
        self.cancelPrope = tk.Button(self.addPropeWindow, text="Cancel", background='white')
        self.cancelPrope.grid(row=14, column=7, sticky='nesw')

    def openEGM(self):
        return None