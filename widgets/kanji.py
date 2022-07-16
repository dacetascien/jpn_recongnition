from PyQt5 import QtCore, QtGui, QtWidgets
import json
import os 

class KanjiWidget(QtWidgets.QMainWindow):
    def __init__(self, text, parent = None):
        super(KanjiWidget, self).__init__(parent)

        self.centralWidget = QtWidgets.QWidget()
        self.secondWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralWidget)

        self.setFixedSize(500, 500)
        self.move(0, 0)
        self.KanjiText = text
        self.KanjiLabel = QtWidgets.QLabel()

        layout = QtWidgets.QGridLayout(self.centralWidget)
        layout.addWidget(self.KanjiLabel)

        self.showKanjiInfo(self.KanjiText)

    def showKanjiInfo(self, text):
        text = self.deleteNoKanji(text)
        kanji_info = str()
        with open("data/kanji.json", "r") as kanji_json:
            self.kanji_data = json.load(kanji_json)
            for i in text:
                kanji_info = kanji_info + "Symbol: " + i + "\n" + "Frequency: " + str(self.kanji_data[i]["freq"]) + "\n" 
                #Рассмотреть случай отсутствия символа в kanji_dat

        self.KanjiLabel.setText(kanji_info)

    def deleteNoKanji(self, text):
        kanji = str()
        for i in text:
            if (ord(i) <= 40879) & (ord(i) >= 19968):
                kanji = kanji + i
        return kanji
