#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 11:27:11 2022

@author: bradleyrauscher
"""

# /DLC commands
#import tensorflow as tf
#gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.7)
#sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))
#import deeplabcut as dlc
# /end

from tkinter import *
from tkinter.filedialog import askopenfilenames,askopenfilename

win_color = '#333333'
frame_color = '#555555'
winheight = 600
winwidth = 800
framewidth = (winwidth/2)-20
column1spacing = framewidth/12
column2spacing = framewidth*7/12


class MyWindow:
    def __init__(self, win):
        # top left frame
        self.topleft = Frame(win, width=framewidth, height=(winheight/4)-20, bg=frame_color)
        self.topleft.grid(row=0, column=0, padx=10, pady=10)
        
        self.config = Button(self.topleft, text='Config', command=self.addfile, height=2, width=10)
        self.config.place(x=column1spacing, y=30)
        self.choosefile = Button(self.topleft, text='Choose File', command=self.addfile, height=2, width=10)
        self.choosefile.place(x=column2spacing, y=30)
        self.choosefolder = Button(self.topleft, text='Choose Folder', command=self.addfile, height=2, width=10)
        self.choosefolder.place(x=column2spacing, y=80)
        
        
        # mid left frame
        self.midleft = Frame(win, width=framewidth, height=(winheight/2)-20, bg=frame_color)
        self.midleft.grid(row=1, column=0, padx=10, pady=10, rowspan=2)
        
        # bot left frame
        self.botleft = Frame(win, width=framewidth, height=(winheight/4)-20, bg=frame_color)
        self.botleft.grid(row=3, column=0, padx=10, pady=10)
        
        # top right frame
        self.topright = Frame(win, width=framewidth, height=(winheight/4)-20, bg=frame_color)
        self.topright.grid(row=0, column=1, padx=10, pady=10)
        
        self.progresstitle = Label(self.topright, text = 'Progess', bg=frame_color, font=("TkDefaultFont", 25))
        self.progresstitle.place(x=130, y=5)
        
        # bot right frame
        self.botright = Frame(win, width=framewidth, height=(winheight/(4/3))-20, bg=frame_color)
        self.botright.grid(row=1, column=1, padx=10, pady=10, rowspan=3)
        
        
        # buttons
        
        self.startswitch = Button(self.botright, text='Off', height=2, width=10, command=self.start)
        self.startswitch.place(x=100,y=50)
        
    def addfile(self):
        filename = askopenfilenames()
        print(filename)
    def start(self):
        if self.startswitch.config('text')[-1] == 'On':
            self.startswitch.config(text='Off')
        else:
            self.startswitch.config(text='On')

# window properties
window = Tk()
mywin=MyWindow(window)
window.title('DeepLabCut Operator')

heightstr = str(winheight)
widthstr = str(winwidth)

geostr = widthstr+"x"+heightstr+"+200+100"

window.geometry(geostr)
window.configure(bg=win_color)
window.resizable(False, False)
window.mainloop()

#analyze/label videos, choose week, 
