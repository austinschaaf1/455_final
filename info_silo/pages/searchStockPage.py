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

class SEARCH_STOCK(QDialog):  # INDEX = 6
    def __init__(self, mySQL, db,widget):
        super(SEARCH_STOCK, self).__init__()
        self.mySQL = mySQL
        self.db = db
        self.widget = widget
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
        screen = WELCOME(self.mySQL, self.db,self.widget)
        self.widget.addWidget(screen)
        self.widget.setCurrentIndex(1)

    def addStockToFav(self):
        # Determine if stock exists or not if it does add it to users interests and give conformation message
        ###SQL needed
        ## if select is not null
        ##  SELECT * FROM stocks where (ticker LIKE ‘searchTicker%’);
        ##  INSERT INTO user_interest (user_interest_id, search_word_id, interest_type) VALUES (userID, keywordID, interestType);
        self.success_label.setText("Stock XX added successfully")
        pass