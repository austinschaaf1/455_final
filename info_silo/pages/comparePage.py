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

from info_silo.pages.loginPage import LOGIN
from info_silo.pages.welcomePage import WELCOME


class COMPARE(QDialog):  # INDEX = 2
    def __init__(self, mySQL, db, widget):
        super(COMPARE, self).__init__()
        self.mySQL = mySQL
        self.db = db
        self.widget = widget
        try:
            loadUi("UI\compare.ui", self)
        except:
            loadUi("UI/compare.ui", self)
        self.backToList.clicked.connect(self.gotoWelcome)
        self.update_graph()

    def setWidget(self, wid):
        # need to set up in order to get communication working
        self.widget = wid

    def gotoWelcome(self):
        screen = COMPARE(self.mySQL, self.db, self.widget)
        self.widget.addWidget(screen)
        self.widget.setCurrentIndex(1)

    def update_graph(self):

        x1 = ([1, 2, 3, 4, 5, 6])
        y1 = ([3, 5, 6, 8, 4, 7])
        x2 = ([1, 2, 3, 4, 5, 6])
        y2 = ([2, 4, 4, 7, 8, 9])


        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.plot(x1, y1)
        self.MplWidget.canvas.axes.plot(x2, y2)
        self.MplWidget.canvas.axes.legend((WELCOME.stockSelected, "FUCHSIA"), loc='upper right')
        self.MplWidget.canvas.axes.set_ylabel("Y-AXIS")
        self.MplWidget.canvas.axes.set_xlabel("X-AXIS")
        self.MplWidget.canvas.axes.set_title("Comparisons")
        self.MplWidget.canvas.draw()
