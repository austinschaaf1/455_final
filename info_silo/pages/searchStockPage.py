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
from pages.keywordManagerPage import KEYWORD
import yfinance as yf
import pandas as pd  

class SEARCH_STOCK(QDialog):  # INDEX = 6
    def __init__(self, mySQL, db,widget, user):
        super(SEARCH_STOCK, self).__init__()
        self.mySQL = mySQL
        self.db = db
        self.widget = widget
        self.user = user
        try:
            loadUi("UI\stock_search.ui", self)
        except:
            loadUi("UI/stock_search.ui", self)
        # button clicks
        self.homeButton.clicked.connect(self.gotoWelcome)
        self.addStockButton.clicked.connect(self.addStockToFav)
    def setWidget(self, wid):
        #need to set up in order to get communication working
        self.widget = wid

    def gotoWelcome(self):
        self.success_label.setText("")
        self.EnterTickerInput.clear()
        screen = WELCOME(self.mySQL, self.db, self.widget, self.user)
        self.widget.addWidget(screen)
        self.widget.setCurrentIndex(1)

    def addStockToFav(self):
        # Determine if stock exists or not if it does add it to users interests and give conformation message
        
        userID = self.user[0][0]

        #determine if stock already is in database
        ticker = self.EnterTickerInput.text()
        sql = "SELECT * FROM stock WHERE (ticker LIKE %s)"
        val = (ticker,)
        self.mySQL.execute(sql, val)
        tickerInfo = self.mySQL.fetchall()

        if len(tickerInfo) == 0: #stock not found need to add
            
            message = "Researching " + ticker + " LOADING"
            self.success_label.setText(message)
            self.success_label.setStyleSheet("color:blue;background: none;font-size:25px;font-weight: bold;")

            try: ##attempt to add stock from nasdaq

                ###load stock info
                stockList = [ticker]
                msft = yf.Ticker(stockList[0])
                priceNow = msft.info['regularMarketPrice']
                price = msft.history(start="2022-04-01",end="2022-04-29")

                ###insert stock info into stock page
                sql = "INSERT INTO stock (ticker, current_price) VALUES (%s, %s)"
                val = (stockList[0], priceNow)
                self.mySQL.execute(sql, val)
                self.db.commit()
                
                ###Get the stock closing price and remove unwanted lables by pop
                val = str(price['Close'])
                val = val.split()
                val.pop(0)
                val.pop(len(val)-1)
                val.pop(len(val)-1)
                val.pop(len(val)-1)
                val.pop(len(val)-1)

                ###Populate stock historical data 
                for j in range(0,(len(price)-2),2):
                    sql = "INSERT INTO prices_over_time (ticker, PRICE, date_time) VALUES (%s, %s,%s)"
                    val2 = (stockList[0], val[j+1],val[j])
                    self.mySQL.execute(sql, val2)
                    self.db.commit()

                ##Determine if stock is in users interests already
                sql = "SELECT * FROM user_interest WHERE (stock_ticker LIKE %s) And user_id=%s"
                val = (ticker,userID)
                self.mySQL.execute(sql, val)
                alreadyInterest = self.mySQL.fetchall()

                if len(alreadyInterest) == 0: ###Not in users interests

                    ###Insert stock into users interests
                    sql = "INSERT INTO user_interest (user_id, stock_ticker, interest_type) VALUES (%s, %s, %s)"
                    val = (userID,stockList[0],"STOCK",)
                    self.mySQL.execute(sql, val)
                    self.db.commit()
                    ##success message
                    message = ticker + " succesfully added to your interests"
                    self.success_label.setText(message)
                    self.success_label.setStyleSheet("color:blue;background: none;font-size:25px;font-weight: bold;")
                else: #already in your interests
                    #success message 
                    message = ticker + " is already in your interests"
                    self.success_label.setText(message)
                    self.success_label.setStyleSheet("color:blue;background: none;font-size:25px;font-weight: bold;")
    
            except:###fail message for stock not found
                message = ticker + " not found on NASDAQ"
                self.success_label.setText(message)
                self.success_label.setStyleSheet("color:blue;background: none;font-size:25px;font-weight: bold;")

        else: ##stock is already inside database

            #determine if stock is already in users interests
            sql = "SELECT * FROM user_interest WHERE (stock_ticker LIKE %s) And user_id=%s"
            val = (ticker,userID)
            self.mySQL.execute(sql, val)
            alreadyInterest = self.mySQL.fetchall()

            if len(alreadyInterest) == 0: ##stock not found in users user_interests

                ##insert stock in users interests
                sql = "INSERT INTO user_interest (user_id, stock_ticker, interest_type) VALUES (%s, %s, %s)"
                val = (userID,tickerInfo[0][0],"STOCK",)
                self.mySQL.execute(sql, val)
                self.db.commit()

                ##success message
                message = ticker + " succesfully added to your interests"
                self.success_label.setText(message)
                self.success_label.setStyleSheet("color:blue;background: none;font-size:25px;font-weight: bold;")
            else: ##stock already in users interests 
                message = ticker + " is already in your interests"
                self.success_label.setText(message)
                self.success_label.setStyleSheet("color:blue;background: none;font-size:25px;font-weight: bold;")
        self.EnterTickerInput.clear()