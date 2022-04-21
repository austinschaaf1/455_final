import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QMainWindow
from PyQt5.uic import loadUi

# how to set up designer and qt 5
## https://www.youtube.com/watch?v=kxSuHyQfStA&t=0s
### Reference on muli screen setup
# https://www.youtube.com/watch?v=82v2ZR-g6wY
# pip install pyqt5
# pip install pyqt5-tools
## open designer by searching designer on search bar

class LOGIN(QMainWindow): #INDEX = 0
    def __init__(self):
        super(LOGIN,self).__init__()
        loadUi("UI\login.ui",self)
        try:
            loadUi("UI\login.ui",self)
        except:
            loadUi("UI/login.ui",self)
        self.loginButton.clicked.connect(self.gotoScreen2)
        self.createAccountButton.clicked.connect(self.gotoCreateAccount)
        
    def gotoScreen2(self):
        widget.setCurrentIndex(1)
    def gotoCreateAccount(self):
        widget.setCurrentIndex(3)

class WELCOME(QDialog):  #INDEX = 1
    def __init__(self):
        super(WELCOME, self).__init__()
        try:
            loadUi("UI\welcome.ui",self)
        except:
            loadUi("UI/welcome.ui",self)
        self.returnToLogin.clicked.connect(self.gotoScreen2)
        self.compair1.clicked.connect(self.gotoCompair)
    def gotoScreen2(self):
        screen = WELCOME()
        widget.addWidget(screen)
        widget.setCurrentIndex(0)

    def gotoCompair(self):
        screen = WELCOME()
        widget.addWidget(screen)
        widget.setCurrentIndex(2)

class COMPAIR(QDialog):  #INDEX = 2
    def __init__(self):
        super(COMPAIR, self).__init__()
        try:
            loadUi("UI\compare.ui",self)
        except:
            loadUi("UI/compare.ui",self)
        self.backToList.clicked.connect(self.gotoWelcome)
 
    def gotoWelcome(self):
        screen = COMPAIR()
        widget.addWidget(screen)
        widget.setCurrentIndex(1)
class CREATE(QDialog):  #INDEX = 3
    def __init__(self):
        super(CREATE, self).__init__()
        try:
            loadUi("UI\create_account.ui",self)
        except:
            loadUi("UI/create_account.ui",self)
        self.welcomeButton.clicked.connect(self.gotoWelcome)
 
    def gotoWelcome(self):
        screen = CREATE()
        widget.addWidget(screen)
        widget.setCurrentIndex(1)




#main
app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget() #shows the windows
login = LOGIN()
welcome = WELCOME()
compair = COMPAIR()
create = CREATE()


widget.addWidget(login)
widget.addWidget(welcome)
widget.addWidget(compair)
widget.addWidget(create)

widget.setFixedHeight(600)
widget.setFixedWidth(800)
widget.show()

try:
    sys.exit(app.exec_())
except:
    print("exiting")