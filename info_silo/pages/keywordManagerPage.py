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
from pytrends.request import TrendReq
import pandas as pd   
from datetime import date, timedelta


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
        self.rejectButton.clicked.connect(self.deleteRow)

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
    def deleteRow(self):
        addKeyWordInput = self.keywordList.currentItem()
        itemName = addKeyWordInput.text()
        index = self.keywordList.currentRow()
        sql = "DELETE FROM pending_keyword WHERE keyword=%s"
        val = (itemName,)
        self.mySQL.execute(sql, val)
        self.db.commit()
        self.keywordList.takeItem(index)

    def addToDB(self):
        addKeyWordInput = self.keywordList.currentItem()
        sql = "SELECT * FROM keyword WHERE (keyword_name LIKE %s)"
        val = (addKeyWordInput.text(),)
        self.mySQL.execute(sql, val)
        keywordInfo = self.mySQL.fetchall()
        if len(keywordInfo) == 0:
            sql = "INSERT INTO keyword (keyword_name) VALUES (%s)"
            val = (addKeyWordInput.text(),)
            self.mySQL.execute(sql, val)
            self.db.commit()

            sql = "SELECT * FROM keyword WHERE (keyword_name LIKE %s)"
            val = (addKeyWordInput.text(),)
            self.mySQL.execute(sql, val)
            keywordInfo = self.mySQL.fetchall()

            pytrend = TrendReq()
            data1 = []
            data1.append(keywordInfo[0][1])
            list1 = pytrend.get_historical_interest(data1, year_start=2022, month_start=1, day_start=1, hour_start=0, year_end=2022, month_end=2, day_end=1, hour_end=0, cat=0, geo='', gprop='', sleep=0)
            my_date = date(2022, 1, 1)
            for i in range(30):

                my_date += timedelta(days=1)
            
                sql = "INSERT INTO searches_over_time (keyword,number_of_searches,date_time) VALUES (%s,%s,%s)"
                val = (keywordInfo[0][0],list1.values[i][0],my_date,)
                self.mySQL.execute(sql, val)
                self.db.commit()

            self.deleteRow()
