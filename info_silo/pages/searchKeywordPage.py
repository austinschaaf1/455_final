import sys

import pyqtgraph.examples
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
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
    def __init__(self, mySQL, db, widget, user):
        super(SEARCH_KEYWORD, self).__init__()
        self.mySQL = mySQL
        self.db = db
        self.widget = widget
        self.user = user
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
        sql = "SELECT * FROM keyword_manager WHERE user_info= %s"
        try:
            val = (self.user[0][0],)
            self.mySQL.execute(sql, val)
            isManager = self.mySQL.fetchall()

            if len(isManager) > 0:
                self.success_label.setText("")
                screen = KEYWORD(self.mySQL, self.db, self.widget, self.user)
                self.widget.addWidget(screen)
                self.widget.setCurrentIndex(4)
            else:
                message = "You must be a keyword manager to access this page!"
                self.success_label.setText(message)
                self.success_label.setStyleSheet("color:blue;background: none;font-size:25px;font-weight: bold;")
                # QTimer(self).connect(self.success_label.setText("TEST"))
                # QTimer.start(1000)
        except:
            pass


    def gotoWelcome(self):
        self.success_label.setText("")
        screen = KEYWORD(self.mySQL, self.db, self.widget, self.user)
        self.widget.addWidget(screen)
        self.widget.setCurrentIndex(1)
        

    def addKeywordToFav(self):
        ##adds a user selected keyword to the database if it is found

        ##determine if keyword is in the database
        addKeyWordInput = self.enterKeywordInput.text()
        sql = "SELECT * FROM keyword WHERE (keyword_name LIKE %s)"
        val = (addKeyWordInput,)
        self.mySQL.execute(sql, val)
        keywordInfo = self.mySQL.fetchall()

        if len(keywordInfo) == 0:
            ##Keyword not found in database
            message = addKeyWordInput + " not in Database try Request"
            self.success_label.setText(message)
            self.success_label.setStyleSheet("color:blue;background: none;font-size:25px;font-weight: bold;")
            pass
        else:
            ###keyword found in database
            ########need to change to have User ID

            userID = self.user[0][0]

            ###Determine if keyword exists inside the users interests so its not readded
            sql = "SELECT * FROM user_interest WHERE user_id=%s AND keyword_key=%s"
            val = (userID,keywordInfo[0][0],)
            self.mySQL.execute(sql, val)
            userInterestMatch = self.mySQL.fetchall()

            if len(userInterestMatch) == 0: #keyword not in user_interests
                
                ##Insert the keyword into user interests
                sql = "INSERT INTO user_interest (user_id, keyword_key, interest_type) VALUES (%s, %s, %s)"
                val = (userID,keywordInfo[0][0],"KEY",)
                self.mySQL.execute(sql, val)
                self.db.commit()
                message = addKeyWordInput + " added to your interests!"
                self.success_label.setText(message)
                self.success_label.setStyleSheet("color:blue;background: none;font-size:25px;font-weight: bold;")

            else: #keyword is already in users interests
                message = addKeyWordInput + " is already in your interests!"
                self.success_label.setText(message)
                self.success_label.setStyleSheet("color:blue;background: none;font-size:25px;font-weight: bold;")
        
    def requestKeyword(self):
        ####Adds the keyword to the keyword manager page
        ########need to change to have User ID
        userID = self.user[0][0]

        #determine if membership level is high enough
        sql = "SELECT * FROM user_data WHERE user_id=%s"
        val = (userID,)
        self.mySQL.execute(sql, val)
        userinfo = self.mySQL.fetchall()
        
        if(userinfo[0][3] == 5):
            ##determine if keyword is inside the keyword table
            requestKeyWordInput = self.requestKeywordInput.text()
            sql = "SELECT * FROM keyword WHERE (keyword_name LIKE %s)"
            val = (requestKeyWordInput,)
            self.mySQL.execute(sql, val)
            keywordInfo = self.mySQL.fetchall()

            if len(keywordInfo) == 0: ##Keyword not found in database Send it to the keyword manager
                
                ###Determine if the keyword is not already in the keyword manager table
                requestKeyWordInput = self.requestKeywordInput.text()
                sql = "SELECT * FROM pending_keyword WHERE (keyword LIKE %s)"
                val = (requestKeyWordInput,)
                self.mySQL.execute(sql, val)
                keywordMangerInfo = self.mySQL.fetchall()

                if len(keywordMangerInfo) == 0: ##### keyword not in the keyword manager table
                    sql = "INSERT INTO pending_keyword (keyword, date_requested) VALUES (%s, %s)"
                    val = (requestKeyWordInput,date.today(),)
                    self.mySQL.execute(sql, val)
                    self.db.commit()

                ##Success message
                message = requestKeyWordInput + " has been sent to keyword manager!"
                self.success_label.setText(message)
                self.success_label.setStyleSheet("color:blue;background: none;font-size:25px;font-weight: bold;")
            else:
                ###keyword found in database


                ###Determine if the keyword is in the users interests already
                sql = "SELECT * FROM user_interest WHERE user_id=%s AND keyword_key=%s"
                val = (userID,keywordInfo[0][0],)
                self.mySQL.execute(sql, val)
                userInterestMatch = self.mySQL.fetchall()

                if len(userInterestMatch) == 0: #keyword not in user_interests
                    
                    ######Add the keyword to the users interests
                    sql = "INSERT INTO user_interest (user_id, keyword_key, interest_type) VALUES (%s, %s, %s)"
                    val = (userID,keywordInfo[0][0],"KEY",)
                    self.mySQL.execute(sql, val)
                    self.db.commit()

                    ###success message
                    message = requestKeyWordInput + " has been added to your interests!"
                    self.success_label.setText(message)
                    self.success_label.setStyleSheet("color:blue;background: none;font-size:25px;font-weight: bold;")
                    
                else: ###user already has requested keyword
                    
                    message = requestKeyWordInput + " is already in your interests!"
                    self.success_label.setText(message)
                    self.success_label.setStyleSheet("color:blue;background: none;font-size:25px;font-weight: bold;")
        else: ###not high enough membership Level
            message = "Please purchase paid version to request keyword"
            self.success_label.setText(message)
            self.success_label.setStyleSheet("color:blue;background: none;font-size:25px;font-weight: bold;")
