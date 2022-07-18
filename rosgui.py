#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 17:09:41 2022

@author: bradleyrauscher
"""

import PyQt5.QtWidgets as ptw
from PyQt5.QtWidgets import QFrame
import sys
import subprocess
import time

xoffset = 350
yoffset = 200
winwidth = 500
winheight = 450

class Window(ptw.QMainWindow):
    def __init__(self, parent = None):
        super(Window, self).__init__(parent)
        
        styleComboBox = ptw.QComboBox()
        styleComboBox.addItems(ptw.QStyleFactory.keys())
        
        widget = ptw.QWidget()
        
        choosedir = ptw.QPushButton('Directory')
        choosedir.setDefault(True)
        choosecon = ptw.QPushButton('Config File')
        choosecon.setDefault(True)
        choosevids = ptw.QPushButton('Videos')
        choosevids.setDefault(True)
        
        self.createtopleftgb()
        self.createbotleftgb()
        self.createtoprightgb()
        self.createbotrightgb()
        self.createprogressbar()
        
        toplayout = ptw.QHBoxLayout()
        toplayout.addWidget(choosedir)
        toplayout.addWidget(choosecon)
        toplayout.addWidget(choosevids)
        
        mainlayout = ptw.QGridLayout()
        mainlayout.addLayout(toplayout,0,0,1,2)
        mainlayout.addWidget(self.topleftgb,1,0)
        mainlayout.addWidget(self.botleftgb,2,0)
        mainlayout.addWidget(self.toprightgb,1,1)
        mainlayout.addWidget(self.botrightgb,2,1)
        mainlayout.addWidget(self.progressbar,3,0,1,2)
        widget.setLayout(mainlayout)
        
        self.setCentralWidget(widget)
        
        self.setWindowTitle = "DLC Operator"
        self.setGeometry(xoffset,yoffset,winwidth,winheight) #x,y,w,h
        
        
    def createtopleftgb(self):
        self.topleftgb = ptw.QGroupBox("Group 1")
        
        ex1 = ptw.QPushButton('ex1')
        ex1.setDefault(True)
        ex2 = ptw.QPushButton('ex2')
        ex2.setDefault(True)
        ex3 = ptw.QPushButton('ex3')
        ex3.setDefault(True)
        ex4 = ptw.QPushButton('ex4')
        ex4.setDefault(True)
        
        layout = ptw.QVBoxLayout()
        layout.addWidget(ex1)
        layout.addWidget(ex2)
        layout.addWidget(ex3)
        layout.addWidget(ex4)
        self.topleftgb.setLayout(layout)
    
    def createbotleftgb(self):
        self.botleftgb = ptw.QGroupBox("Group 2")
        
        ex1 = ptw.QPushButton('ex1')
        ex1.setDefault(True)
        ex2 = ptw.QPushButton('ex2')
        ex2.setDefault(True)
        ex3 = ptw.QPushButton('ex3')
        ex3.setDefault(True)
        ex4 = ptw.QLabel('')
        
        layout = ptw.QVBoxLayout()
        layout.addWidget(ex1)
        layout.addWidget(ex2)
        layout.addWidget(ex3)
        layout.addWidget(ex4)
        self.botleftgb.setLayout(layout)
        
    def createtoprightgb(self):
        self.toprightgb = ptw.QGroupBox("Group 3")
    
    def createbotrightgb(self):
        self.botrightgb = ptw.QGroupBox("Group 4")
    
    def createprogressbar(self):
        self.progressbar = ptw.QProgressBar()
        self.progressbar.setRange(0, 10)
        self.progressbar.setValue(0)
    
    def onClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            print("Country is %s" % (radioButton.country))
    
    def buttonclick(self):
        print("Success!")
    
    def openFileNameDialog(self):
        filenameex,_ = ptw.QFileDialog.getOpenFileName(self,"Open File","/Users/bradleyrauscher/Documents/BostonU")
        print(filenameex)
        
    def runfile(self):
        file = "extscript.py"
        self.p = subprocess.Popen(["python3",file,"5"])
        
    def checkrun(self):
        poll = self.p.poll()
        if poll is None:
            print("not finished")
        else:
            print("finished")
    
    def openpdf(self):
        file = "DLC_Complete_Guide.pdf"
        subprocess.Popen(["open",file])

app = ptw.QApplication(sys.argv)
app.setStyle('macintosh')
ptw.QApplication.setPalette(ptw.QApplication.style().standardPalette())

screen = Window()
screen.show()
screen.raise_()
sys.exit(app.exec_())