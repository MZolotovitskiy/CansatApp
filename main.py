import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QFileDialog, QTableWidgetItem, QMainWindow, QWidget, QInputDialog, QDialog
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from MainWindow import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
