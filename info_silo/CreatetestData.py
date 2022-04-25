##CSCI 455 Final
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

from pages.comparePage import COMPARE
from pages.createAccountPage import CREATE
from pages.keywordManagerPage import KEYWORD
from pages.loginPage import LOGIN
from pages.searchKeywordPage import SEARCH_KEYWORD
from pages.searchStockPage import SEARCH_STOCK
from pages.welcomePage import WELCOME
import pandas as pd                         
from pytrends.request import TrendReq
from datetime import date, timedelta
import yfinance as yf


HOST = "cs455project.csuy1zz16lbb.us-east-1.rds.amazonaws.com"
DATABASE = "455 Project"
USER = "admin"
PASSWORD = "FLBbA3YWrg7PKA5"
db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
mySQL = db_connection.cursor()
print("Connected to: ", db_connection.get_server_info())
def createKeyword(mydb, mycursor):
    pytrend = TrendReq()
    pytrend.build_payload(kw_list=["Taylor Swift"])
    # Interest by Region
    kw_list = ["Blockchain","snowmobile","apple","hunting","sql","answer","obtainable","conscious","gleaming","business","forlese","whole","feet","mac"]
    for i in range(len(kw_list)):
        mycursor = mydb.cursor()

        sql = "INSERT INTO keyword (keyword_name) VALUES (%s)"
        val = (kw_list[i],)
        mycursor.execute(sql, val)
        mydb.commit()

    sql = "SELECT * FROM keyword"
    mycursor.execute(sql)
    keyword_data = mycursor.fetchall()
    for j in range(len(keyword_data)):
        data1 = []
        data1.append(keyword_data[j][1])
        list1 = pytrend.get_historical_interest(data1, year_start=2022, month_start=1, day_start=1, hour_start=0, year_end=2022, month_end=2, day_end=1, hour_end=0, cat=0, geo='', gprop='', sleep=0)
        my_date = date(2022, 1, 1)
        for i in range(30):
            my_date += timedelta(days=1)
           
            sql = "INSERT INTO searches_over_time (keyword,number_of_searches,date_time) VALUES (%s,%s,%s)"
            val = (keyword_data[j][0],list1.values[i][0],my_date,)
            mycursor.execute(sql, val)
            mydb.commit()

def createStock(mydb, mycursor):
    stockList = ["TSLA","GOOGL","AMZN","TSM","NVDA","UNH","PG","CNI","BAC","KO"]
    for i in range(len(stockList)):
        msft = yf.Ticker(stockList[i])
        priceNow = msft.info['regularMarketPrice']
        mycursor = mydb.cursor()
        sql = "INSERT INTO stock (ticker, current_price) VALUES (%s, %s)"
        val = (stockList[i], priceNow)

        mycursor.execute(sql, val)
        mydb.commit()
        price = msft.history(start="2022-01-01",end="2022-01-29")

        val = str(price['Close'])
        val = val.split()
        val.pop(0)
        val.pop(len(val)-1)
        val.pop(len(val)-1)
        val.pop(len(val)-1)
        val.pop(len(val)-1)
        for j in range(0,(len(price)-2),2):
            sql = "INSERT INTO prices_over_time (ticker, PRICE, date_time) VALUES (%s, %s,%s)"
            val2 = (stockList[i], val[j+1],val[j])

            mycursor.execute(sql, val2)
            mydb.commit()


def createUsers(mydb, mycursor):
    for i in range(20):
        mycursor = mydb.cursor()

        sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
        val = ("John", "Highway 21")
        mycursor.execute(sql, val)

#createUsers(db_connection,mySQL)
#createKeyword(db_connection,mySQL)
#createStock(db_connection,mySQL)