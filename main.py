import sys
from widgets import main
from PyQt5 import QtCore, QtGui, QtWidgets

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = main.MainWindow()

    w.setFixedSize(800, 500) 
    w.move(50, 50) 
    w.show()

    sys.exit(app.exec_())