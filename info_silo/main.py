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

class LOGIN(QMainWindow):
    def __init__(self):
        super(LOGIN,self).__init__()
        loadUi("UI\login.ui",self)
        self.loginButton.clicked.connect(self.gotoScreen2)
        
        

    def gotoScreen2(self):
        widget.setCurrentIndex(widget.currentIndex() + 1)

class WELCOME(QDialog):
    def __init__(self):
        super(WELCOME, self).__init__()
        loadUi("UI\welcome.ui",self)
        self.returnToLogin.clicked.connect(self.gotoScreen2)
    def gotoScreen2(self):
        screen = WELCOME()
        widget.addWidget(screen)
        widget.setCurrentIndex(widget.currentIndex() - 1)




#main
app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget() #shows the windows
login = LOGIN()
welcome = WELCOME()


widget.addWidget(login)
widget.addWidget(welcome)

widget.setFixedHeight(600)
widget.setFixedWidth(800)
widget.show()

try:
    sys.exit(app.exec_())
except:
    print("exiting")