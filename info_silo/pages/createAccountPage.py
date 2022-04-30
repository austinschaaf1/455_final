import sys

import pyqtgraph.examples
import time
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QMainWindow, QMessageBox
from PyQt5.uic import loadUi
import mysql.connector as mysql
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
from mplwidget import MplWidget
import numpy as np
import random

class CREATE(QDialog):  # INDEX = 3
    ####Create account class
    def __init__(self, mySQL, db,widget, user):
        super(CREATE, self).__init__()
        self.mySQL = mySQL
        self.db = db
        self.widget = widget
        self.user = user
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
        screen = CREATE(self.mySQL, self.db, self.widget, self.user)
        self.widget.addWidget(screen)
        self.widget.setCurrentIndex(1)

    def gotoLogin(self):
        screen = CREATE(self.mySQL, self.db, self.widget, self.user)
        self.widget.addWidget(screen)
        self.widget.setCurrentIndex(0)

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
            password = self.pass_input.text()
            sql = "INSERT INTO user_data (user_name, bday, membership_level) VALUES (%s, %s,%s);"
            val = (name, bday, memLevel)
            self.mySQL.execute(sql, val)

            self.db.commit()

            sql = "INSERT INTO logins (user_id, user_password, email) VALUES (LAST_INSERT_ID(), %s, %s)"
            val = (password, email)
            self.mySQL.execute(sql, val)
            self.db.commit()
            msg = QMessageBox()
            msg.setWindowTitle("Successful Account Creation")
            msg.setText("Account successfully created.\nPlease login to continue.")
            msg.exec_()
            self.gotoLogin()
            pass
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Account already exists!")
            msg.setText("An account with the provided email address already exists.\nPlease login to continue")
            msg.exec_()
            self.gotoLogin()
            pass