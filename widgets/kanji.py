from PyQt5 import QtCore, QtGui, QtWidgets
from widgets import scroll
import json
import os 

class KanjiWidget(QtWidgets.QMainWindow):
    def __init__(self, text, parent = None):
        super(KanjiWidget, self).__init__(parent)

        self.setFixedSize(500, 500)
        self.move(0, 0)
        self.KanjiText = text

        self.showKanjiInfo(self.KanjiText)

    def setTextScroll(self, text):

        # creating scroll label
        label = scroll.ScrollLabel(self)
 
        # setting text to the label
        label.setText(text)
 
        # setting geometry
        label.setGeometry(20, 20, 460, 460)

    def showKanjiInfo(self, text):
        text = self.deleteNoKanji(text)
        kanji_info = str()
        with open("data/kanji.json", "r") as kanji_json:
            self.kanji_data = json.load(kanji_json)
            for i in text:
                kanji_info = kanji_info + "Symbol: " + i + " " + "Frequency: " + str(self.kanji_data[i]["freq"]) + " " + "Meaning: " + str(self.kanji_data[i]["wk_meanings"]) + "\n" 
                #Рассмотреть случай отсутствия символа в kanji_dat

        self.setTextScroll(kanji_info)

    def deleteNoKanji(self, text):
        kanji = str()
        for i in text:
            if (ord(i) <= 40879) & (ord(i) >= 19968):
                kanji = kanji + i
        return kanji
