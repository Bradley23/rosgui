#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 18:00:01 2022

@author: bradleyrauscher
"""

import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename,askdirectory
from tkinter.simpledialog import askstring,askinteger
from tkinter.messagebox import askokcancel
import os
from PyQt5 import QtCore

padding = 10
winheight = 500
winwidth = 450
win_color = '#222222'
frame_color = '#333333'
frameheight = 100

butheight = 30
butwidth = 100

class MyWindow:
    def __init__(self,win):
        self.topleftframe(win)
        self.toprightframe(win)
        self.botleftframe(win)
        self.botrightframe(win)
        
        #layout
        self.topleft.grid(row=0, column=0, padx=padding, pady=padding, sticky='NSEW')
        self.topright.grid(row=0, column=1, padx=padding, pady=padding, sticky='NSEW')
        self.botleftframe.grid(row=1, column=0, padx=padding, pady=padding, sticky='NSEW')
        self.botrightframe.grid(row=1, column=1, padx=padding, pady=padding, sticky='NSEW')
        
        win.grid_columnconfigure(0, weight=1, uniform='x')
        win.grid_columnconfigure(1, weight=1, uniform='x')
        
    def topleftframe(self,inp):
        self.topleft = tk.Frame(inp,bg=frame_color)
        cont = self.topleft
        
        w1 = ttk.Button(cont,text="example")
        w1.grid(row=0,column=0,padx=padding,sticky='WE')
        
        w2 = ttk.Button(cont,text="example2")
        w2.grid(row=1,column=0,padx=padding,sticky='WE')
        
        
    def toprightframe(self,inp):
        self.topright = tk.Frame(inp,bg=frame_color,height=100)
        
    def botleftframe(self,inp):
        self.botleftframe = tk.Frame(inp,bg=frame_color,height=100)
    
    def botrightframe(self,inp):
        self.botrightframe = tk.Frame(inp,bg=frame_color,height=100)

window = tk.Tk()
app = MyWindow(window)
window.title('DeepLabCut Operator')

heightstr = str(winheight)
widthstr = str(winwidth)

geostr = widthstr+"x"+heightstr+"+200+100"

window.geometry(geostr)
window.configure(bg=win_color)
window.resizable(False, False)
window.mainloop()