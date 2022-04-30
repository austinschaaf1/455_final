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
    def __init__(self, mySQL, db, widget, user):
        super(KEYWORD, self).__init__()
        self.mySQL = mySQL
        self.db = db
        self.widget = widget
        self.user = user
        try:
            loadUi("UI\keyword_manager.ui", self)
        except:
            loadUi("UI/keyword_manager.ui", self)
        self.homeButton.clicked.connect(self.gotoWelcome)
        self.loadList()
        self.approveButton.clicked.connect(self.addToDB)
        self.rejectButton.clicked.connect(self.deleteRow)
        self.reloadListB.clicked.connect(self.reloadList)

    def setWidget(self, wid):
        # need to set up in order to get communication working
        self.widget = wid

    def gotoWelcome(self):
        screen = WELCOME(self.mySQL, self.db, self.widget, self.user)
        self.widget.addWidget(screen)
        self.widget.setCurrentIndex(1)

    def loadList(self):
        ###pull in the list from database
        sql = "SELECT keyword FROM pending_keyword"
        self.mySQL.execute(sql)
        exists = self.mySQL.fetchall()
        for row in exists:
            self.keywordList.addItem(row[0])
    
    def reloadList(self):
        ###clears the whole list then rebuilds it
        self.keywordList.clear()
        self.loadList()
        message = "List has been reloaded!"
        self.success_label.setText(message)
        self.success_label.setStyleSheet("color:blue;background: none;font-size:25px;font-weight: bold;")
        
    def deleteRow(self,delete=True):
        ### Delete a single item from the pending keyword table

        addKeyWordInput = self.keywordList.currentItem()
        itemName = addKeyWordInput.text()
        index = self.keywordList.currentRow()
        sql = "DELETE FROM pending_keyword WHERE keyword=%s"
        val = (itemName,)
        self.mySQL.execute(sql, val)
        self.db.commit()
        self.keywordList.takeItem(index)
        
        ##If comming in from the reject button display a message
        if delete == False:
            message = itemName + " has been deleted from list!"
            self.success_label.setText(message)
            self.success_label.setStyleSheet("color:blue;background: none;font-size:25px;font-weight: bold;")

    def addToDB(self):
        ###add the new keyword to the database and search for it

        addKeyWordInput = self.keywordList.currentItem()
        sql = "SELECT * FROM keyword WHERE (keyword_name LIKE %s)"
        val = (addKeyWordInput.text(),)
        self.mySQL.execute(sql, val)
        keywordInfo = self.mySQL.fetchall()

        if len(keywordInfo) == 0:   ##Keyword not found in database add it

            ####Insert the keyword into the keyword table
            sql = "INSERT INTO keyword (keyword_name) VALUES (%s)"
            val = (addKeyWordInput.text(),)
            self.mySQL.execute(sql, val)
            self.db.commit()

            ##### Get the Keyword dbkey
            sql = "SELECT * FROM keyword WHERE (keyword_name LIKE %s)"
            val = (addKeyWordInput.text(),)
            self.mySQL.execute(sql, val)
            keywordInfo = self.mySQL.fetchall()

            ####Load a month worth of searches
            pytrend = TrendReq()
            data1 = []
            data1.append(keywordInfo[0][1])
            list1 = pytrend.get_historical_interest(data1, year_start=2022, month_start=4, day_start=1, hour_start=0, year_end=2022, month_end=4, day_end=29, hour_end=0, cat=0, geo='', gprop='', sleep=0)
            my_date = date(2022, 4, 1)

            for i in range(30):
                ####Add a month worth of searches 
                my_date += timedelta(days=1)
                sql = "INSERT INTO searches_over_time (keyword,number_of_searches,date_time) VALUES (%s,%s,%s)"
                val = (keywordInfo[0][0],list1.values[i][0],my_date,)
                self.mySQL.execute(sql, val)
                self.db.commit()

            ######Display success message for databases   
            message = addKeyWordInput.text() + " has been added to the database!"
            self.success_label.setText(message)
            self.success_label.setStyleSheet("color:blue;background: none;font-size:25px;font-weight: bold;")
            self.deleteRow(True)
