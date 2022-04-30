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


class COMPARE(QDialog):  # INDEX = 2
    def __init__(self, mySQL, db, widget, user):
        super(COMPARE, self).__init__()
        self.mySQL = mySQL
        self.db = db
        self.widget = widget
        self.user = user
        try:
            loadUi("UI\compare.ui", self)
        except:
            loadUi("UI/compare.ui", self)
        self.backToList.clicked.connect(self.gotoWelcome)
        # self.update_graph()
        self.loadStocksList()
        self.loadKeywordList()
        self.refreshButton.clicked.connect(self.refreshLists)
        self.stocksList.itemClicked.connect(self.update_graph)
        self.keywordsList.itemClicked.connect(self.update_graph)

    def setWidget(self, wid):
        # need to set up in order to get communication working
        self.widget = wid

    def gotoWelcome(self):
        screen = COMPARE(self.mySQL, self.db, self.widget, self.user)
        self.widget.addWidget(screen)
        self.widget.setCurrentIndex(1)

    def update_graph(self):

        if (self.keywordsList.currentItem() is not None) and (self.stocksList.currentItem() is not None):
            x1 = ([1, 2, 3, 4, 5])
            x2 = ([1, 2, 3, 4, 5])
            y1 = []
            y2 = []

            # Keyword Searches
            sql = "SELECT k.keyword_name, searches_over_time.number_of_searches FROM searches_over_time" \
                  " JOIN keyword k on k.keyword_dbkey = searches_over_time.keyword " \
                  "WHERE k.keyword_name = %s ORDER BY date_time DESC LIMIT 5;"
            val = (self.keywordsList.currentItem().text(),)
            self.mySQL.execute(sql, val)
            exists = self.mySQL.fetchall()
            for row in exists:
                y2.insert(0, row[1])

            # Stock Prices
            sql = "SELECT stock.ticker, pot.PRICE, stock.current_price FROM stock " \
                  "JOIN prices_over_time pot on stock.ticker = pot.ticker " \
                  "WHERE stock.ticker = %s ORDER BY date_time DESC LIMIT 5;"
            val = (self.stocksList.currentItem().text(),)
            self.mySQL.execute(sql, val)
            exists = self.mySQL.fetchall()
            for row in exists:
                y1.insert(0, row[1])

            self.MplWidget.canvas.axes.clear()
            self.MplWidget.canvas.ax2.clear()
            stocksLine = self.MplWidget.canvas.axes.plot(x1, y1, label=self.stocksList.currentItem().text(),
                                                         color='blue')
            keywordsLine = self.MplWidget.canvas.ax2.plot(x2, y2, label=self.keywordsList.currentItem().text(),
                                                          color='orange')
            lns = stocksLine + keywordsLine
            labs = [line.get_label() for line in lns]
            self.MplWidget.canvas.axes.legend(lns, labs, loc='upper left')
            self.MplWidget.canvas.axes.set_ylabel("Stock Price ($ USD)")
            self.MplWidget.canvas.axes.set_xlabel("Last 5 Days")
            self.MplWidget.canvas.axes.set_title("Stock Price VS Keyword Searches")
            self.MplWidget.canvas.ax2.set_ylabel("Keyword (Number of Searches)")
            self.MplWidget.canvas.draw()

    def loadStocksList(self):
        self.stocksList.clear()
        sql = "SELECT * FROM stock"
        self.mySQL.execute(sql)
        exists = self.mySQL.fetchall()
        for row in exists:
            self.stocksList.addItem(row[0])

    def loadKeywordList(self):
        self.keywordsList.clear()
        sql = "SELECT keyword_name FROM keyword"
        self.mySQL.execute(sql)
        exists = self.mySQL.fetchall()
        for row in exists:
            self.keywordsList.addItem(row[0])

    def refreshLists(self):
        self.loadKeywordList()
        self.loadStocksList()
