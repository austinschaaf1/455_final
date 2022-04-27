import sys

import pyqtgraph.examples
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QMainWindow, QTableWidgetItem
from PyQt5.uic import loadUi
import mysql.connector as mysql
from PyQt5.uic.properties import QtGui

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
from mplwidget import MplWidget
import numpy as np
import random


class WELCOME(QDialog):  # INDEX = 1
    keywordSelected = None
    stockSelected = None

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
        self.loadStocksTable()
        self.loadKeywordTable()


    def setWidget(self, wid):
        # need to set up in order to get communication working
        self.widget = wid

    def gotoScreen2(self):
        screen = WELCOME(self.mySQL, self.db, self.widget)
        self.widget.addWidget(screen)
        self.widget.setCurrentIndex(0)

    def gotoCompare(self):
        screen = WELCOME(self.mySQL, self.db, self.widget)
        self.widget.addWidget(screen)
        self.widget.setCurrentIndex(2)

    def goToStockSearch(self):
        screen = WELCOME(self.mySQL, self.db, self.widget)
        self.widget.addWidget(screen)
        self.widget.setCurrentIndex(6)

    def goToKeywordSearch(self):
        screen = WELCOME(self.mySQL, self.db, self.widget)
        self.widget.addWidget(screen)
        self.widget.setCurrentIndex(5)

    def loadStocksTable(self):
        sql = "SELECT * FROM stock"
        self.mySQL.execute(sql)
        exists = self.mySQL.fetchall()
        for row in exists:
            rowPosition = self.stocksTable.rowCount()
            self.stocksTable.insertRow(rowPosition)
            self.stocksTable.setItem(rowPosition, 0, QTableWidgetItem(row[0]))
            self.stocksTable.setItem(rowPosition, 1, QTableWidgetItem(str(row[1])))

    def loadKeywordTable(self):
        sql = "SELECT keyword.keyword_name, SUM(sot.number_of_searches)" \
              " FROM keyword JOIN searches_over_time sot on keyword.keyword_dbkey = sot.keyword " \
              "GROUP BY keyword.keyword_name"
        self.mySQL.execute(sql)
        exists = self.mySQL.fetchall()
        for row in exists:
            rowPosition = self.keywordsTable.rowCount()
            self.keywordsTable.insertRow(rowPosition)
            self.keywordsTable.setItem(rowPosition, 0, QTableWidgetItem(row[0]))
            self.keywordsTable.setItem(rowPosition, 1, QTableWidgetItem(str(row[1])))

