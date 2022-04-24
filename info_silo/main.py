import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QMainWindow
from PyQt5.uic import loadUi
import mysql.connector as mysql

# how to set up designer and qt 5
## https://www.youtube.com/watch?v=kxSuHyQfStA&t=0s
### Reference on muli screen setup
# https://www.youtube.com/watch?v=82v2ZR-g6wY
# pip install pyqt5
# pip install pyqt5-tools
## open designer by searching designer on search bar

class LOGIN(QMainWindow): #INDEX = 0
    def __init__(self,mySQL,db):
        super(LOGIN,self).__init__()
        self.mySQL = mySQL
        self.db = db
        loadUi("UI\login.ui",self)
        try:
            loadUi("UI\login.ui",self)
        except:
            loadUi("UI/login.ui",self)
        self.loginButton.clicked.connect(self.gotoScreen2)
        self.createAccountButton.clicked.connect(self.gotoCreateAccount)
        self.keywordManagerButton.clicked.connect(self.gotoKeywordManager)
        
    def gotoScreen2(self):
        widget.setCurrentIndex(1)
    def gotoCreateAccount(self):
        widget.setCurrentIndex(3)
    def gotoKeywordManager(self):
        widget.setCurrentIndex(4)

class WELCOME(QDialog):  #INDEX = 1
    def __init__(self,mySQL,db):
        super(WELCOME, self).__init__()
        self.mySQL = mySQL
        self.db = db
        try:
            loadUi("UI\welcome.ui",self)
        except:
            loadUi("UI/welcome.ui",self)
        self.returnToLogin.clicked.connect(self.gotoScreen2)
        self.compair1.clicked.connect(self.gotoCompair)
    def gotoScreen2(self):
        screen = WELCOME(self.mySQL, self.db)
        widget.addWidget(screen)
        widget.setCurrentIndex(0)

    def gotoCompair(self):
        screen = WELCOME(self.mySQL, self.db)
        widget.addWidget(screen)
        widget.setCurrentIndex(2)

class COMPAIR(QDialog):  #INDEX = 2
    def __init__(self,mySQL,db):
        super(COMPAIR, self).__init__()
        self.mySQL = mySQL
        self.db = db
        try:
            loadUi("UI\compare.ui",self)
        except:
            loadUi("UI/compare.ui",self)
        self.backToList.clicked.connect(self.gotoWelcome)
 
    def gotoWelcome(self):
        screen = COMPAIR(self.mySQL, self.db)
        widget.addWidget(screen)
        widget.setCurrentIndex(1)

class CREATE(QDialog):  #INDEX = 3
    def __init__(self,mySQL,db):
        super(CREATE, self).__init__()
        self.mySQL = mySQL
        self.db = db
        try:
            loadUi("UI\create_account.ui",self)
        except:
            loadUi("UI/create_account.ui",self)
        self.welcomeButton.clicked.connect(self.gotoWelcome)
        self.create_account.clicked.connect(self.createAccount)
 
    def gotoWelcome(self):
        screen = CREATE(self.mySQL, self.db)
        widget.addWidget(screen)
        widget.setCurrentIndex(1)
    def createAccount(self):
        sql = "INSERT INTO keyword (keyword_dbkey, keyword_name) VALUES (%s, %s)"
        val = ("John", "Highway 21")
        self.mySQL.execute(sql, val)

        self.db.commit()
        print(self.nameInput.text())


class KEYWORD(QDialog):  #INDEX = 4
    def __init__(self,mySQL,db):
        super(KEYWORD, self).__init__()
        self.mySQL = mySQL
        self.db = db
        try:
            loadUi("UI\keyword_manager.ui",self)
        except:
            loadUi("UI/keyword_manager.ui",self)
        self.Welcome.clicked.connect(self.gotoWelcome)
 
    def gotoWelcome(self):
        screen = KEYWORD(self.mySQL, self.db)
        widget.addWidget(screen)
        widget.setCurrentIndex(1)


#db setup
HOST = "cs455project.csuy1zz16lbb.us-east-1.rds.amazonaws.com"

DATABASE = "455 Project"

USER = "admin"

PASSWORD = "FLBbA3YWrg7PKA5"

db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
mySQL = db_connection.cursor() 
print("Connected to: ", db_connection.get_server_info())

#main
app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget() #shows the windows
login = LOGIN(mySQL,db_connection)
welcome = WELCOME(mySQL,db_connection)
compair = COMPAIR(mySQL,db_connection)
create = CREATE(mySQL,db_connection)
keyword_manager = KEYWORD(mySQL,db_connection)


widget.addWidget(login)
widget.addWidget(welcome)
widget.addWidget(compair)
widget.addWidget(create)
widget.addWidget(keyword_manager)


widget.setFixedHeight(600)
widget.setFixedWidth(800)
widget.show()

try:
    sys.exit(app.exec_())
except:
    print("exiting")