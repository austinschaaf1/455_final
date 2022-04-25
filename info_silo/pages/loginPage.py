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

class LOGIN(QMainWindow):  # INDEX = 0
    def __init__(self, mySQL, db,widget):
        super(LOGIN, self).__init__()
        self.mySQL = mySQL
        self.db = db
        self.widget = widget
        try:
            loadUi("UI\login.ui", self)
        except:
            loadUi("UI/login.ui", self)
        self.loginButton.clicked.connect(self.gotoScreen2)
        self.createAccountButton.clicked.connect(self.gotoCreateAccount)
        # self.keywordManagerButton.clicked.connect(self.gotoKeywordManager)
    def setWidget(self, wid):
        #need to set up in order to get communication working
        self.widget = wid
    def gotoScreen2(self):
        self.widget.setCurrentIndex(1)

    def gotoCreateAccount(self):
        self.widget.setCurrentIndex(3)

    def gotoKeywordManager(self):
        self.widget.setCurrentIndex(4)