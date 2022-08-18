#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 18:00:01 2022

@author: bradleyrauscher
"""

# /DLC commands
#import tensorflow as tf
#gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.7)
#sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))
#import deeplabcut as dlc
# /end

import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename,askdirectory
from tkinter.simpledialog import askstring,askinteger
from tkinter.messagebox import askokcancel
import os
from PyQt5 import QtCore
import subprocess
import time

padding = 10
toppadding = 5
winheight = 525
winwidth = 500
win_color = '#222222'
frame_color = '#333333'


butpadding = 20

class ProcessRunnable(QtCore.QRunnable):
    def __init__(self, target, args):
        QtCore.QRunnable.__init__(self)
        self.t = target
        self.args = args

    def run(self):
        self.t(self.args)

    def start(self):
        QtCore.QThreadPool.globalInstance().start(self)

def run(log):
    print('hello')
    log.progressbar['value'] = 100
    log.curdir = '/'
    time.sleep(5)
    print('done')

class MyWindow:
    def __init__(self,win):
        
        s = ttk.Style()
        print(s.theme_names())
        
        print(s.theme_use())
        
        s.theme_use('clam')
        
        s.configure('TFrame',background=win_color)
        s.configure('TCheckbutton',background=win_color,foreground='#dddddd')
        s.configure('TButton',background='#ee0011',bordercolor='#ee0011',foreground='#eeeeee')
        s.configure("Treeview", background=frame_color, fieldbackground=frame_color, foreground="#dddddd")
        
        self.topleftframe(win)
        self.toprightframe(win)
        self.botleftframe(win)
        self.botrightframe(win)
        self.progressbarframe(win)
        self.topframe(win)
        
        #layout
        self.top.grid(row=0,column=0,columnspan=2, padx=toppadding,pady=toppadding,sticky='NSEW')
        self.topleft.grid(row=1, column=0, padx=padding, pady=padding, sticky='NSEW')
        self.topright.grid(row=1, column=1, padx=padding, pady=padding, sticky='NSEW')
        self.botleft.grid(row=2, column=0, padx=padding, pady=padding, sticky='NSEW')
        self.botright.grid(row=2, column=1, padx=padding, pady=padding, sticky='NSEW')
        self.pbframe.grid(row=3, column=0, columnspan=2)
        tk.Frame(win,height=5,bg=win_color).grid(row=4,column=0)
        
        win.grid_columnconfigure(0, weight=1, uniform='x')
        win.grid_columnconfigure(1, weight=1, uniform='x')
        win.grid_rowconfigure(1,weight=1,uniform='y')
        win.grid_rowconfigure(2,weight=1,uniform='y')
        
        self.curdir = '/'
        
    def topframe(self,inp):
        self.top = ttk.Frame(inp,style='TFrame')
        cont = self.top
        
        w1 = ttk.Button(cont,text="Directory", style="big.TButton", command=self.choosedir)
        w1.grid(row=0,column=0,padx=toppadding,pady=toppadding,sticky='WE')
        
        w2 = ttk.Button(cont,text="Config File", style="big.TButton", command=self.choosecon)
        w2.grid(row=0,column=1,padx=toppadding,pady=toppadding,sticky='WE')
        
        w3 = ttk.Button(cont,text="Videos", style="big.TButton", command=self.choosevidspar)
        w3.grid(row=0,column=2,padx=toppadding,pady=toppadding,sticky='WE')
        
        w4 = ttk.Button(cont,text="Help", style="big.TButton", command=self.openhelp)
        w4.grid(row=1,column=0,padx=toppadding,pady=toppadding,sticky='WE')
        
        self.slv = tk.IntVar(value=0)
        self.svm = tk.IntVar(value=0)
        
        w5 = ttk.Checkbutton(cont,text="Select labeled videos",variable = self.slv,onvalue=1,offvalue=0)
        w5.grid(row=1,column=1,padx=toppadding,pady=toppadding,sticky='W')
        
        w6 = ttk.Checkbutton(cont,text="Manually select files",variable = self.svm,onvalue=1,offvalue=0)
        w6.grid(row=1,column=2,padx=toppadding,pady=toppadding,sticky='W')
        
        cont.grid_columnconfigure(0,weight=1,uniform='y')
        cont.grid_columnconfigure(1,weight=1,uniform='y')
        cont.grid_columnconfigure(2,weight=1,uniform='y')
    
    def topleftframe(self,inp):
        self.topleft = tk.Frame(inp,bg=frame_color)
        cont = self.topleft
        
        w1 = ttk.Button(cont,text="Create Project", style="big.TButton")
        w1.grid(row=0,column=0,padx=butpadding,sticky='WE')
        
        w2 = ttk.Button(cont,text="Add Videos", style="big.TButton")
        w2.grid(row=1,column=0,padx=butpadding,sticky='WE')
        
        w3 = ttk.Button(cont,text="Extract Frames", style="big.TButton")
        w3.grid(row=2,column=0,padx=butpadding,sticky='WE')
        
        w4 = ttk.Button(cont,text="Label Frames", style="big.TButton")
        w4.grid(row=3,column=0,padx=butpadding,sticky='WE')
        
        cont.grid_columnconfigure(0,weight=1)
        cont.grid_rowconfigure(0,weight=1)
        cont.grid_rowconfigure(1,weight=1)
        cont.grid_rowconfigure(2,weight=1)
        cont.grid_rowconfigure(3,weight=1)
        
        
    def toprightframe(self,inp):
        self.topright = tk.Frame(inp,bg=frame_color)
        cont = self.topright
        
        w1 = ttk.Button(cont,text="Analyze/Label Videos", style="big.TButton", command=(lambda: self.backproc(self)))
        w1.grid(row=0,column=0,padx=butpadding,sticky='WE')
        
        w2 = ttk.Button(cont,text="Extract Outliers", style="big.TButton", command=self.progress)
        w2.grid(row=1,column=0,padx=butpadding,sticky='WE')
        
        w3 = ttk.Button(cont,text="Refine Labels", style="big.TButton", command=self.reset)
        w3.grid(row=2,column=0,padx=butpadding,sticky='WE')
        
        w4 = ttk.Button(cont,text="Merge Datasets", style="big.TButton", command=self.cleargrid)
        w4.grid(row=3,column=0,padx=butpadding,sticky='WE')
        
        cont.grid_columnconfigure(0,weight=1)
        cont.grid_rowconfigure(0,weight=1)
        cont.grid_rowconfigure(1,weight=1)
        cont.grid_rowconfigure(2,weight=1)
        cont.grid_rowconfigure(3,weight=1)
        
        
    def botleftframe(self,inp):
        self.botleft = tk.Frame(inp,bg=frame_color)
        cont = self.botleft
        
        w1 = ttk.Button(cont,text="Create Training Dataset", style="big.TButton")
        w1.grid(row=0,column=0,padx=butpadding,sticky='WE')
        
        w2 = ttk.Button(cont,text="Train Network", style="big.TButton")
        w2.grid(row=1,column=0,padx=butpadding,sticky='WE')
        
        w3 = ttk.Button(cont,text="Evaluate Network", style="big.TButton")
        w3.grid(row=2,column=0,padx=butpadding,sticky='WE')
        
        w4 = tk.Label(cont)
        w4.grid(row=3,column=0,padx=butpadding,sticky='WE')
        
        cont.grid_columnconfigure(0,weight=1)
        cont.grid_rowconfigure(0,weight=1)
        cont.grid_rowconfigure(1,weight=1)
        cont.grid_rowconfigure(2,weight=1)
        cont.grid_rowconfigure(3,weight=1)
        
        
    def botrightframe(self,inp):
        self.botright = tk.Frame(inp,bg=frame_color)
        cont = self.botright
        
        self.vidgrid = ttk.Treeview(cont,columns=('vid'),show='headings')
        self.vidgrid.column('vid')
        self.vidgrid.heading('vid', text='Videos')
        for i in range(30):
            self.vidgrid.insert('', tk.END, values=i)
        
        self.vidgrid.grid(row=0,column=0)
        self.vidgrid.pack(fill='x')
        self.vidgrid.insert('',tk.END, values='/Users/bradleyrauscher/Documents/Coding/DLC_Complete_Guide.pdf')
        
        self.vidgrid.bind("<Double-1>", self.opengridlink)
        
    def progressbarframe(self,inp):
        self.pbframe = tk.Frame(inp, bg=win_color)
        cont = self.pbframe
        
        self.progressbar = ttk.Progressbar(cont,length=450, mode='determinate')
        self.progressbar.grid(row=0,column=0,padx=padding,pady=padding,sticky="WE")
        
        cont.grid_columnconfigure(0,weight=1)
        cont.grid_rowconfigure(0,weight=1)
        
    #___Button Functions___
    
    #__Top Frame__
    def choosedir(self):
        self.curdir = askdirectory(initialdir=self.curdir)
        print(self.curdir)
    
    def choosecon(self):
        self.configfile,_ = askopenfilename(initialdir=self.curdir)
        print(self.configfile)
        
    def choosevidspar(self):
        if self.svm.get():
            self.choosevid()
        else:
            self.chooselabeledvidspar()
    
    def chooselabeledvidspar(self):
        if self.slv.get():
            self.chooselabeledvids()
        else:
            self.choosevids()
        pass
    
    def chooselabeledvids(self):
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
            mp4files = []
            for (dirpath2,dirnames2,filenames2) in os.walk(foldername):
                files2.extend(filenames2)
                break
            for vidname in files2:
                if vidname[-3:] == '.py':
                    fullpath = dirpath2+'/'+vidname
                    mp4files.append(fullpath)
                else:
                    pass
            self.vidpaths.append(min(mp4files,key=len))
        print(self.vidpaths)
        lenstr = "Selected " + str(len(self.vidpaths)) + " videos"
        print(lenstr)
    
    def choosevids(self):
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
                if vidname[-3:] == '.py':
                    fullpath = dirpath2+'/'+vidname
                    allmp4s.append(fullpath)
                else:
                    pass
            if len(allmp4s) == 1:
                self.vidpaths.append(allmp4s[0])
            else:
                pass
        print(self.vidpaths)
        lenstr = "Selected " + str(len(self.vidpaths)) + " videos"
        print(lenstr)
    
    def choosevid(self):
        dirpaths = []
        self.vidpaths=[]
        dirpaths.append(askdirectory(initialdir=self.curdir))
        answer = askokcancel(title='Deeplabcut Operator',message='Press "Ok" to select more videos.')
        while answer:
            self.newdir = self.getparent(dirpaths[-1])
            dirpaths.append(askdirectory(initialdir=self.newdir))
            answer = askokcancel(title='Deeplabcut Operator',message='Press "Ok" to select more videos.')
        else:
            pass
        for paths in dirpaths:
            files = []
            mp4files = []
            for (dirpath, dirnames, filenames) in os.walk(paths):
                files.extend(filenames)
                break
            for vidname in files:
                if vidname[-3:] == '.py':
                    fullpath = dirpath+'/'+vidname
                    mp4files.append(fullpath)
                else:
                    pass
            self.vidpaths.append(min(mp4files,key=len))
        print(self.vidpaths)
        lenstr = "Selected " + str(len(self.vidpaths)) + " videos"
        print(lenstr)
    
    def getparent(self,file):
        pos = []
        pos.append(file.find('/',0,len(file)))
        while pos[-1] != -1:
            pos.append(file.find('/',pos[-1]+1,len(file)))
        file = file[:pos[-2]]
        return(file)
    
    def openhelp(self):
        link = '/Users/bradleyrauscher/Documents/Coding/DLC_Complete_Guide.pdf'
        subprocess.Popen(["open",link])
    
    #__DLC Buttons__
    
    def backproc(self,bar):
        self.p = ProcessRunnable(target=run, args=(bar))
        self.p.start()
    
    def progress(self):
        self.progressbar['maximum'] = 160
        self.progressbar.step(20)
        
    def reset(self):
        self.progressbar['value'] = 0
        
    def cleargrid(self):
        self.vidgrid.delete(*self.vidgrid.get_children())
    
    def opengridlink(self,event):
        link = self.vidgrid.item(self.vidgrid.focus())['values']
        subprocess.Popen(["open",link[0]])
        
    
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