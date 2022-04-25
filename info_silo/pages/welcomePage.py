import sys

import pyqtgraph.examples
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QMainWindow
from PyQt5.uic import loadUi
import mysql.connector as mysql

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
from mplwidget import MplWidget
import numpy as np
import random

class WELCOME(QDialog):  # INDEX = 1
    def __init__(self, mySQL, db, widget):
        super(WELCOME, self).__init__()
        self.mySQL = mySQL
        self.db = db
        self.widget = widget
        try:
            loadUi("UI\welcome.ui", self)
        except:
            loadUi("UI/welcome.ui", self)
        self.returnToLogin.clicked.connect(self.gotoScreen2)
        self.compareButton.clicked.connect(self.gotoCompare)
        self.stockSearchButton.clicked.connect(self.goToStockSearch)
        self.keywordSearchButton.clicked.connect(self.goToKeywordSearch)
    def setWidget(self, wid):
        #need to set up in order to get communication working
        self.widget = wid

    def gotoScreen2(self):
        screen = WELCOME(self.mySQL, self.db,self.widget)
        self.widget.addWidget(screen)
        self.widget.setCurrentIndex(0)

    def gotoCompare(self):
        screen = WELCOME(self.mySQL, self.db,self.widget)
        self.widget.addWidget(screen)
        self.widget.setCurrentIndex(2)

    def goToStockSearch(self):
        screen = WELCOME(self.mySQL, self.db,self.widget)
        self.widget.addWidget(screen)
        self.widget.setCurrentIndex(6)

    def goToKeywordSearch(self):
        screen = WELCOME(self.mySQL, self.db,self.widget)
        self.widget.addWidget(screen)
        self.widget.setCurrentIndex(5)