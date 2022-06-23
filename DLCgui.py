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
from tkinter.filedialog import askopenfilenames,askopenfilename,askdirectory
from tkinter.simpledialog import askstring,askinteger
import os

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
        
        self.direct = Button(self.topleft, text='Directory', command=self.direct, height=2, width=10)
        self.direct.place(x=column1spacing, y=20)
        self.config = Button(self.topleft, text='Config', command=self.config, height=2, width=10)
        self.config.place(x=column1spacing, y=70)
        self.choosefile = Button(self.topleft, text='Choose File', command=self.choosefile, height=2, width=10)
        self.choosefile.place(x=column2spacing, y=20)
        self.choosefolder = Button(self.topleft, text='Choose Folder', command=self.choosefolder, height=2, width=10)
        self.choosefolder.place(x=column2spacing, y=70)
        
        # mid left frame
        self.midleft = Frame(win, width=framewidth, height=(winheight/2)-20, bg=frame_color)
        self.midleft.grid(row=1, column=0, padx=10, pady=10, rowspan=2)
        
        self.direct = Button(self.midleft, text='Create Project', command=self.createproj, height=2, width=10)
        self.direct.place(x=column2spacing, y=20)
        self.config = Button(self.midleft, text='Add Videos', command=self.addvids, height=2, width=10)
        self.config.place(x=column2spacing, y=70)
        self.choosefile = Button(self.midleft, text='Extract Frames', command=self.extframes, height=2, width=10)
        self.choosefile.place(x=column2spacing, y=120)
        self.choosefolder = Button(self.midleft, text='Label Frames', command=self.labframes, height=2, width=10)
        self.choosefolder.place(x=column2spacing, y=170)
        self.choosefolder = Button(self.midleft, text='Training Dataset', command=self.traindataset, height=2, width=10)
        self.choosefolder.place(x=column2spacing, y=220)
        
        # bot left frame
        self.botleft = Frame(win, width=framewidth, height=(winheight/4)-20, bg=frame_color)
        self.botleft.grid(row=3, column=0, padx=10, pady=10)
        
        self.direct = Button(self.botleft, text='Train Network', command=self.trainnet, height=2, width=10)
        self.direct.place(x=column1spacing, y=45)
        self.choosefile = Button(self.botleft, text='Evaluate Network', command=self.evalnet, height=2, width=10)
        self.choosefile.place(x=column2spacing, y=45)
        
        # top right frame
        self.topright = Frame(win, width=framewidth, height=(winheight/4)-20, bg=frame_color)
        self.topright.grid(row=0, column=1, padx=10, pady=10)
        
        self.progresstitle = Label(self.topright, text = 'Progess', bg=frame_color, font=("TkDefaultFont", 25))
        self.progresstitle.place(x=130, y=5)
        
        self.text = StringVar()
        self.text.set('0 %')
        self.progresstitle = Label(self.topright, textvariable = self.text, bg=frame_color, font=("TkDefaultFont", 18))
        self.progresstitle.place(x=155, y=55)
        
        # bot right frame
        self.botright = Frame(win, width=framewidth, height=(winheight/(4/3))-20, bg=frame_color)
        self.botright.grid(row=1, column=1, padx=10, pady=10, rowspan=3)
        
        self.direct = Button(self.botright, text='Analyze/Label', command=self.analyzelabel, height=2, width=10)
        self.direct.place(x=column2spacing, y=20)
        self.config = Button(self.botright, text='Extract Outliers', command=self.extoutliers, height=2, width=10)
        self.config.place(x=column2spacing, y=70)
        self.choosefile = Button(self.botright, text='Refine Labels', command=self.refinelabels, height=2, width=10)
        self.choosefile.place(x=column2spacing, y=120)
        self.choosefolder = Button(self.botright, text='Merge Datasets', command=self.merge, height=2, width=10)
        self.choosefolder.place(x=column2spacing, y=170)
        
    def direct(self):
        self.curdir = askdirectory()
    def config(self):
        self.configfile = askopenfilename(initialdir=self.curdir)
    def choosefile(self):
        self.vidpaths = askopenfilenames(initialdir=self.curdir)
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
        print(dirpaths)
        for foldername in dirpaths:
            files2 = []
            for (dirpath2,dirnames2,filenames2) in os.walk(foldername):
                files2.extend(filenames2)
                break
            for vidname in files2:
                if vidname[-4:] == '.mp4':
                    fullpath = dirpath2+'/'+vidname
                    self.vidpaths.append(fullpath)
                else:
                    pass
        print(self.vidpaths)
    
    def createproj(self):
        progresspercent = '0 %'
        self.text.set(progresspercent)
        window.update()
        projname = askstring('Create New Project','Title of Project?')
        initials = askstring('Create New Project','Creator Initials?')
        #dlc.create_new_project(projname,initials,self.vidpaths, working_directory=vidpath,copy_videos=False)
        progresspercent = '100 %'
        self.text.set(progresspercent)
        window.update()
    def addvids(self):
        progresspercent = '0 %'
        self.text.set(progresspercent)
        window.update()
        #dlc.add_new_videos(self.configfile,self.vidpaths,copy_videos=False)
        progresspercent = '100 %'
        self.text.set(progresspercent)
        window.update()
    def extframes(self):
        progresspercent = '0 %'
        self.text.set(progresspercent)
        window.update()
        #dlc.extract_frames(self.configfile,‘manual’,crop=False, userfeedback=False)
        progresspercent = '100 %'
        self.text.set(progresspercent)
        window.update()
    def labframes(self):
        progresspercent = '0 %'
        self.text.set(progresspercent)
        window.update()
        #dlc.label_frames(self.configfile)
        progresspercent = '100 %'
        self.text.set(progresspercent)
        window.update()
    def traindataset(self):
        progresspercent = '0 %'
        self.text.set(progresspercent)
        window.update()
        #dlc.create_training_dataset(self.configfile,num_shuffles=1)
        progresspercent = '100 %'
        self.text.set(progresspercent)
        window.update()
    
    def trainnet(self):
        progresspercent = '0 %'
        self.text.set(progresspercent)
        window.update()
        maxiters = askinteger('Train Network',"""Maxiters? (typically "200000")""")
        #dlc.train_network(self.configfile,maxiters=maxiters)
        progresspercent = '100 %'
        self.text.set(progresspercent)
        window.update()
    def evalnet(self):
        progresspercent = '0 %'
        self.text.set(progresspercent)
        window.update()
        #dlc.evaluate_network(self.configfile,plotting=True)
        progresspercent = '100 %'
        self.text.set(progresspercent)
        window.update()    
    def analyzelabel(self):
        progress = 0
        progresspercent = '0 %'
        self.text.set(progresspercent)
        window.update()
        for vid in self.vidpaths:
            #dlc.analyze_videos(self.configfile,vid,shuffle=1,save_as_csv=True)
            #dlc.create_labeled_video(self.configfile,vid,draw_skeleton=True)
            progress = progress + 1
            progresspercent = 100 * progress / len(self.vidpaths)
            progresspercent = str(progresspercent)
            progresspercent = progresspercent + ' %'
            self.text.set(progresspercent)
            window.update()
    def extoutliers(self):
        progresspercent = '0 %'
        self.text.set(progresspercent)
        window.update()
        #dlc.extract_outlier_frames(self.configfile,self.vidpaths)
        progresspercent = '100 %'
        self.text.set(progresspercent)
        window.update()
    def refinelabels(self):
        progresspercent = '0 %'
        self.text.set(progresspercent)
        window.update()
        #dlc.refine_labels(self.configfile)
        progresspercent = '100 %'
        self.text.set(progresspercent)
        window.update()
    def merge(self):
        progresspercent = '0 %'
        self.text.set(progresspercent)
        window.update()
        #dlc.merge_datasets(self.configfile)
        progresspercent = '100 %'
        self.text.set(progresspercent)
        window.update()


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
