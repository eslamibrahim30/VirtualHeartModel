#!/usr/bin/env python3
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class QTGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(30, 30, 530, 530)

    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap("EP.png")
        painter.drawPixmap(self.rect(), pixmap)
        pen = QPen(Qt.red, 3)
        painter.setPen(pen)
        painter.drawLine(10, 10, self.rect().width() -10 , 10)
