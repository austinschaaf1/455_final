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

# how to set up designer and qt 5
## https://www.youtube.com/watch?v=kxSuHyQfStA&t=0s
### Reference on muli screen setup
# https://www.youtube.com/watch?v=82v2ZR-g6wY
# pip install pyqt5
# pip install pyqt5-tools
## open designer by searching designer on search bar


# Data Base connection
HOST = "cs455project.csuy1zz16lbb.us-east-1.rds.amazonaws.com"
DATABASE = "455 Project"
USER = "admin"
PASSWORD = "FLBbA3YWrg7PKA5"
db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
mySQL = db_connection.cursor()
print("Connected to: ", db_connection.get_server_info())

# Set up all windows
app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
login = LOGIN(mySQL, db_connection, widget)
welcome = WELCOME(mySQL, db_connection, widget)
compare = COMPARE(mySQL, db_connection, widget)
create = CREATE(mySQL, db_connection, widget)
keyword_manager = KEYWORD(mySQL, db_connection, widget)
keywordSearch = SEARCH_KEYWORD(mySQL, db_connection, widget)
stockSearch = SEARCH_STOCK(mySQL, db_connection, widget)

# add widgets for page transitions
widget.addWidget(login)
widget.addWidget(welcome)
widget.addWidget(compare)
widget.addWidget(create)
widget.addWidget(keyword_manager)
widget.addWidget(keywordSearch)
widget.addWidget(stockSearch)

# with all widgets created pass them to class
login.setWidget(widget)
welcome.setWidget(widget)
compare.setWidget(widget)
create.setWidget(widget)
keyword_manager.setWidget(widget)
keywordSearch.setWidget(widget)
stockSearch.setWidget(widget)

# Set up sizes
widget.setFixedHeight(600)
widget.setFixedWidth(800)
widget.show()

try:
    sys.exit(app.exec_())
except:
    print("exiting")
