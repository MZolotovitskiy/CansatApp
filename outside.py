import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QFileDialog, QTableWidgetItem, QMainWindow, QWidget, QInputDialog
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel


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


class W1(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('W1.ui', self)
        self.flight_num = int()
        self.data_file = str()
        self.format = str()
        self.column = int()
        self.data = None
        self.db_con = sqlite3.connect("CansatApp.db")
        self.db_cur = self.db_con.cursor()
        self.addButton.clicked.connect(self.add_table)
        self.modButton.clicked.connect(self.add_data)

    def receive_data(self):
        data_file = QFileDialog.getOpenFileName(self)
        flight_num = QInputDialog.getInt(self, "Номер полёта", "Выберите номер полёта?")
        return data_file[0], flight_num[0]

    def add_table(self):
        data, num = self.receive_data()
        names = open(data, mode="r", encoding="UTF-8").readlines()[0].split()
        new_table = f"Flight{num}"
        table = f"""CREATE TABLE IF NOT EXISTS {new_table} ( \nPackets INTEGER PRIMARY KEY,"""
        for name in range(1, len(names) - 1):
            table += f"""\n{names[name]} REAL NOT NULL,"""
        table += f"""{names[-1]} REAL NOT NULL\n);"""
        self.db_cur.execute(table)
        self.db_con.commit()
        self.add_data(data, num)
        self.display_data(new_table)
        self.db_con.commit()

    def add_data(self, data='', num=0):
        if data == 0 and num == 0:
            data, num = self.receive_data()
        table = f"Flight{num}"
        lines = open(data, mode="r", encoding="UTF-8").readlines()
        values = [[float(j) for j in i.split()] for i in lines[1::]]
        names = lines[0].split()
        add_data_request = f"""INSERT INTO {table}("""
        for i in range(len(names) - 1):
            add_data_request += f"""{names[i]}, """
        add_data_request += f"""{names[-1]}) VALUES({', '.join(('? ' * len(names)).split())})"""
        print(add_data_request)
        for i in range(len(values)):
            self.db_cur.execute(add_data_request, tuple(values[i]))
        self.db_con.commit()

    def display_data(self, name):
        print(name)
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('CansatApp.db')
        db.open()
        model = QSqlTableModel(self, db)
        model.setTable(name)
        model.select()
        self.dbView.setModel(model)

    def closeEvent(self, event):
        pass


class W2(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('W2.ui', self)
        self.db_con = sqlite3.connect("CansatApp.db")
        self.graphButton.clicked.connect(self.build_graph)
        self.db = None

    def build_graph(self):
        self.db = QInputDialog.getInt(self, "Выбор величины", "По какому столбцу строим график?", 1, 3, 7)
