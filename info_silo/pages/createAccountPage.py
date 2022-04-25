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

class CREATE(QDialog):  # INDEX = 3
    ####Create account class
    def __init__(self, mySQL, db,widget):
        super(CREATE, self).__init__()
        self.mySQL = mySQL
        self.db = db
        self.widget = widget
        try:
            loadUi("UI\create_account.ui", self)
        except:
            loadUi("UI/create_account.ui", self)
        self.welcomeButton.clicked.connect(self.gotoWelcome)
        self.create_account.clicked.connect(self.createAccount)
    def setWidget(self, wid):
        #need to set up in order to get communication working
        self.widget = wid
    def gotoWelcome(self):
        screen = CREATE(self.mySQL, self.db,self.widget)
        self.widget.addWidget(screen)
        self.widget.setCurrentIndex(1)

    def createAccount(self):
        email = self.emailInput.text()
        sql = "SELECT * FROM logins WHERE email=%s"
        val = (email,)
        self.mySQL.execute(sql, val)
        exists = self.mySQL.fetchall()
        if len(exists) == 0:
            name = self.nameInput.text()
            bday = self.birthdayInput.text()
            memLevel = self.membership_input.text()
            sql = "INSERT INTO user_data (user_name, bday, membership_level) VALUES (%s, %s,%s)"
            val = (name, bday, memLevel)
            self.mySQL.execute(sql, val)

            self.db.commit()

            # INSERT INTO Login (user_id, password, email) VALUES (userID, userPassword, userEmail);

            # password = self.pass_input.text()
            # sql = "INSERT INTO logins (user_password, email) VALUES (%s, %s)"
            # val = (password, email)
            # self.mySQL.execute(sql, val)

            # self.db.commit()
            pass
        else:
            pass