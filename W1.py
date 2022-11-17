import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QFileDialog, QWidget, QInputDialog, QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel


class W1(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('W1.ui', self)
        self.db = QSqlDatabase.addDatabase('QSQLITE', 'w1')
        self.db.setDatabaseName('CansatApp.db')
        self.db_con = sqlite3.connect("CansatApp.db")
        self.db_cur = self.db_con.cursor()
        self.flight_num = int()
        self.data_file = str()
        self.format = str()
        self.column = int()
        self.data = None
        self.new_table = 'Flight0'
        self.names = self.db_cur.execute(f"""PRAGMA table_info({self.new_table})""").fetchall()
        self.columnBox.setMaximum(len(self.names) - 2)
        self.addButton.clicked.connect(self.add_table)
        self.showButton.clicked.connect(self.display_data)
        self.divButton.clicked.connect(self.refactor_data)
        self.chooseButton.clicked.connect(self.choose_table)

    def choose_table(self):
        flight_num = QInputDialog.getInt(self, "Номер полёта", "Выберите номер полёта?")
        self.new_table = f'Flight{flight_num[0]}'
        self.names = self.db_cur.execute(f"""PRAGMA table_info({self.new_table})""").fetchall()
        self.columnBox.setMaximum(len(self.names) - 2)

    def receive_data(self):
        data_file = QFileDialog.getOpenFileName(self)
        return data_file[0]

    def add_table(self):
        data = self.receive_data()
        try:
            self.db.close()
            self.names = open(data, mode="r", encoding="UTF-8").readlines()[0].split()
            table = f"""CREATE TABLE IF NOT EXISTS {self.new_table} ( \nPackets INTEGER PRIMARY KEY,"""
            for name in range(1, len(self.names) - 1):
                table += f"""\n{self.names[name]} REAL NOT NULL,"""
            table += f"""{self.names[-1]} REAL NOT NULL\n);"""
            self.db_cur.execute(table)
            self.add_data(data)
            self.display_data()
            self.db_con.commit()
            self.display_data()
        except FileNotFoundError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('Такого файла не существует')
            msg.setWindowTitle("Error")
            msg.exec_()

    def add_data(self, data=''):
        try:
            lines = open(data, mode="r", encoding="UTF-8").readlines()
            values = [[float(j) for j in i.split()] for i in lines[1::]]
            names = lines[0].split()
            add_data_request = f"""INSERT INTO {self.new_table}("""
            for i in range(1, len(names) - 1):
                add_data_request += f"""{names[i]}, """
            add_data_request += f"""{names[-1]}) VALUES({', '.join(('? ' * (len(names) - 1)).split())})"""
            for i in range(len(values)):
                self.db_cur.execute(add_data_request, tuple(values[i][1::]))
            self.db_con.commit()
        except ValueError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('Неправильный формат файлов')
            msg.setWindowTitle("Error")
            msg.exec_()

    def display_data(self):
        self.db.open()
        model = QSqlTableModel(self, self.db)
        model.setTable(self.new_table)
        model.select()
        self.dbView.setModel(model)

    def refactor_data(self):
        self.db.close()
        column = self.columnBox.value()
        n = self.nBox.value()
        column_values = self.db_cur.execute(f"""SELECT {self.names[column][1]} FROM {self.new_table}""").fetchall()
        for i in range(len(column_values)):
            self.db_cur.execute(
                f"""UPDATE {self.new_table} SET {self.names[column][1]} = {column_values[i][0] * 10 ** n}
              WHERE Packets = {i + 1}""")
        self.db_con.commit()
        self.display_data()
