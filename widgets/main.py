from PyQt5 import QtCore, QtGui, QtWidgets
from PIL import ImageGrab
import widgets
import pytesseract as pt
import time
from pynput import keyboard
import clipboard
from translate import Translator

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
        self.secondWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralWidget)
        main_layout = QtWidgets.QVBoxLayout(self.centralWidget)

        self.label = QtWidgets.QLabel(alignment=QtCore.Qt.AlignCenter)
        self.area_button = QtWidgets.QPushButton('Select area')
        self.area_button.clicked.connect(self.activateSnipping)
        self.clip_button = QtWidgets.QPushButton('Copy to clipboard')
        self.clip_button.clicked.connect(self.copyClipboard) #Разобраться с копирование в клипборд
        self.kanjiText = widgets.scroll.ScrollLabel(self)
        self.transText = widgets.scroll.ScrollLabel(self)
        self.kanjiAnnotation = QtWidgets.QLabel()
        self.transAnnotation = QtWidgets.QLabel()

        layout = QtWidgets.QGridLayout(self.centralWidget)
        text_layout = QtWidgets.QVBoxLayout(self.centralWidget)
        main_layout.addLayout(layout)
        main_layout.addLayout(text_layout)
        layout.addWidget(self.label, 0, 0, 1, 3)
        layout.addWidget(self.area_button, 1, 0, 1, 2)
        layout.addWidget(self.clip_button, 1, 2, 1, 1)
        text_layout.addWidget(self.kanjiAnnotation)
        text_layout.addWidget(self.kanjiText)
        text_layout.addWidget(self.transAnnotation)
        text_layout.addWidget(self.transText)
        self.kanjiAnnotation.setText("Detected text: ")
        self.transAnnotation.setText("Translsted text: ")
        self.kanjiAnnotation.hide()
        self.transAnnotation.hide()
        self.kanjiText.hide()
        self.transText.hide()

        self.snipper = SnippingWidget()
        self.snipper.closed.connect(self.on_closed)

    def setBackground(self):
        bg = ImageGrab.grab()
        bg.save("temp/bg.png")
        stylesheet = """
            SnippingWidget {
                background-image: url("temp/bg.png"); 
                background-repeat: no-repeat; 
            }
        """
        
        self.snipper.setStyleSheet(stylesheet)

    def activateSnipping(self):
        self.hide()
        time.sleep(0.1) #Костыль на ожидание закрытия окна
        self.setBackground()
        self.snipper.showFullScreen()
        self.snipper.show()
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.CrossCursor)

    def deleteNoJpn(self, text): #Нужны также другие японские алфавиты
        jpn = str()
        for i in text:
            if ((ord(i) <= 40879) and (ord(i) >= 19968)) or (ord(i) >= 12352) and (ord(i) <= 12447):
                jpn = jpn + i
        return jpn 

    def copyClipboard(self):
        clipboard.copy(pt.image_to_string(img, lang = 'jpn'))

    def translate(seld, text):
        translator= Translator(to_lang="en", from_lang = "ja")
        translation = translator.translate(text)
        return translation

    def on_closed(self):
        pixmap = QtGui.QPixmap("temp/area.png")

        jpn_text = self.deleteNoJpn(pt.image_to_string(img, lang = 'jpn'))
        self.kanjiText.setText(jpn_text)
        self.transText.setText(self.translate(jpn_text))
        self.kanjiAnnotation.show()
        self.transAnnotation.show()
        self.kanjiText.show()
        self.transText.show()

        self.kanji = widgets.kanji.KanjiWidget(jpn_text)
        self.kanji.show()
        
        if pixmap.width() > pixmap.height():
            self.label.setPixmap(pixmap.scaledToWidth(720))
        else:
            self.label.setPixmap(pixmap.scaledToHeight(270))

        self.show()
        self.adjustSize()