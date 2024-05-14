#!/usr/bin/env python3
"""
This module conatains GUI class for creating GUI object.
"""
import tkinter as tk
from tkinter.ttk import Treeview
from PIL import Image, ImageTk
from tkinter import filedialog


class GUI:
    def __init__(self, title="My Application", geometry="300x200", heartModel=None):
        """
        Initializes the GUI window with a title and geometry.
        """
        self.heartModel = heartModel
        self.img_path = "EP.png"
        self.root = tk.Tk()

        self.heartModel.simData.formalModeChecked = tk.IntVar(value=0)
        self.heartModel.simData.updateFigureChecked = tk.IntVar(value=0)
        self.heartModel.simData.updateTableChecked = tk.IntVar(value=0)
        self.heartModel.simData.pacemakerOnChecked = tk.IntVar(value=0)
        self.heartModel.simData.displayImageChecked = tk.IntVar(value=0)
        self.heartModel.simData.showUnipolarChecked = tk.IntVar(value=0)
        self.heartModel.simData.formalModeChecked = tk.IntVar(value=0)

        self.heartModel.simData.curS1period = tk.IntVar(value=500)
        self.heartModel.simData.curS2period = tk.IntVar(value=250)
        self.heartModel.simData.curS1number = tk.IntVar(value=3)
        self.heartModel.simData.curS2number = tk.IntVar(value=1)
        self.heartModel.simData.curPulseWidth = tk.IntVar(value=4)
        self.heartModel.simData.curAmplitude = tk.IntVar(value=20)
        self.heartModel.simData.curPacePrope = tk.StringVar(value='HRA1')

        self.newPropeName = tk.StringVar(value='')

        self.root.title(title)
        self.root.geometry(geometry)

        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)
        for i in range(20):
            self.root.grid_rowconfigure(i, weight=1)
        self.image = Image.open(self.img_path)
        self.resizedImage = self.image.resize((530,530), Image.LANCZOS)
        self.imageHeart = ImageTk.PhotoImage(self.resizedImage)
        self.canvas = tk.Canvas(self.root, width=530, height=530, background='white')
        self.canvas.create_image(265, 265, image = self.imageHeart)
        self.canvas.grid(row=0,column=0, rowspan=10, columnspan=2, padx=10)

        self.buttonRun = tk.Button(self.root, text="Run", background='white', command=self.heartModel.heart_model_run)
        self.buttonRun.grid(row=1, column=2, sticky='nesw')
    
        self.buttonNodeTable = tk.Button(self.root, text="Node table", background='white', command=self.open_node_table)
        self.buttonNodeTable.grid(row=2, column=2, sticky='nesw')
        self.buttonPathTable = tk.Button(self.root, text="Path table", background='white', command=self.open_path_table)
        self.buttonPathTable.grid(row=3, column=2, sticky='nesw')
        self.buttonPaceParaTable = tk.Button(self.root, text="Pace Para table", background='white', command=self.open_pace_para_table)
        self.buttonPaceParaTable.grid(row=4, column=2, sticky='nesw')

        self.buttonPacePanel = tk.Button(self.root, text="Pace panel", background='white', command=self.open_pace_panel)
        self.buttonPacePanel.grid(row=5, column=2, sticky='nesw')
        self.buttonSaveModel = tk.Button(self.root, text="Save model", background='white', command=self.save_model)
        self.buttonSaveModel.grid(row=6, column=2, sticky='nesw')
        self.buttonLoadModel = tk.Button(self.root, text="Load model", background='white', command=self.load_model)
        self.buttonLoadModel.grid(row=7, column=2, sticky='nesw')
        self.buttonShowEGM = tk.Button(self.root, text="Show EGM", background='white', command=self.openEGM)
        self.buttonShowEGM.grid(row=8, column=2, sticky='nesw')
        self.buttonSaveEGM = tk.Button(self.root, text="Save EGM", background='white', command=self.saveEGM)
        self.buttonSaveEGM.grid(row=9, column=2, sticky='nesw')

        self.buttonAddNode = tk.Button(self.root, text="Add node", background='white', command=self.open_add_node)
        self.buttonAddNode.grid(row=10, column=2,sticky='nesw')
        self.buttonAddPath = tk.Button(self.root, text="Add path", background='white', command=self.open_add_path)
        self.buttonAddPath.grid(row=11, column=2, sticky='nesw')
        self.buttonAddPrope = tk.Button(self.root, text="Add prope", background='white', command=self.open_add_prope)
        self.buttonAddPrope.grid(row=12, column=2, sticky='nesw')
        
        self.updateFigure = tk.Checkbutton(self.root, text='Update figure', variable=self.heartModel.simData.updateFigureChecked, onvalue=1, offvalue=0)
        self.updateFigure.grid(row=10, column=0, sticky='nesw')
        self.updateTable = tk.Checkbutton(self.root, text='Update table', variable=self.heartModel.simData.updateTableChecked, onvalue=1, offvalue=0)
        self.updateTable.grid(row=11, column=0, sticky='nesw')
        self.displayImage = tk.Checkbutton(self.root, text='Pacemaker on', variable=self.heartModel.simData.pacemakerOnChecked, onvalue=1, offvalue=0)
        self.displayImage.grid(row=12, column=0, sticky='nesw')
        self.displayImage = tk.Checkbutton(self.root, text='Display image', variable=self.heartModel.simData.displayImageChecked, onvalue=1, offvalue=0)
        self.displayImage.grid(row=10, column=1, sticky='nesw')
        self.showUnipolar = tk.Checkbutton(self.root, text='Show unipolar', variable=self.heartModel.simData.showUnipolarChecked, onvalue=1, offvalue=0)
        self.showUnipolar.grid(row=11, column=1, sticky='nesw')
        self.formalMode = tk.Checkbutton(self.root, text='Formal mode', variable=self.heartModel.simData.formalModeChecked, onvalue=1, offvalue=0)
        self.formalMode.grid(row=12, column=1, sticky='nesw')

    def start(self):
        """
        Starts the main loop of the GUI, displaying the window.
        """
        self.root.mainloop()

    def open_node_table(self):
        # TODO Make table editable
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
        # TODO Make table editable
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
        # TODO Make table editable
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
        self.s1Period = tk.Entry(self.pacePanelWindow, textvariable=self.heartModel.simData.curS1period).grid(row=1, column=1)
        tk.Label(self.pacePanelWindow, text='S2 period').grid(row=0, column=3)
        self.s2Period = tk.Entry(self.pacePanelWindow, textvariable=self.heartModel.simData.curS2period).grid(row=1, column=3)
        tk.Label(self.pacePanelWindow, text='Pulse width').grid(row=0, column=5)
        self.pulseWidth = tk.Entry(self.pacePanelWindow, textvariable=self.heartModel.simData.curPulseWidth).grid(row=1, column=5)
        tk.Label(self.pacePanelWindow, text='Amplitude').grid(row=0, column=7)
        self.amplitude = tk.Entry(self.pacePanelWindow, textvariable=self.heartModel.simData.curAmplitude).grid(row=1, column=7)
        tk.Label(self.pacePanelWindow, text='S1 number').grid(row=3, column=1)
        self.s1Number = tk.Entry(self.pacePanelWindow, textvariable=self.heartModel.simData.curS1number).grid(row=4, column=1)
        tk.Label(self.pacePanelWindow, text='S2 number').grid(row=3, column=3)
        self.s2Number = tk.Entry(self.pacePanelWindow, textvariable=self.heartModel.simData.curS2number).grid(row=4, column=3)
        tk.Label(self.pacePanelWindow, text='pace probe').grid(row=3, column=5)
        self.pacePrope = tk.Entry(self.pacePanelWindow, textvariable=self.heartModel.simData.curPacePrope).grid(row=4, column=5)
        self.deliverPace = tk.Button(self.pacePanelWindow, text="Deliver", background='white')
        self.deliverPace.grid(row=4, column=7, sticky='nesw')


    def save_model(self):
        # TODO
        return None


    def load_model(self):
        file_path = filedialog.askopenfilename(filetypes=[("Mat files", "*.mat")])
        self.heartModel.simData.load_model(file_path)
        for i in self.heartModel.simData.node_pos:
            self.canvas.create_oval(i[0] - 5, i[1] - 5, i[0] + 5, i[1] + 5, fill='red')
        for i in self.heartModel.simData.prope_pos:
            self.canvas.create_oval(i[0] - 5, i[1] - 5, i[0] + 5, i[1] + 5, fill='cyan')

    
    def open_add_node(self):
        self.addNodeWindow = tk.Toplevel(self.root)
        for i in range(2):
            self.addNodeWindow.grid_columnconfigure(i, weight=1)
        for i in range(15):
            self.addNodeWindow.grid_rowconfigure(i, weight=1)
        tk.Label(self.addNodeWindow, text='Node Name').grid(row=0, columnspan=2)
        self.newNodeName = tk.Entry(self.addNodeWindow).grid(row=1, columnspan=2, padx=5)
        tk.Label(self.addNodeWindow, text='State').grid(row=2, columnspan=2)
        self.newNodeState = tk.Listbox(self.addNodeWindow, height=3, selectmode=tk.BROWSE)
        self.newNodeState.insert(1, 'Rest')
        self.newNodeState.insert(2, 'REP')
        self.newNodeState.insert(3, 'RRP')
        self.newNodeState.grid(row=3, columnspan=2)
        tk.Label(self.addNodeWindow, text='REP_c').grid(row=4, column=0)
        self.newNodeERP1 = tk.Entry(self.addNodeWindow).grid(row=5, column=0, padx=5)
        tk.Label(self.addNodeWindow, text='REP_d').grid(row=4, column=1)
        self.newNodeERP2 = tk.Entry(self.addNodeWindow).grid(row=5, column=1, padx=5)
        tk.Label(self.addNodeWindow, text='RRP_c').grid(row=6, column=0)
        self.newNodeRRP1 = tk.Entry(self.addNodeWindow).grid(row=7, column=0, padx=5)
        tk.Label(self.addNodeWindow, text='RRP_c').grid(row=6, column=1)
        self.newNodeRRP1 = tk.Entry(self.addNodeWindow).grid(row=7, column=1, padx=5)
        tk.Label(self.addNodeWindow, text='Rest_c').grid(row=8, column=0)
        self.newNodeRest1 = tk.Entry(self.addNodeWindow).grid(row=9, column=0, padx=5)
        tk.Label(self.addNodeWindow, text='Rest_c').grid(row=8, column=1)
        self.newNodeRest2 = tk.Entry(self.addNodeWindow).grid(row=9, column=1, padx=5)
        tk.Label(self.addNodeWindow, text='Pos_x').grid(row=10, column=0)
        self.newNodePosX = tk.Entry(self.addNodeWindow).grid(row=11, column=0, padx=5)
        tk.Label(self.addNodeWindow, text='Pos_y').grid(row=10, column=1)
        self.newNodePosY = tk.Entry(self.addNodeWindow).grid(row=11, column=1, padx=5)
        self.deliverPace = tk.Button(self.addNodeWindow, text="Add node", background='white', command=self.add_node)
        self.deliverPace.grid(row=12, column=0, padx=5, pady=10, sticky='nesw')
        self.deliverPace = tk.Button(self.addNodeWindow, text="Cancel", background='white', command=self.addNodeWindow.destroy)
        self.deliverPace.grid(row=12, column=1, padx=5, pady=10, sticky='nesw')
    
    def open_add_path(self):
        self.addPathWindow = tk.Toplevel(self.root)
        for i in range(8):
            self.addPathWindow.grid_columnconfigure(i, weight=1)
        for i in range(15):
            self.addPathWindow.grid_rowconfigure(i, weight=1)
        tk.Label(self.addPathWindow, text='Path Name').grid(row=0, columnspan=2)
        self.newPathName = tk.Entry(self.addPathWindow).grid(row=1, columnspan=2)
        tk.Label(self.addPathWindow, text='Select Source Node').grid(row=2, column=0, padx=5)
        self.selectedSourceNode = tk.Listbox(self.addPathWindow, selectmode=tk.BROWSE, exportselection=False)
        for i in range(len(self.heartModel.simData.node_table)):
            self.selectedSourceNode.insert(i + 1, self.heartModel.simData.node_table[i][0])
        self.selectedSourceNode.grid(row=3, column=0, padx=5, pady=5)
        tk.Label(self.addPathWindow, text='Select Destination Node').grid(row=2, column=1, padx=5)
        self.selectedDestinationNode = tk.Listbox(self.addPathWindow, selectmode=tk.BROWSE, exportselection=False)
        for i in range(len(self.heartModel.simData.node_table)):
            self.selectedDestinationNode.insert(i + 1, self.heartModel.simData.node_table[i][0])
        self.selectedDestinationNode.grid(row=3, column=1, padx=5, pady=5)
        tk.Label(self.addPathWindow, text='Path Amplitude').grid(row=5, columnspan=2)
        self.newPathAmp = tk.Entry(self.addPathWindow).grid(row=6, columnspan=2)
        tk.Label(self.addPathWindow, text='Path Ante').grid(row=7, columnspan=2)
        self.newPathAnte = tk.Entry(self.addPathWindow).grid(row=8, columnspan=2)
        tk.Label(self.addPathWindow, text='Path Retro').grid(row=9, columnspan=2)
        self.newPathRetro = tk.Entry(self.addPathWindow).grid(row=10, columnspan=2)
        self.addNewPath = tk.Button(self.addPathWindow, text="Add path", background='white', command=self.add_path)
        self.addNewPath.grid(row=11, column=0, padx=5, pady=5, sticky='nesw')
        self.cancelPath = tk.Button(self.addPathWindow, text="Cancel", background='white', command=self.addPathWindow.destroy)
        self.cancelPath.grid(row=11, column=1, padx=5, pady=5, sticky='nesw')
        
        
    
    def open_add_prope(self):
        self.addPropeWindow = tk.Toplevel(self.root)
        for i in range(8):
            self.addPropeWindow.grid_columnconfigure(i, weight=1)
        for i in range(10):
            self.addPropeWindow.grid_rowconfigure(i, weight=1)
        tk.Label(self.addPropeWindow, text='Prope Name').grid(row=0, padx=20)
        self.newPropeName = tk.Entry(self.addPropeWindow).grid(row=1, padx=20)
        tk.Label(self.addPropeWindow, text='Select Nodes').grid(row=2, padx=20, pady=5)
        self.selectedPropes = tk.Listbox(self.addPropeWindow, selectmode=tk.MULTIPLE)
        for i in range(len(self.heartModel.simData.node_table)):
            self.selectedPropes.insert(i + 1, self.heartModel.simData.node_table[i][0])
        self.selectedPropes.grid(row=3, padx=20)
        self.addNewPrope = tk.Button(self.addPropeWindow, text="Add prope", background='white', command=self.add_prope)
        self.addNewPrope.grid(row=4, column=0, padx=20, pady=5, sticky='nesw')
        self.cancelPrope = tk.Button(self.addPropeWindow, text="Cancel", background='white', command=self.addPropeWindow.destroy)
        self.cancelPrope.grid(row=5, column=0, padx=20, pady=5, sticky='nesw')

    def add_node(self):
        # TODO
        return None
    
    def add_path(self):
        # TODO
        return None

    def add_prope(self):
        # TODO
        return None
    

    def openEGM(self):
        # TODO
        return None
    
    def saveEGM(self):
        # TODO
        return None