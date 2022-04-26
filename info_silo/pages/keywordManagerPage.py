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
from pages.loginPage import LOGIN
from pages.welcomePage import WELCOME


class KEYWORD(QDialog):  # INDEX = 4
    def __init__(self, mySQL, db, widget):
        super(KEYWORD, self).__init__()
        self.mySQL = mySQL
        self.db = db
        self.widget = widget
        try:
            loadUi("UI\keyword_manager.ui", self)
        except:
            loadUi("UI/keyword_manager.ui", self)
        self.homeButton.clicked.connect(self.gotoWelcome)
        self.loadList()
        self.approveButton.clicked.connect(self.addToDB)

    def setWidget(self, wid):
        # need to set up in order to get communication working
        self.widget = wid

    def gotoWelcome(self):
        screen = WELCOME(self.mySQL, self.db, self.widget)
        self.widget.addWidget(screen)
        self.widget.setCurrentIndex(1)

    def loadList(self):
        sql = "SELECT keyword FROM pending_keyword"
        self.mySQL.execute(sql)
        exists = self.mySQL.fetchall()
        for row in exists:
            self.keywordList.addItem(row[0])

    def addToDB(self):
        keyword_name = self.keywordList.itemClicked()
        sql = "INSERT INTO keyword (keyword_name) VALUES (%s)"
        val = keyword_name
        self.mySQL.execute(sql, val)
