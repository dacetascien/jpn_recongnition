import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PIL import ImageGrab
import pytesseract as pt
import os
from pynput import keyboard


class SnippingWidget(QtWidgets.QMainWindow):
    closed = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(SnippingWidget, self).__init__(parent)

        img = ImageGrab.grab()
        img.save("temp/bg.png")
        stylesheet = """
            SnippingWidget {
                background-image: url("temp/bg.png"); 
                background-repeat: no-repeat; 
            }
        """

        self.setStyleSheet(stylesheet)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.outsideSquareColor = "red"
        self.squareThickness = 2

        self.start_point = QtCore.QPoint()
        self.end_point = QtCore.QPoint()

    def mousePressEvent(self, event):
        self.start_point = event.pos()
        self.end_point = event.pos()
        self.update()

    def mouseMoveEvent(self, event):
        self.end_point = event.pos()
        self.update()

    def mouseReleaseEvent(self, QMouseEvent):
        r = QtCore.QRect(self.start_point, self.end_point).normalized()
        img = ImageGrab.grab(r.getCoords())
        print(pt.image_to_string(img, lang = 'jpn'))
        img.save("temp/area.png")
        self.hide()
        QtWidgets.QApplication.restoreOverrideCursor()
        self.closed.emit()
        self.start_point = QtCore.QPoint()
        self.end_point = QtCore.QPoint()

    def paintEvent(self, event):
        trans = QtGui.QColor(22, 100, 233)
        r = QtCore.QRectF(self.start_point, self.end_point).normalized()
        qp = QtGui.QPainter(self)
        trans.setAlphaF(0.2)
        qp.setBrush(trans)
        outer = QtGui.QPainterPath()
        outer.addRect(QtCore.QRectF(self.rect()))
        inner = QtGui.QPainterPath()
        inner.addRect(r)
        r_path = outer - inner
        qp.drawPath(r_path)
        qp.setPen(
            QtGui.QPen(QtGui.QColor(self.outsideSquareColor), self.squareThickness)
        )
        trans.setAlphaF(0)
        qp.setBrush(trans)
        qp.drawRect(r)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralWidget)

        self.label = QtWidgets.QLabel(alignment=QtCore.Qt.AlignCenter)
        self.button = QtWidgets.QPushButton('Select area')
        self.button.clicked.connect(self.activateSnipping)
        
        layout = QtWidgets.QVBoxLayout(self.centralWidget)
        layout.addWidget(self.label, 1)
        layout.addWidget(self.button, 0)

        self.snipper = SnippingWidget()
        self.snipper.closed.connect(self.on_closed)

    def activateSnipping(self):
        self.snipper.showFullScreen()
        self.snipper.show()
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.CrossCursor)
        self.hide()

    def on_closed(self):
        pixmap = QtGui.QPixmap("temp/area.png")

        try:
            os.remove("temp/bg.png")
        except:
            pass

        self.setFixedSize(pixmap.width(), pixmap.height()) 
        self.label.setPixmap(pixmap)
        self.show()
        self.adjustSize()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.setFixedSize(400, 300) 
    w.move(50, 50) 
    w.show()
    sys.exit(app.exec_())