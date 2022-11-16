import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QFileDialog, QWidget, QInputDialog
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel


class W1(QWidget):

    def __init__(self):
        super().__init__()
        uic.loadUi('W1.ui', self)
        self.flight_num = int()
        self.data_file = str()
        self.format = str()
        self.column = int()
        self.data = None
        self.names = None
        self.new_table = 'Flight0'
        self.db = QSqlDatabase.addDatabase('QSQLITE', 'w1')
        self.db.setDatabaseName('CansatApp.db')
        self.db.open()
        self.db_con = sqlite3.connect("CansatApp.db")
        self.db_cur = self.db_con.cursor()
        self.addButton.clicked.connect(self.add_table)

    def receive_data(self):
        data_file = QFileDialog.getOpenFileName(self)
        flight_num = QInputDialog.getInt(self, "Номер полёта", "Выберите номер полёта?")
        return data_file[0], flight_num[0]

    def add_table(self):
        data, num = self.receive_data()
        self.names = open(data, mode="r", encoding="UTF-8").readlines()[0].split()
        self.new_table = f"Flight{num}"
        table = f"""CREATE TABLE IF NOT EXISTS {self.new_table} ( \nPackets INTEGER PRIMARY KEY,"""
        for name in range(1, len(self.names) - 1):
            table += f"""\n{self.names[name]} REAL NOT NULL,"""
        table += f"""{self.names[-1]} REAL NOT NULL\n);"""
        self.db_cur.execute(table)
        self.add_data(data, num)
        self.display_data(self.new_table)
        self.db_con.commit()

    def add_data(self, data='', num=0):
        if data == 0 and num == 0:
            data, num = self.receive_data()
        table = f"Flight{num}"
        lines = open(data, mode="r", encoding="UTF-8").readlines()
        values = [[float(j) for j in i.split()] for i in lines[1::]]
        names = lines[0].split()
        add_data_request = f"""INSERT INTO {table}("""
        for i in range(1, len(names) - 1):
            add_data_request += f"""{names[i]}, """
        add_data_request += f"""{names[-1]}) VALUES({', '.join(('? ' * (len(names) - 1)).split())})"""
        for i in range(len(values)):
            self.db_cur.execute(add_data_request, tuple(values[i][1::]))
        self.db_con.commit()

    def display_data(self, name):
        model = QSqlTableModel(self, self.db)
        model.setTable(name)
        model.select()
        self.dbView.setModel(model)
