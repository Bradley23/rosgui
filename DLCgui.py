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

import tkinter as tk
from tkinter.filedialog import askopenfilenames,askopenfilename,askdirectory
from tkinter.simpledialog import askstring,askinteger
from tkinter.messagebox import askokcancel
import os

win_color = '#333333'
frame_color = '#555555'
winheight = 600
winwidth = 800
framewidth = (winwidth/2)-20
column1spacing = framewidth/12
column2spacing = framewidth*7/12
buttonwidth = 10
buttonheight = 2
fontcolor = '#ffffff'
fontsize = 12

class MyWindow:
    
    def __init__(self, win):
        # top left frame
        self.topleft = tk.Frame(win, width=framewidth, height=(winheight/4)-20, bg=frame_color)
        self.topleft.grid(row=0, column=0, padx=10, pady=10)
        
        self.direct = tk.Button(self.topleft, text='Directory', command=self.direct, height=buttonheight, width=buttonwidth)
        self.direct.place(x=column1spacing, y=20)
        self.config = tk.Button(self.topleft, text='Config', command=self.config, height=buttonheight, width=buttonwidth)
        self.config.place(x=column1spacing, y=70)
        self.choosefile = tk.Button(self.topleft, text='Choose File', command=self.choosefile, height=buttonheight, width=buttonwidth)
        self.choosefile.place(x=column2spacing, y=20)
        self.choosefolder = tk.Button(self.topleft, text='Choose Folder', command=self.choosefolder, height=buttonheight, width=buttonwidth)
        self.choosefolder.place(x=column2spacing, y=70)
        
        # mid left frame
        self.midleft = tk.Frame(win, width=framewidth, height=(winheight/2)-20, bg=frame_color)
        self.midleft.grid(row=1, column=0, padx=10, pady=10, rowspan=2)
        
        self.direct = tk.Button(self.midleft, text='Create Project', command=self.createproj, height=buttonheight, width=buttonwidth)
        self.direct.place(x=column2spacing, y=20)
        self.config = tk.Button(self.midleft, text='Add Videos', command=self.addvids, height=buttonheight, width=buttonwidth)
        self.config.place(x=column2spacing, y=70)
        self.choosefile = tk.Button(self.midleft, text='Extract Frames', command=self.extframes, height=buttonheight, width=buttonwidth)
        self.choosefile.place(x=column2spacing, y=120)
        self.choosefolder = tk.Button(self.midleft, text='Label Frames', command=self.labframes, height=buttonheight, width=buttonwidth)
        self.choosefolder.place(x=column2spacing, y=170)
        self.choosefolder = tk.Button(self.midleft, text='Training Dataset', command=self.traindataset, height=buttonheight, width=buttonwidth)
        self.choosefolder.place(x=column2spacing, y=220)
        
        midlefttext = """__Startup__
Begin by choosing base directory. Then choose config file.
To select videos, use "Choose Folder" to automatically select all videos within a rat# folder.
To select specific videos, use "Choose File" to select videos within a rat# folder.\n
__Create Project__
Use "Directory" to set location of network.
Use "Choose File/Folder" to select videos."""
        
        self.p1 = tk.Label(self.midleft, justify=tk.LEFT, fg=fontcolor, text=midlefttext, wraplength=190, bg=frame_color, font=("TkDefaultFont",fontsize))
        self.p1.place(x=5, y=5)
        
        # bot left frame
        self.botleft = tk.Frame(win, width=framewidth, height=(winheight/4)-20, bg=frame_color)
        self.botleft.grid(row=3, column=0, padx=10, pady=10)
        
        self.direct = tk.Button(self.botleft, text='Train Network', command=self.trainnet, height=buttonheight, width=buttonwidth)
        self.direct.place(x=column1spacing, y=45)
        self.choosefile = tk.Button(self.botleft, text='Evaluate Network', command=self.evalnet, height=buttonheight, width=buttonwidth)
        self.choosefile.place(x=column2spacing, y=45)
        
        # top right frame
        self.topright = tk.Frame(win, width=framewidth, height=(winheight/4)-20, bg=frame_color)
        self.topright.grid(row=0, column=1, padx=10, pady=10)
        
        self.progresstitle = tk.Label(self.topright, fg=fontcolor, text = 'Progess', bg=frame_color, font=("TkDefaultFont", 25))
        self.progresstitle.place(x=130, y=5)
        
        self.progressbarout = tk.Frame(self.topright, width=6*framewidth/8, height = 30, bg=frame_color, highlightbackground="#ffffff", highlightthickness=2)
        self.progressbarout.place(x=framewidth/8,y=60)
        
        self.progressbar = tk.Frame(self.progressbarout, width=0, height=30-4, bg='#00ff00')
        self.progressbar.place(x=0,y=0)
        
        self.text = tk.StringVar()
        self.text.set('0 %')
        self.progresstitle = tk.Label(self.topright, fg=fontcolor, textvariable = self.text, bg=frame_color, font=("TkDefaultFont", 18))
        self.progresstitle.place(x=framewidth/8, y=95)
        
        # bot right frame
        self.botright = tk.Frame(win, width=framewidth, height=(winheight/(4/3))-20, bg=frame_color)
        self.botright.grid(row=1, column=1, padx=10, pady=10, rowspan=3)
        
        self.direct = tk.Button(self.botright, text='Analyze/Label', command=self.analyzelabel, height=buttonheight, width=buttonwidth)
        self.direct.place(x=column2spacing, y=20)
        self.config = tk.Button(self.botright, text='Extract Outliers', command=self.extoutliers, height=buttonheight, width=buttonwidth)
        self.config.place(x=column2spacing, y=70)
        self.choosefile = tk.Button(self.botright, text='Refine Labels', command=self.refinelabels, height=buttonheight, width=buttonwidth)
        self.choosefile.place(x=column2spacing, y=120)
        self.choosefolder = tk.Button(self.botright, text='Merge Datasets', command=self.merge, height=buttonheight, width=buttonwidth)
        self.choosefolder.place(x=column2spacing, y=170)
        
        botrighttext = """__Analyze/Label__
Analyzes and Labels all videos chosen with Choose File/Folder.\n
__Choose Folder__
Choose week/cam/"rat" folder which selects all.mp4 files inside.\n
__Choose File__
Choose specific folders for indicidual .mp4 files."""
        
        self.p1 = tk.Label(self.botright, justify=tk.LEFT, fg=fontcolor, text=botrighttext, wraplength=190, bg=frame_color, font=("TkDefaultFont",fontsize))
        self.p1.place(x=5, y=5)
        
    def direct(self):
        self.curdir = askdirectory()
    def config(self):
        self.configfile = askopenfilename(initialdir=self.curdir)
    def choosefile(self):
        dirpaths = []
        self.vidpaths=[]
        dirpaths.append(askdirectory(initialdir=self.curdir))
        answer = askokcancel(title='Deeplabcut Operator',message='Press "Ok" to select more videos.')
        while answer:
            dirpaths.append(askdirectory(initialdir=self.curdir))
            answer = askokcancel(title='Deeplabcut Operator',message='Press "Ok" to select more videos.')
        else:
            pass
        for paths in dirpaths:
            files = []
            for (dirpath, dirnames, filenames) in os.walk(paths):
                files.extend(filenames)
                break
            for vidname in files:
                if vidname[-4:] == '.mp4':
                    fullpath = dirpath+'/'+vidname
                    self.vidpaths.append(fullpath)
                else:
                    pass
        print(self.vidpaths)
    def choosefolder(self):
        self.vidpaths = []
        dirpaths = []
        folderpath = askdirectory(initialdir=self.curdir)
        files = []
        for (dirpath, dirnames, filenames) in os.walk(folderpath):
            files.extend(dirnames)
            break
        for a in files:
            fullpath = dirpath+'/'+a
            dirpaths.append(fullpath)
        for foldername in dirpaths:
            files2 = []
            for (dirpath2,dirnames2,filenames2) in os.walk(foldername):
                files2.extend(filenames2)
                break
            allmp4s = []
            for vidname in files2:
                if vidname[-4:] == '.mp4':
                    fullpath = dirpath2+'/'+vidname
                    allmp4s.append(fullpath)
                else:
                    pass
            if len(allmp4s) == 1:
                self.vidpaths.append(allmp4s[0])
            else:
                pass
    
    def createproj(self):
        progresspercent = '0 %'
        self.text.set(progresspercent)
        self.progressbar.config(width=0)
        window.update()
        projname = askstring('Create New Project','Title of Project?')
        initials = askstring('Create New Project','Creator Initials?')
        #dlc.create_new_project(projname,initials,self.vidpaths, working_directory=self.curdir,copy_videos=False)
        progresspercent = '100 %'
        self.text.set(progresspercent)
        self.progressbar.config(width=6*framewidth/8-4)
        window.update()
    def addvids(self):
        progresspercent = '0 %'
        self.text.set(progresspercent)
        self.progressbar.config(width=0)
        window.update()
        #dlc.add_new_videos(self.configfile,self.vidpaths,copy_videos=False)
        progresspercent = '100 %'
        self.text.set(progresspercent)
        self.progressbar.config(width=6*framewidth/8-4)
        window.update()
    def extframes(self):
        progresspercent = '0 %'
        self.text.set(progresspercent)
        self.progressbar.config(width=0)
        window.update()
        #dlc.extract_frames(self.configfile,"manual",crop=False, userfeedback=False)
        progresspercent = '100 %'
        self.text.set(progresspercent)
        self.progressbar.config(width=6*framewidth/8-4)
        window.update()
    def labframes(self):
        progresspercent = '0 %'
        self.text.set(progresspercent)
        self.progressbar.config(width=0)
        window.update()
        #dlc.label_frames(self.configfile)
        progresspercent = '100 %'
        self.text.set(progresspercent)
        self.progressbar.config(width=6*framewidth/8-4)
        window.update()
    def traindataset(self):
        progresspercent = '0 %'
        self.text.set(progresspercent)
        self.progressbar.config(width=0)
        window.update()
        #dlc.create_training_dataset(self.configfile,num_shuffles=1)
        progresspercent = '100 %'
        self.text.set(progresspercent)
        self.progressbar.config(width=6*framewidth/8-4)
        window.update()
    
    def trainnet(self):
        progresspercent = '0 %'
        self.text.set(progresspercent)
        self.progressbar.config(width=0)
        window.update()
        maxiters = askinteger('Train Network',"""Maxiters? (typically "200000")""")
        #dlc.train_network(self.configfile,maxiters=maxiters)
        progresspercent = '100 %'
        self.text.set(progresspercent)
        self.progressbar.config(width=6*framewidth/8-4)
        window.update()
    def evalnet(self):
        progresspercent = '0 %'
        self.text.set(progresspercent)
        self.progressbar.config(width=0)
        window.update()
        #dlc.evaluate_network(self.configfile,plotting=True)
        progresspercent = '100 %'
        self.text.set(progresspercent)
        self.progressbar.config(width=6*framewidth/8-4)
        window.update()
    def analyzelabel(self):
        progress = 0
        progresspercent = '0 %'
        self.text.set(progresspercent)
        self.progressbar.config(width=0)
        window.update()
        for vid in self.vidpaths:
            #dlc.analyze_videos(self.configfile,vid,shuffle=1,save_as_csv=True)
            #dlc.create_labeled_video(self.configfile,vid,draw_skeleton=True)
            progress = progress + 1
            progresspercent = 100 * progress / len(self.vidpaths)
            self.progressbar.config(width=progresspercent*(6*framewidth/8-4)/100)
            progresspercent = str(progresspercent)
            progresspercent = progresspercent + ' %'
            self.text.set(progresspercent)
            window.update()
    def extoutliers(self):
        progresspercent = '0 %'
        self.text.set(progresspercent)
        self.progressbar.config(width=0)
        window.update()
        #dlc.extract_outlier_frames(self.configfile,self.vidpaths)
        progresspercent = '100 %'
        self.text.set(progresspercent)
        self.progressbar.config(width=6*framewidth/8-4)
        window.update()
    def refinelabels(self):
        progresspercent = '0 %'
        self.text.set(progresspercent)
        self.progressbar.config(width=0)
        window.update()
        #dlc.refine_labels(self.configfile)
        progresspercent = '100 %'
        self.text.set(progresspercent)
        self.progressbar.config(width=6*framewidth/8-4)
        window.update()
    def merge(self):
        progresspercent = '0 %'
        self.text.set(progresspercent)
        self.progressbar.config(width=0)
        window.update()
        #dlc.merge_datasets(self.configfile)
        progresspercent = '100 %'
        self.text.set(progresspercent)
        self.progressbar.config(width=6*framewidth/8-4)
        window.update()


# window properties
window = tk.Tk()
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
