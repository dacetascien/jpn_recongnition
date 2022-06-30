from PyQt5 import QtCore, QtGui, QtWidgets
import pytesseract as pt
from PIL import ImageGrab
import os
import clipboard

class SnippingWidget(QtWidgets.QMainWindow):
    closed = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(SnippingWidget, self).__init__(parent)

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
        global img
        img = ImageGrab.grab(r.getCoords())
        img.save("temp/area.png")
        self.hide()
        QtWidgets.QApplication.restoreOverrideCursor()
        self.closed.emit() #Закрывать сразу все виджеты из slip_widgets
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
        self.secondWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralWidget)

        self.label = QtWidgets.QLabel(alignment=QtCore.Qt.AlignCenter)
        self.area_button = QtWidgets.QPushButton('Select area')
        self.area_button.clicked.connect(self.activateSnipping)
        self.clip_button = QtWidgets.QPushButton('Copy to clipboard')
        self.clip_button.clicked.connect(self.copyClipboard)
        self.text = QtWidgets.QLabel()

        layout = QtWidgets.QGridLayout(self.centralWidget)
        layout.addWidget(self.label, 0, 0)
        layout.addWidget(self.area_button, 1, 0)
        layout.addWidget(self.clip_button, 1, 1)
        layout.addWidget(self.text, 2, 0)

        #self.snipper = SnippingWidget() 
        #self.snipper.closed.connect(self.on_closed) 

    def setBackground(self, screen, widget, n):
        geom = screen.geometry()
        bg = screen.grabWindow(0)
        bg.save("temp/bg" + str(n) + ".png")

        stylesheet = ("""
            SnippingWidget {
                background-image: url("temp/bg""" + str(n) + """.png"); 
                background-repeat: no-repeat; 
            }
        """)

        widget.setStyleSheet(stylesheet)

    def activateSnipping(self):
        self.slip_widgets = list()
        for n, i in enumerate(QtGui.QGuiApplication.screens()):
                self.slip_widgets.append(SnippingWidget())
                self.setBackground(i, self.slip_widgets[n], n)
                self.slip_widgets[n].setFixedSize(1, 1)
                self.slip_widgets[n].move(0, 0)
                self.slip_widgets[n].show()
                #self.slip_widgets[n].windowHandle().setScreen(i)
                if n!=0:
                    self.slip_widgets[n].move(2000, 0)
                self.slip_widgets[n].showFullScreen()
                self.slip_widgets[n].closed.connect(self.on_closed)
        

        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.CrossCursor)
        self.hide()

    def copyClipboard(self):
        clipboard.copy(pt.image_to_string(img, lang = 'jpn'))

    def on_closed(self):
        for i in self.slip_widgets:
            i.closed.emit()
        pixmap = QtGui.QPixmap("temp/area.png")
        self.text.setText("Detected text:\n" + pt.image_to_string(img, lang = 'jpn'))

        
        #try:
        #    os.remove("temp/bg.png")
        #except:
        #    pass
        
        if pixmap.width() > pixmap.height():
            self.label.setPixmap(pixmap.scaledToWidth(720))
        else:
            self.label.setPixmap(pixmap.scaledToHeight(270))

        self.show()
        self.adjustSize()