import sys

import pyqtgraph.examples
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QMainWindow, QTableWidgetItem, QMessageBox
from PyQt5.uic import loadUi
import mysql.connector as mysql
from PyQt5.uic.properties import QtGui

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
from mplwidget import MplWidget
import numpy as np
import random


class WELCOME(QDialog):  # INDEX = 1

    def __init__(self, mySQL, db, widget, user):
        super(WELCOME, self).__init__()
        self.mySQL = mySQL
        self.db = db
        self.widget = widget
        self.user = user
        try:
            loadUi("UI\welcome.ui", self)
        except:
            loadUi("UI/welcome.ui", self)
        self.returnToLogin.clicked.connect(self.gotoScreen2)
        self.compareButton.clicked.connect(self.gotoCompare)
        self.stockSearchButton.clicked.connect(self.goToStockSearch)
        self.keywordSearchButton.clicked.connect(self.goToKeywordSearch)
        self.loadButton.clicked.connect(self.loadTables)

    def setWidget(self, wid):
        # need to set up in order to get communication working
        self.widget = wid

    def gotoScreen2(self):
        if len(self.user) > 0:
            self.user.clear()
            self.stocksTable.setRowCount(0)
            self.keywordsTable.setRowCount(0)
        screen = WELCOME(self.mySQL, self.db, self.widget, self.user)
        self.widget.addWidget(screen)
        self.widget.setCurrentIndex(0)

    def gotoCompare(self):
        screen = WELCOME(self.mySQL, self.db, self.widget, self.user)
        self.widget.addWidget(screen)
        self.widget.setCurrentIndex(2)

    def goToStockSearch(self):
        screen = WELCOME(self.mySQL, self.db, self.widget, self.user)
        self.widget.addWidget(screen)
        self.widget.setCurrentIndex(6)

    def goToKeywordSearch(self):
        screen = WELCOME(self.mySQL, self.db, self.widget, self.user)
        self.widget.addWidget(screen)
        self.widget.setCurrentIndex(5)

    def loadStocksTable(self):
        sql = "SELECT user_interest.stock_ticker, s.current_price, PRICE, " \
              "ROUND(SUM(current_price-pot.PRICE),2), stockCount " \
              "FROM (SELECT COUNT(user_id) as stockCount " \
              "FROM user_interest WHERE user_id = %s AND interest_type = 'STOCK' ) as uiC, user_interest " \
              "JOIN user_data ud on ud.user_id = user_interest.user_id " \
              "JOIN stock s on s.ticker = user_interest.stock_ticker " \
              "JOIN prices_over_time pot on s.ticker = pot.ticker " \
              "WHERE ud.user_id = %s AND user_interest.interest_type = 'STOCK' " \
              "group by s.current_price, user_interest.stock_ticker, PRICE, date_time order by date_time desc;"
        val = (self.user[0][0], self.user[0][0])
        self.mySQL.execute(sql, val)
        exists = self.mySQL.fetchall()
        counter = 0
        for row in exists:
            rowPosition = self.stocksTable.rowCount()
            self.stocksTable.insertRow(rowPosition)
            self.stocksTable.setItem(rowPosition, 0, QTableWidgetItem(row[0]))
            self.stocksTable.setItem(rowPosition, 1, QTableWidgetItem(str(row[1])))
            self.stocksTable.setItem(rowPosition, 2, QTableWidgetItem(str(row[3])))
            counter += 1
            if counter == row[4]:
                break

    def loadKeywordTable(self):
        sql = "SELECT k.keyword_name, SUM(sot.number_of_searches) FROM user_interest " \
              "JOIN user_data ud on ud.user_id = user_interest.user_id " \
              "JOIN keyword k on k.keyword_dbkey = user_interest.keyword_key " \
              "JOIN searches_over_time sot on k.keyword_dbkey = sot.keyword " \
              "WHERE ud.user_id = %s AND user_interest.interest_type = 'KEY' GROUP BY k.keyword_name;"
        val = (self.user[0][0],)
        self.mySQL.execute(sql, val)
        exists = self.mySQL.fetchall()
        for row in exists:
            rowPosition = self.keywordsTable.rowCount()
            self.keywordsTable.insertRow(rowPosition)
            self.keywordsTable.setItem(rowPosition, 0, QTableWidgetItem(row[0]))
            self.keywordsTable.setItem(rowPosition, 1, QTableWidgetItem(str(row[1])))

    def loadTables(self):
        self.stocksTable.setRowCount(0)
        self.keywordsTable.setRowCount(0)
        self.loadStocksTable()
        self.loadKeywordTable()
