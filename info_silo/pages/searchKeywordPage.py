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
from datetime import date
from pprint import pprint


class SEARCH_KEYWORD(QDialog):  # INDEX = 5
    def __init__(self, mySQL, db, widget):
        super(SEARCH_KEYWORD, self).__init__()
        self.mySQL = mySQL
        self.db = db
        self.widget = widget
        try:
            loadUi("UI\keyword_search.ui", self)
        except:
            loadUi("UI/keyword_search.ui", self)
        # button clicks
        self.goToKeywordManagerButton.clicked.connect(self.goToManager)
        self.homeButton.clicked.connect(self.gotoWelcome)
        self.addKeywordButton.clicked.connect(self.addKeywordToFav)
        self.requestKeywordButton.clicked.connect(self.requestKeyword)

    def setWidget(self, wid):
        # need to set up in order to get communication working
        self.widget = wid

    def goToManager(self):
        # Return to the keyword manager
        screen = KEYWORD(self.mySQL, self.db, self.widget)
        self.widget.addWidget(screen)
        self.widget.setCurrentIndex(4)

    def gotoWelcome(self):
        screen = KEYWORD(self.mySQL, self.db, self.widget)
        self.widget.addWidget(screen)
        self.widget.setCurrentIndex(1)
        

    def addKeywordToFav(self):
        # Determine if keyword exists or not if it does add it to users interests and give conformation message
        ###SQL needed
        ## if select is not null
        ##  SELECT * FROM keyword WHERE (keyword_name LIKE %userSearch%);
        ##  INSERT INTO user_interest (user_interest_id, search_word_id, interest_type) VALUES (userID, keywordID, interestType);
        addKeyWordInput = self.enterKeywordInput.text()
        sql = "SELECT * FROM keyword WHERE (keyword_name LIKE %s)"
        val = (addKeyWordInput,)
        self.mySQL.execute(sql, val)
        keywordInfo = self.mySQL.fetchall()
        if len(keywordInfo) == 0:
            ##Keyword not found in database
            print("miss")
            pass
        else:
            ###keyword found in database
            ########need to change to have User ID
            userID = 5 ######Chris Change
            sql = "SELECT * FROM user_interest WHERE user_id=%s AND keyword_key=%s"
            val = (userID,keywordInfo[0][0],)
            self.mySQL.execute(sql, val)
            userInterestMatch = self.mySQL.fetchall()
            if len(userInterestMatch) == 0:
                #keyword not in user_interests
                sql = "INSERT INTO user_interest (user_id, keyword_key, interest_type) VALUES (%s, %s, %s)"
                val = (userID,keywordInfo[0][0],"KEY",)
                self.mySQL.execute(sql, val)
                self.db.commit()
                #need to add success message
            else:
                #need to add fail message
                pass
            
            
            
        

        

    def requestKeyword(self):
        # Determine if keyword exists if it does not add it to keyword managers list and give conformation message
        ###SQL needed examples
        # If select is null
        ##  SELECT * FROM keyword WHERE (keyword_name LIKE %userSearch%);
        ##  INSERT INTO pending_keyword (keyword, date_requested) VALUES (pendKeyword, currentDate);
        requestKeyWordInput = self.requestKeywordInput.text()
        sql = "SELECT * FROM keyword WHERE (keyword_name LIKE %s)"
        val = (requestKeyWordInput,)
        self.mySQL.execute(sql, val)
        keywordInfo = self.mySQL.fetchall()
        if len(keywordInfo) == 0:
            ##Keyword not found in database Send it to the keyword manager
            requestKeyWordInput = self.requestKeywordInput.text()
            sql = "SELECT * FROM pending_keyword WHERE (keyword LIKE %s)"
            val = (requestKeyWordInput,)
            self.mySQL.execute(sql, val)
            keywordMangerInfo = self.mySQL.fetchall()
            if len(keywordMangerInfo) == 0:
                sql = "INSERT INTO pending_keyword (keyword, date_requested) VALUES (%s, %s)"
                val = (requestKeyWordInput,date.today(),)
                self.mySQL.execute(sql, val)
                self.db.commit()
            
            pass
        else:
            ###keyword found in database
            ########need to change to have User ID
            userID = 5 ######Chris Change
            sql = "SELECT * FROM user_interest WHERE user_id=%s AND keyword_key=%s"
            val = (userID,keywordInfo[0][0],)
            self.mySQL.execute(sql, val)
            userInterestMatch = self.mySQL.fetchall()
            if len(userInterestMatch) == 0:
                #keyword not in user_interests
                sql = "INSERT INTO user_interest (user_id, keyword_key, interest_type) VALUES (%s, %s, %s)"
                val = (userID,keywordInfo[0][0],"KEY",)
                self.mySQL.execute(sql, val)
                self.db.commit()
                #need to add success message
            else:
                #need to add fail message
                pass
        pass
