#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 10:40:14 2022

@author: bradleyrauscher
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import time
        
class App(QWidget):
    def __init__(self):
        super().__init__()
        
        self.init_ui()

    def init_ui(self):
        submit = QPushButton('Submit', self)
        submit2 = QPushButton('Submit2', self)
        
        grid = QGridLayout()
        grid.addWidget(submit, 1, 0)
        grid.addWidget(submit2,1,1)

        self.setLayout(grid)
        self.resize(350, 250)
        self.setWindowTitle('GetMeStuff Bot v0.1')
        self.show()
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = App()
    widget.raise_()
    sys.exit(app.exec_())