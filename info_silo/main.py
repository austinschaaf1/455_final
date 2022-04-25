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


# how to set up designer and qt 5
## https://www.youtube.com/watch?v=kxSuHyQfStA&t=0s
### Reference on muli screen setup
# https://www.youtube.com/watch?v=82v2ZR-g6wY
# pip install pyqt5
# pip install pyqt5-tools
## open designer by searching designer on search bar

class LOGIN(QMainWindow):  # INDEX = 0
    def __init__(self, mySQL, db):
        super(LOGIN, self).__init__()
        self.mySQL = mySQL
        self.db = db
        try:
            loadUi("UI\login.ui", self)
        except:
            loadUi("UI/login.ui", self)
        self.loginButton.clicked.connect(self.gotoScreen2)
        self.createAccountButton.clicked.connect(self.gotoCreateAccount)
        # self.keywordManagerButton.clicked.connect(self.gotoKeywordManager)

    def gotoScreen2(self):
        widget.setCurrentIndex(1)

    def gotoCreateAccount(self):
        widget.setCurrentIndex(3)

    def gotoKeywordManager(self):
        widget.setCurrentIndex(4)


class WELCOME(QDialog):  # INDEX = 1
    def __init__(self, mySQL, db):
        super(WELCOME, self).__init__()
        self.mySQL = mySQL
        self.db = db
        try:
            loadUi("UI\welcome.ui", self)
        except:
            loadUi("UI/welcome.ui", self)
        self.returnToLogin.clicked.connect(self.gotoScreen2)
        self.compareButton.clicked.connect(self.gotoCompare)
        self.stockSearchButton.clicked.connect(self.goToStockSearch)
        self.keywordSearchButton.clicked.connect(self.goToKeywordSearch)

    def gotoScreen2(self):
        screen = WELCOME(self.mySQL, self.db)
        widget.addWidget(screen)
        widget.setCurrentIndex(0)

    def gotoCompare(self):
        screen = WELCOME(self.mySQL, self.db)
        widget.addWidget(screen)
        widget.setCurrentIndex(2)

    def goToStockSearch(self):
        screen = WELCOME(self.mySQL, self.db)
        widget.addWidget(screen)
        widget.setCurrentIndex(6)

    def goToKeywordSearch(self):
        screen = WELCOME(self.mySQL, self.db)
        widget.addWidget(screen)
        widget.setCurrentIndex(5)


class COMPARE(QDialog):  # INDEX = 2
    def __init__(self, mySQL, db):
        super(COMPARE, self).__init__()
        self.mySQL = mySQL
        self.db = db
        try:
            loadUi("UI\compare.ui", self)
        except:
            loadUi("UI/compare.ui", self)
        self.backToList.clicked.connect(self.gotoWelcome)
        self.update_graph()
        self.clearButton.clicked.connect(self.updateGraph)
        # self.plotData()
        # pyqtgraph.examples.run()
        # self.setLegend()
        # self.plotButton.clicked.connect(self.plotData)
        # self.clearButton.clicked.connect(self.clearData)

    def gotoWelcome(self):
        screen = COMPARE(self.mySQL, self.db)
        widget.addWidget(screen)
        widget.setCurrentIndex(1)

    def update_graph(self):
        x1 = ([1, 2, 3, 4, 5, 6])
        y1 = ([3, 5, 6, 8, 4, 7])
        x2 = ([1, 2, 3, 4, 5, 6])
        y2 = ([2, 4, 4, 7, 8, 9])

        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.plot(x1, y1)
        self.MplWidget.canvas.axes.plot(x2, y2)
        self.MplWidget.canvas.axes.legend(('STOCKNAME', 'KEYWORD'), loc='upper right')
        self.MplWidget.canvas.axes.set_ylabel("Y-AXIS")
        self.MplWidget.canvas.axes.set_xlabel("X-AXIS")
        self.MplWidget.canvas.axes.set_title("Comparisons")
        self.MplWidget.canvas.draw()

    def updateGraph(self):
        self.update_graph()


class CREATE(QDialog):  # INDEX = 3
    ####Create account class
    def __init__(self, mySQL, db):
        super(CREATE, self).__init__()
        self.mySQL = mySQL
        self.db = db
        try:
            loadUi("UI\create_account.ui", self)
        except:
            loadUi("UI/create_account.ui", self)
        self.welcomeButton.clicked.connect(self.gotoWelcome)
        self.create_account.clicked.connect(self.createAccount)

    def gotoWelcome(self):
        screen = CREATE(self.mySQL, self.db)
        widget.addWidget(screen)
        widget.setCurrentIndex(1)

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


