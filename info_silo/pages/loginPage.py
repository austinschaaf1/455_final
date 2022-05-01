import sys

import pyqtgraph.examples
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QMainWindow, QLineEdit, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import mysql.connector as mysql

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
from mplwidget import MplWidget
import numpy as np
import random

import __main__




class LOGIN(QMainWindow):  # INDEX = 0
    def __init__(self, mySQL, db, widget, user):
        super(LOGIN, self).__init__()
        self.mySQL = mySQL
        self.db = db
        self.widget = widget
        self.user = user
        try:
            loadUi("UI\login.ui", self)
        except:
            loadUi("UI/login.ui", self)
        self.loginButton.clicked.connect(self.gotoScreen2)
        self.createAccountButton.clicked.connect(self.gotoCreateAccount)

        ## Quick Logins
        # self.dimButton.setVisible(False)
        # self.chrisButton.setVisible(False)
        # self.austinButton.setVisible(False)
        self.dimButton.clicked.connect(self.dimLogin)
        self.austinButton.clicked.connect(self.austinLogin)
        self.chrisButton.clicked.connect(self.chrisLogin)

        # self.keywordManagerButton.clicked.connect(self.gotoKeywordManager)

    def setWidget(self, wid):
        # need to set up in order to get communication working
        self.widget = wid

    def gotoScreen2(self):
        email = self.emailText.text()
        password = self.passwordText.text()
        sql = "SELECT user_id from logins WHERE email = %s AND user_password = %s"
        params = (email, password)  # Protect against SQL injection
        self.mySQL.execute(sql, params)
        result = self.mySQL.fetchone()
        user_id = result
        self.emailText.clear()
        self.passwordText.clear()
        if not user_id:
            # print("Invalid Login information. Try again")
            msg = QMessageBox()
            msg.setWindowTitle("Invalid Login!")
            msg.setText("Email and password do not match.\nTry again!")
            msg.exec_()
            return
        self.user.append(user_id)
        # print("User id: %d" % user_id)

        self.widget.setCurrentIndex(1)

    def gotoCreateAccount(self):
        self.widget.setCurrentIndex(3)

    def gotoKeywordManager(self):
        self.widget.setCurrentIndex(4)

    def austinLogin(self):
        email = self.emailText.text()
        password = self.passwordText.text()
        user_id = (5, 0)
        self.emailText.clear()
        self.passwordText.clear()
        self.user.append(user_id)
        self.widget.setCurrentIndex(1)

    def chrisLogin(self):
        email = self.emailText.text()
        password = self.passwordText.text()
        user_id = (6, 0)
        self.emailText.clear()
        self.passwordText.clear()
        self.user.append(user_id)
        self.widget.setCurrentIndex(1)

    def dimLogin(self):
        email = self.emailText.text()
        password = self.passwordText.text()
        user_id = (7, 0)
        self.emailText.clear()
        self.passwordText.clear()
        self.user.append(user_id)
        self.widget.setCurrentIndex(1)
