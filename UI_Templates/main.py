import sys
from PyQt5 import QtWidgets, QtCore
import untitled
from PyQt5 import QtCore, QtGui, QtWidgets
from untitled import Ui_MainWindow


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())

# app = QtWidgets.QApplication(sys.argv)
# widget = QtWidgets.QWidget()
# widget.resize(400, 200)
# widget.setWindowTitle("This is PyQt Widget example")
# widget.show()
# exit(app.exec_())
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