class KEYWORD(QDialog):  # INDEX = 4
    def __init__(self, mySQL, db):
        super(KEYWORD, self).__init__()
        self.mySQL = mySQL
        self.db = db
        try:
            loadUi("UI\keyword_manager.ui", self)
        except:
            loadUi("UI/keyword_manager.ui", self)
        self.homeButton.clicked.connect(self.gotoWelcome)
        self.loadList()
        self.approveButton.clicked.connect(self.addToDB)

    def gotoWelcome(self):
        screen = KEYWORD(self.mySQL, self.db)
        widget.addWidget(screen)
        widget.setCurrentIndex(1)

    def loadList(self):
        sql = "SELECT keyword FROM pending_keyword"
        self.mySQL.execute(sql)
        exists = self.mySQL.fetchall()
        for row in exists:
            self.keywordList.addItem(row[0])

    def addToDB(self):
        keyword_name = self.keywordList.itemClicked()
        sql = "INSERT INTO keyword (keyword_name) VALUES (%s)"
        val = keyword_name
        self.mySQL.execute(sql, val)


class SEARCH_KEYWORD(QDialog):  # INDEX = 5
    def __init__(self, mySQL, db):
        super(SEARCH_KEYWORD, self).__init__()
        self.mySQL = mySQL
        self.db = db
        try:
            loadUi("UI\keyword_search.ui", self)
        except:
            loadUi("UI/keyword_search.ui", self)
        # button clicks
        self.goToKeywordManagerButton.clicked.connect(self.goToKeywordManager)
        self.addKeywordButton.clicked.connect(self.addKeywordToFav)
        self.requestKeywordButton.clicked.connect(self.requestKeyword)

    def goToKeywordManager(self):
        # Return to the keyword manager
        screen = KEYWORD(self.mySQL, self.db)
        widget.addWidget(screen)
        widget.setCurrentIndex(4)

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


class SEARCH_STOCK(QDialog):  # INDEX = 6
    def __init__(self, mySQL, db):
        super(SEARCH_STOCK, self).__init__()
        self.mySQL = mySQL
        self.db = db
        try:
            loadUi("UI\stock_search.ui", self)
        except:
            loadUi("UI/stock_search.ui", self)
        # button clicks
        self.goToKeywordManagerButton.clicked.connect(self.goToKeywordManager)
        self.addStockButton.clicked.connect(self.addStockToFav)

    def goToKeywordManager(self):
        # Return to the keyword manager
        screen = KEYWORD(self.mySQL, self.db)
        widget.addWidget(screen)
        widget.setCurrentIndex(4)

    def addStockToFav(self):
        # Determine if stock exists or not if it does add it to users interests and give conformation message
        ###SQL needed
        ## if select is not null
        ##  SELECT * FROM stocks where (ticker LIKE ‘searchTicker%’);
        ##  INSERT INTO user_interest (user_interest_id, search_word_id, interest_type) VALUES (userID, keywordID, interestType);
        self.success_label.setText("Stock XX added successfully")
        pass


# Data Base connection
HOST = "cs455project.csuy1zz16lbb.us-east-1.rds.amazonaws.com"
DATABASE = "455 Project"
USER = "admin"
PASSWORD = "FLBbA3YWrg7PKA5"
db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
mySQL = db_connection.cursor()
print("Connected to: ", db_connection.get_server_info())

# main
app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()  # shows the windows
login = LOGIN(mySQL, db_connection)
welcome = WELCOME(mySQL, db_connection)
compare = COMPARE(mySQL, db_connection)
create = CREATE(mySQL, db_connection)
keyword_manager = KEYWORD(mySQL, db_connection)
keywordSearch = SEARCH_KEYWORD(mySQL, db_connection)
stockSearch = SEARCH_STOCK(mySQL, db_connection)

widget.addWidget(login)
widget.addWidget(welcome)
widget.addWidget(compare)
widget.addWidget(create)
widget.addWidget(keyword_manager)
widget.addWidget(keywordSearch)
widget.addWidget(stockSearch)

widget.setFixedHeight(600)
widget.setFixedWidth(800)
widget.show()

try:
    sys.exit(app.exec_())
except:
    print("exiting")
