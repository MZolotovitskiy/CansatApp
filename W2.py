import sqlite3
import pyqtgraph as pg

from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QWidget, QDialog, QColorDialog
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel


class W2(QWidget):
    def __init__(self):
        super().__init__()
        self.symbol = None
        self.color = (255, 255, 255)
        self.name = None
        self.table = None
        self.axx = None
        self.axy = None
        self.table_inf = None
        self.x_coords = None
        self.x_coordsa = None
        self.y_coords = None
        self.y_coordsa = None
        self.symboldialog = None
        uic.loadUi('W2.ui', self)
        self.db_con = sqlite3.connect("CansatApp.db")
        self.db_cur = self.db_con.cursor()
        self.db = QSqlDatabase.addDatabase('QSQLITE', 'w2')
        self.db.setDatabaseName('CansatApp.db')
        self.db.open()
        self.tableButton.clicked.connect(self.open_table)
        self.plotButton.clicked.connect(self.build_plot)
        self.clearButton.clicked.connect(self.clear_plot)
        self.colorButton.clicked.connect(self.choose_color)
        self.symbolButton.clicked.connect(self.choose_symbol)

    def open_table(self):
        self.name = f"FLight{self.tableBox.value()}"
        self.table = Table(self.name, self, self.db)
        self.table.show()
        self.table.exec()
        self.axx, self.axy = self.table.display_axis()
        self.table_inf = self.db_cur.execute(f"""PRAGMA table_info(
              {self.name}
              );""").fetchall()
        self.yEdit.setText(self.table_inf[self.axy][1])
        self.xEdit.setText(self.table_inf[self.axx][1])

    def build_plot(self):
        self.x_coordsa = self.db_cur.execute(
            f"""SELECT {self.table_inf[self.axx][1]} FROM {self.name}""").fetchall()
        self.y_coordsa = self.db_cur.execute(
            f"""SELECT {self.table_inf[self.axy][1]} FROM {self.name}""").fetchall()
        self.x_coords, self.y_coords = [], []
        for i in range(len(self.x_coordsa)):
            self.x_coords.extend(self.x_coordsa[i])
            self.y_coords.extend(self.y_coordsa[i])
        self.plotView.showGrid(x=True, y=True)
        pen = pg.mkPen(color=self.color, width=1, style=QtCore.Qt.DashLine)
        if self.symbol:
            self.plotView.plot(self.x_coords, self.y_coords, symbol=self.symbol, pen=pen)
        else:
            self.plotView.plot(self.x_coords, self.y_coords, pen=pen)

    def clear_plot(self):
        self.plotView.clear()

    def choose_color(self):
        self.color = QColorDialog.getColor()

    def choose_symbol(self):
        self.symboldialog = SymbolDialog(self)
        self.symboldialog.show()
        self.symboldialog.exec()
        self.symbol = self.symboldialog.return_data()


class Table(QDialog):
    def __init__(self, name, widget, db):
        super().__init__()
        uic.loadUi('Table.ui', self)
        self.widget = widget
        self.ax = None
        self.axx = 0
        self.axy = 0
        self.db = db
        self.chsxButton.clicked.connect(self.save_axx)
        self.chsyButton.clicked.connect(self.save_axy)
        self.model = QSqlTableModel(self, self.db)
        self.model.setTable(name)
        self.model.select()
        self.display_data()
        self.dbView.selectionModel().selectionChanged.connect(self.choose_ax)
        self.closeButton.clicked.connect(self.accept_data)

    def display_data(self):
        self.dbView.setModel(self.model)

    def choose_ax(self, selected):
        self.ax = selected.indexes()[0].column()

    def save_axx(self):
        self.axx = self.ax

    def save_axy(self):
        self.axy = self.ax

    def display_axis(self):
        return self.axx, self.axy

    def accept_data(self):
        self.close()


class SymbolDialog(QDialog):
    def __init__(self, widget):
        super().__init__()
        uic.loadUi('Symbol.ui', self)
        self.widget = widget
        self.symbol = None
        self.buttonBox.accepted.connect(self.accept_data)
        self.buttonBox.rejected.connect(self.reject_data)

    def accept_data(self):
        self.symbol = self.symbolEdit.text()
        self.close()

    def reject_data(self):
        self.symbol = None
        self.close()

    def return_data(self):
        return self.symbol
