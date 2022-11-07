import sqlite3
import sys
import numpy as np
import pyqtgraph as pg
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QFileDialog, QTableWidgetItem, QMainWindow, QWidget, QInputDialog, QDialog, \
    QSpinBox, QDialog
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel


class W2(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('W2.ui', self)
        self.db_con = sqlite3.connect("CansatApp.db")
        self.db_cur = self.db_con.cursor()
        self.tableButton.clicked.connect(self.open_table)
        self.table = None
        self.plotButton.clicked.connect(self.build_plot)

    def open_table(self):
        self.name = f"FLight{self.tableBox.value()}"
        self.table = Table(self.name, self)
        self.table.show()
        self.table.exec()
        self.axx, self.axy = self.table.display_axis()
        self.table_info = self.db_cur.execute(f"""PRAGMA table_info(
              {self.name}
              );""").fetchall()
        self.yEdit.setText(self.table_info[self.axy][1])
        self.xEdit.setText(self.table_info[self.axx][1])

    def build_plot(self):
        self.x_coordsa = self.db_cur.execute(f"""SELECT {self.table_info[self.axx][1]} FROM {self.name}""").fetchall()
        self.y_coordsa = self.db_cur.execute(f"""SELECT {self.table_info[self.axy][1]} FROM {self.name}""").fetchall()
        self.x_coords, self.y_coords = [], []
        for i in range(len(self.x_coordsa)):
            self.x_coords.extend(self.x_coordsa[i])
            self.y_coords.extend(self.y_coordsa[i])
        self.plotView.plot(self.x_coords, self.y_coords)


class Table(QDialog):
    def __init__(self, name, widget):
        super().__init__()
        uic.loadUi('Table.ui', self)
        self.widget = widget
        self.ax = None
        self.axx = 0
        self.axy = 0
        self.display_data(name)
        self.dbView.selectionModel().selectionChanged.connect(self.choose_ax)
        self.chsxButton.clicked.connect(self.save_axx)
        self.chsyButton.clicked.connect(self.save_axy)

    def display_data(self, name):
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('CansatApp.db')
        db.open()
        model = QSqlTableModel(self, db)
        model.setTable(name)
        model.select()
        self.dbView.setModel(model)

    def choose_ax(self, selected):
        self.ax = selected.indexes()[0].column()

    def save_axx(self):
        self.axx = self.ax

    def save_axy(self):
        self.axy = self.ax

    def display_axis(self):
        return self.axx, self.axy
