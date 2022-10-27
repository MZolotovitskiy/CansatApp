import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QFileDialog, QTableWidgetItem
from PyQt5.QtWidgets import QMainWindow, QWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.W1 = W1()
        self.W2 = W2()
        uic.loadUi('Wm.ui', self)
        self.w1Button.clicked.connect(self.open_w1)
        self.w2Button.clicked.connect(self.open_w2)

    def open_w1(self):
        self.W1.show()

    def open_w2(self):
        self.W2.show()


class W1(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('W1.ui', self)
        self.data_file = str()
        self.format = str()
        self.column = int()
        self.data = None
        self.cur = None
        self.db_con = sqlite3.connect("CansatApp.db")
        self.addButton.clicked.connect(self.add_data)

    def add_data(self):
        self.data_file = QFileDialog.getOpenFileName(self)
        self.data = [[float(j) for j in i.split()] for i in
                     open(self.data_file[0], mode="r", encoding="UTF-8").readlines()]
        self.cur = self.db_con.cursor()
        for row in range(len(self.data)):
            self.cur.execute("INSERT INTO First_flight(Package, Time, Ax, Ay, Az, Temperature, Altitude, Pressure)"
                             "VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                             (row, self.data[row][1], self.data[row][2], self.data[row][3], self.data[row][4],
                              self.data[row][4], self.data[row][6], self.data[row][7]))
            self.db_con.commit()
        self.display_data(self.data)

    def display_data(self, table, rows=12):
        pass

    def closeEvent(self, event):
        pass


class W2(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('W2.ui', self)
