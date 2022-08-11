#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 17:09:41 2022

@author: bradleyrauscher
"""

# /DLC commands
#import tensorflow as tf
#gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.7)
#sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))
#import deeplabcut as dlc
# /end

import PyQt5.QtWidgets as ptw
import sys
import subprocess
from PyQt5 import QtCore
import os

xoffset = 350
yoffset = 200
winwidth = 500
winheight = 450


class ProcessRunnable(QtCore.QRunnable):
    def __init__(self, target, args):
        QtCore.QRunnable.__init__(self)
        self.t = target
        self.args = args

    def run(self):
        self.t(self.args)

    def start(self):
        QtCore.QThreadPool.globalInstance().start(self)

def getparentex(file):
    pos = []
    pos.append(file.find('/',0,len(file)))
    while pos[-1] != -1:
        pos.append(file.find('/',pos[-1]+1,len(file)))
    file = file[:pos[-2]]
    return(file)

def run(log):
    Window.disable(log[1],False)
    percent = '0 %'
    QtCore.QMetaObject.invokeMethod(log[1],"setpercent", QtCore.Qt.QueuedConnection,QtCore.Q_ARG(str, percent))    
    progint = 0
    QtCore.QMetaObject.invokeMethod(log[0],"progress", QtCore.Qt.QueuedConnection,QtCore.Q_ARG(int, progint))
    try:
        if log[2] == 'Create Project':
            #dlc.create_new_project(log[1].projname,log[1].initials,log[1].vidpaths, working_directory=log[1].curdir,copy_videos=False)
            pass
        
        elif log[2] == 'Add Videos':
            #dlc.add_new_videos(log[1].configfile,log[1].vidpaths,copy_videos=False)
            pass
        
        elif log[2] == 'Extract Frames':
            #dlc.extract_frames(log[1].configfile,"manual",crop=False, userfeedback=False)
            pass
        
        elif log[2] == 'Label Frames':
            #dlc.label_frames(log[1].configfile)
            pass
        
        elif log[2] == 'Create Training Dataset':
            #dlc.create_training_dataset(log[1].configfile,num_shuffles=1)
            pass
        
        elif log[2] == 'Train Network':
            #dlc.train_network(log[1].configfile,maxiters=log[1].maxiters)
            pass
        
        elif log[2] == 'Evaluate Network':
            #dlc.evaluate_network(log[1].configfile,plotting=True)
            pass
        
        elif log[2] == 'Analyze Label':
            nonsense = 3
            QtCore.QMetaObject.invokeMethod(log[1],"cleartable", QtCore.Qt.QueuedConnection,QtCore.Q_ARG(int, nonsense))
            
            log[1].tabcell = 0
            progrange = len(log[1].vidpaths)
            QtCore.QMetaObject.invokeMethod(log[0],"changerange", QtCore.Qt.QueuedConnection,QtCore.Q_ARG(int, progrange))
            for vid in log[1].vidpaths:
                #dlc.analyze_videos(log[1].configfile,vid,shuffle=1,save_as_csv=True)
                #dlc.create_labeled_video(log[1].configfile,vid,draw_skeleton=True)
                progint += 1
                
                #finds new video
                parent = getparentex(vid)
                
                files = []
                mp4files = []
                
                for (dirpath, dirnames, filenames) in os.walk(parent):
                    files.extend(filenames)
                    break
                for vidname in files:
                    if vidname[-3:] == '.py':
                        fullpath = dirpath+'/'+vidname
                        mp4files.append(fullpath)
                    else:
                        pass
                
                newvid = max(mp4files,key=len)
                
                QtCore.QMetaObject.invokeMethod(log[1],"settableval", QtCore.Qt.QueuedConnection,QtCore.Q_ARG(str, newvid)) 
                
                percent = 100 * progint / progrange
                percent = round(percent,1)
                percent = str(percent) + ' %'
                QtCore.QMetaObject.invokeMethod(log[1],"setpercent", QtCore.Qt.QueuedConnection,QtCore.Q_ARG(str, percent))    
                QtCore.QMetaObject.invokeMethod(log[0],"progress", QtCore.Qt.QueuedConnection,QtCore.Q_ARG(int, progint))
            
        
        elif log[2] == 'Extract Outliers':
            #dlc.extract_outlier_frames(log[1].configfile,log[1].vidpaths)
            pass
        
        elif log[2] == 'Refine Labels':
            #dlc.refine_labels(log[1].configfile)
            pass
        
        elif log[2] == 'Merge Datasets':
            #dlc.merge_datasets(log[1].configfile)
            pass
    except:
        pass
    QtCore.QMetaObject.invokeMethod(log[0],"setmax", QtCore.Qt.QueuedConnection,QtCore.Q_ARG(int, progint))
    percent = '100 %'
    QtCore.QMetaObject.invokeMethod(log[1],"setpercent", QtCore.Qt.QueuedConnection,QtCore.Q_ARG(str, percent))    
    Window.disable(log[1],True)

class myProgressBar(ptw.QProgressBar):
    def __init__(self, parent=None):
        super(myProgressBar, self).__init__(parent)
        self.setValue(0)
    
    @QtCore.pyqtSlot(int)
    def progress(self, progint):
        self.setValue(progint)
    
    @QtCore.pyqtSlot(int)
    def changerange(self, progrange):
        self.setRange(0,progrange)
    
    @QtCore.pyqtSlot(int)
    def setmax(self, progint):
        self.setValue(self.maximum())

class Window(ptw.QMainWindow):
    tabcell = 0
    def __init__(self, parent = None):
        super(Window, self).__init__(parent)
        
        widget = ptw.QWidget()
        choosedir = ptw.QPushButton('Directory')
        choosedir.setDefault(True)
        choosedir.clicked.connect(self.choosedir)
        choosecon = ptw.QPushButton('Config File')
        choosecon.setDefault(True)
        choosecon.clicked.connect(self.choosecon)
        choosevids = ptw.QPushButton('Videos')
        choosevids.setDefault(True)
        choosevids.clicked.connect(self.choosevidspar)
        
        helptab = ptw.QPushButton('Help')
        helptab.clicked.connect(self.openhelp)
        helptab.setDefault(True)
        self.settoggle = ptw.QCheckBox('Select Labeled Videos')
        self.filetab = ptw.QCheckBox('Manually Select Files')
        
        progresslabel = ptw.QLabel('Progress')
        progresslabel.setAlignment(QtCore.Qt.AlignCenter)
        
        self.progresspercent = '0 %'
        self.progressnum = ptw.QLabel(self.progresspercent)
        self.progressnum.setAlignment(QtCore.Qt.AlignRight)
        
        self.createtopleftgb()
        self.createbotleftgb()
        self.createtoprightgb()
        self.createbotrightgb()
        self.bar = myProgressBar(self)
                
        toplayout = ptw.QHBoxLayout()
        toplayout.addWidget(choosedir)
        toplayout.addWidget(choosecon)
        toplayout.addWidget(choosevids)
        
        midlayout = ptw.QHBoxLayout()
        midlayout.addWidget(helptab)
        midlayout.addWidget(self.settoggle)
        midlayout.addWidget(self.filetab)
        
        botlayout = ptw.QHBoxLayout()
        botlayout.addWidget(progresslabel)
        
        perlayout = ptw.QHBoxLayout()
        perlayout.addWidget(self.progressnum)
        
        mainlayout = ptw.QGridLayout()
        mainlayout.addLayout(toplayout,0,0,1,2)
        mainlayout.addLayout(midlayout,1,0,1,2)
        mainlayout.addWidget(self.topleftgb,2,0)
        mainlayout.addWidget(self.botleftgb,3,0)
        mainlayout.addWidget(self.toprightgb,2,1)
        mainlayout.addWidget(self.botrightgb,3,1)
        mainlayout.addLayout(botlayout,4,0,1,2)
        mainlayout.addWidget(self.bar,5,0,1,2)
        mainlayout.addLayout(perlayout,6,0,1,2)
        mainlayout.setRowStretch(1, 1)
        mainlayout.setRowStretch(2, 1)
        mainlayout.setColumnStretch(0, 1)
        mainlayout.setColumnStretch(1, 1)
        widget.setLayout(mainlayout)
        
        self.setCentralWidget(widget)
        
        self.setWindowTitle("DLC Operator")
        self.setGeometry(xoffset,yoffset,winwidth,winheight) #x,y,w,h
        
        #___Variable Initialization___
        
        self.p = '0'
        self.curdir = '/'
        self.progressstep = 0    
        
        
    #___Initiate group boxes___
    
    def createtopleftgb(self):
        self.topleftgb = ptw.QGroupBox("Create Network")
        
        ex1 = ptw.QPushButton('Create Project')
        ex1.clicked.connect(lambda: self.createnetwork((self.bar,self,'Create Project')))
        ex1.setDefault(True)
        ex2 = ptw.QPushButton('Add Videos')
        ex2.clicked.connect(lambda: self.analyzelabel((self.bar,self,'Add Videos')))
        ex2.setDefault(True)
        ex3 = ptw.QPushButton('Extract Frames')
        ex3.clicked.connect(lambda: self.analyzelabel((self.bar,self,'Extract Frames')))
        ex3.setDefault(True)
        ex4 = ptw.QPushButton('Label Frames')
        ex4.clicked.connect(lambda: self.analyzelabel((self.bar,self,'Label Frames')))
        ex4.setDefault(True)
        
        layout = ptw.QVBoxLayout()
        layout.addWidget(ex1)
        layout.addWidget(ex2)
        layout.addWidget(ex3)
        layout.addWidget(ex4)
        self.topleftgb.setLayout(layout)
    
    def createbotleftgb(self):
        self.botleftgb = ptw.QGroupBox("Train Network")
        
        ex1 = ptw.QPushButton('Create Training Dataset')
        ex1.clicked.connect(lambda: self.analyzelabel((self.bar,self,'Create Training Dataset')))
        ex1.setDefault(True)
        ex2 = ptw.QPushButton('Train Network')
        ex2.clicked.connect(lambda: self.trainnetwork((self.bar,self,'Train Network')))
        ex2.setDefault(True)
        ex3 = ptw.QPushButton('Evaluate Network')
        ex3.clicked.connect(lambda: self.analyzelabel((self.bar,self,'Evaluate Network')))
        ex3.setDefault(True)
        ex4 = ptw.QLabel('')
        
        layout = ptw.QVBoxLayout()
        layout.addWidget(ex1)
        layout.addWidget(ex2)
        layout.addWidget(ex3)
        layout.addWidget(ex4)
        self.botleftgb.setLayout(layout)
        
    def createtoprightgb(self):
        self.toprightgb = ptw.QGroupBox("Process Videos")
        
        ex1 = ptw.QPushButton('Analyze/Label Videos')
        ex1.clicked.connect(lambda: self.analyzelabel((self.bar,self,'Analyze Label')))
        ex1.setDefault(True)
        ex2 = ptw.QPushButton('Extract Outliers')
        ex2.clicked.connect(lambda: self.analyzelabel((self.bar,self,'Extract Outliers')))
        ex2.setDefault(True)
        ex3 = ptw.QPushButton('Refine Labels')
        ex3.clicked.connect(lambda: self.analyzelabel((self.bar,self,'Refine Labels')))
        ex3.setDefault(True)
        ex4 = ptw.QPushButton('Merge Datasets')
        ex4.clicked.connect(lambda: self.analyzelabel((self.bar,self,'Merge Datasets')))
        ex4.setDefault(True)
        
        layout = ptw.QVBoxLayout()
        layout.addWidget(ex1)
        layout.addWidget(ex2)
        layout.addWidget(ex3)
        layout.addWidget(ex4)
        self.toprightgb.setLayout(layout)
        
    def createbotrightgb(self):
        self.botrightgb = ptw.QGroupBox("Results")
        self.botrightgb.setSizePolicy(ptw.QSizePolicy.Preferred,ptw.QSizePolicy.Ignored)
        
        self.table = ptw.QTableWidget(0,1)
        header = self.table.horizontalHeader()       
        header.setSectionResizeMode(0, ptw.QHeaderView.Stretch)
        self.table.setHorizontalHeaderLabels(["Video Link"])
        self.table.setEditTriggers(ptw.QAbstractItemView.NoEditTriggers)
        
        layout = ptw.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.table)
        self.botrightgb.setLayout(layout)
        
        self.table.itemDoubleClicked.connect(self.OpenLink)
    

    
    # ___Button Functions___
    @QtCore.pyqtSlot(int)
    def cleartable(self, nonsense):
        while self.table.rowCount() > 0:
            self.table.removeRow(0)
    
    @QtCore.pyqtSlot(str)
    def settableval(self,newvid):
        rowPosition = self.table.rowCount()
        self.table.insertRow(rowPosition)
        self.table.setItem(self.tabcell,0,ptw.QTableWidgetItem(newvid))
        self.tabcell += 1
    
    
    def getnames(self):
        self.projname, nonsense = ptw.QInputDialog.getText(self,'Create Project','Project name?')
        self.initials, nonsense = ptw.QInputDialog.getText(self,'Create Project','Creator initials?')
    
    def analyzelabel(self,bar):
        self.p = ProcessRunnable(target=run, args=(bar))
        self.p.start()
        
    def createnetwork(self,bar):
        self.getnames()
        self.p = ProcessRunnable(target=run, args=(bar))
        self.p.start()
    
    def trainnetwork(self,bar):
        self.maxiters, nonsense = ptw.QInputDialog.getInt(self,'Train Network',"""Maxiters? (Typically "200000")""")
        self.p = ProcessRunnable(target=run, args=(bar))
        self.p.start()
    
    def disable(self, cond):
        self.topleftgb.setEnabled(cond)
        self.botleftgb.setEnabled(cond)
        self.toprightgb.setEnabled(cond)
    
    @QtCore.pyqtSlot(str)
    def setpercent(self, percent):
        self.progressnum.setText(percent)
    
    def OpenLink(self):
        row = self.table.currentRow()
        column = self.table.currentColumn()
        print(row)
        print(column)
        link = self.table.item(row,column)
        link = link.text()
        print(link)
        subprocess.Popen(["xdg-open",link])
        #use xdg-open for linux
        
    def openhelp(self):
        subprocess.Popen(["xdg-open","/home/spencelab/dlcgui/DLC_Complete_Guide.pdf"])
    
    #__Button Functions__
    def choosedir(self):
        self.curdir = ptw.QFileDialog.getExistingDirectory(self,"Open Directory","/")
        print(self.curdir)
    
    def choosecon(self):
        self.configfile,_ = ptw.QFileDialog.getOpenFileName(self,"Choose Config File",self.curdir)
        print(self.configfile)
        
    def choosevidspar(self):
        if self.filetab.isChecked():
            self.choosevid()
        else:
            self.chooselabeledvidspar()
    
    def chooselabeledvidspar(self):
        if self.settoggle.isChecked():
            self.chooselabeledvids()
        else:
            self.choosevids()
        pass
    
    def chooselabeledvids(self):
        self.vidpaths = []
        dirpaths = []
        folderpath = ptw.QFileDialog.getExistingDirectory(self,"Open Folder",self.curdir)
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
                if vidname[-4:] == '.mp4':
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
        folderpath = ptw.QFileDialog.getExistingDirectory(self,"Open Folder",self.curdir)
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
        print(self.vidpaths)
        lenstr = "Selected " + str(len(self.vidpaths)) + " videos"
        print(lenstr)
    
    def choosevid(self):
        msgBox = ptw.QMessageBox()
        msgBox.setIcon(ptw.QMessageBox.Information)
        msgBox.setText("Click Ok to select more videos")
        msgBox.setWindowTitle("Select Files")
        msgBox.setStandardButtons(ptw.QMessageBox.Ok | ptw.QMessageBox.Cancel)
        
        dirpaths = []
        self.vidpaths=[]
        dirpaths.append(ptw.QFileDialog.getExistingDirectory(self,"Open Folder",self.curdir))
        answer = msgBox.exec()
        while answer == ptw.QMessageBox.Ok:
            self.curdir = self.getparent(dirpaths[-1])
            dirpaths.append(ptw.QFileDialog.getExistingDirectory(self,"Open Folder",self.curdir))
            answer = msgBox.exec()
        else:
            pass
        for paths in dirpaths:
            files = []
            mp4files = []
            for (dirpath, dirnames, filenames) in os.walk(paths):
                files.extend(filenames)
                break
            for vidname in files:
                if vidname[-4:] == '.mp4':
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
        
app = ptw.QApplication(sys.argv)
app.setStyle('macintosh')
ptw.QApplication.setPalette(ptw.QApplication.style().standardPalette())

screen = Window()
screen.show()
screen.raise_()
sys.exit(app.exec_())
