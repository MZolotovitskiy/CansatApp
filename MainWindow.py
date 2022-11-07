import sqlite3
import sys
import numpy as np
import pyqtgraph as pg
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QFileDialog, QTableWidgetItem, QMainWindow, QWidget, QInputDialog, QDialog, \
    QSpinBox, QDialog
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel

from W1 import W1
from W2 import W2


class MainWindow(QMainWindow):
    def __init__(self):  # Инициализация главного окна
        super().__init__()
        self.W1 = W1()
        self.W2 = W2()
        uic.loadUi('Wm.ui', self)  #
        self.w1Button.clicked.connect(self.open_w1)
        self.w2Button.clicked.connect(self.open_w2)

    def open_w1(self):
        self.W1.show()

    def open_w2(self):
        self.W2.show()
