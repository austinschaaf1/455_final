import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi

# how to set up designer and qt 5
## https://www.youtube.com/watch?v=kxSuHyQfStA&t=0s
### Reference on muli screen setup
# https://www.youtube.com/watch?v=82v2ZR-g6wY
# pip install pyqt5
# pip install pyqt5-tools
## open designer by searching designer on search bar

class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow,self).__init__()
        loadUi("455_final\info_silo\page4.ui",self)
        self.button1.clicked.connect(self.gotoScreen2)

    def gotoScreen2(self):
        widget.setCurrentIndex(widget.currentIndex() + 1)


class Screen2(QDialog):
    def __init__(self):
        super(Screen2, self).__init__()
        loadUi("455_final\info_silo\page5.ui",self)
        self.button2.clicked.connect(self.gotoScreen2)
    
    def gotoScreen2(self):
        screen = Screen2()
        widget.addWidget(screen)
        widget.setCurrentIndex(widget.currentIndex() - 1)

#main
app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget() #shows the windows
mainWindow = MainWindow()

widget.addWidget(mainWindow)
widget.setFixedHeight(300)
widget.setFixedWidth(400)
widget.show()

try:
    sys.exit(app.exec_())
except:
    print("exiting")