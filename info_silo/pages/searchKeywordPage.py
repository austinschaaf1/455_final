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

class SEARCH_KEYWORD(QDialog):  # INDEX = 5
    def __init__(self, mySQL, db,widget):
        super(SEARCH_KEYWORD, self).__init__()
        self.mySQL = mySQL
        self.db = db
        self.widget = widget
        try:
            loadUi("UI\keyword_search.ui", self)
        except:
            loadUi("UI/keyword_search.ui", self)
        # button clicks
        self.goToKeywordManagerButton.clicked.connect(self.goToWelcome)
        self.addKeywordButton.clicked.connect(self.addKeywordToFav)
        self.requestKeywordButton.clicked.connect(self.requestKeyword)
    def setWidget(self, wid):
        #need to set up in order to get communication working
        self.widget = wid
    def goToWelcome(self):
        # Return to the keyword manager
        screen = KEYWORD(self.mySQL, self.db,self.widget)
        self.widget.addWidget(screen)
        self.widget.setCurrentIndex(1)

    def addKeywordToFav(self):
        # Determine if keyword exists or not if it does add it to users interests and give conformation message
        ###SQL needed
        ## if select is not null
        ##  SELECT * FROM keyword WHERE (keyword_name LIKE %userSearch%);
        ##  INSERT INTO user_interest (user_interest_id, search_word_id, interest_type) VALUES (userID, keywordID, interestType);
        pass

    def requestKeyword(self):
        # Determine if keyword exists if it does not add it to keyword managers list and give conformation message
        ###SQL needed examples
        # If select is null
        ##  SELECT * FROM keyword WHERE (keyword_name LIKE %userSearch%);
        ##  INSERT INTO pending_keyword (keyword, date_requested) VALUES (pendKeyword, currentDate);
        pass