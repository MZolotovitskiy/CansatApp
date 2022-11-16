from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QDialog
from PyQt5.QtGui import QPixmap
from W1 import W1
from W2 import W2


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.W1 = W1()
        self.W2 = W2()
        self.instr = InstrDialog()
        uic.loadUi('Wm.ui', self)
        self.w1Button.clicked.connect(self.open_w1)
        self.w2Button.clicked.connect(self.open_w2)
        self.instrButton.clicked.connect(self.instruction)

    def open_w1(self):
        self.W1.show()

    def open_w2(self):
        self.W2.show()

    def instruction(self):
        self.instr.show()


class InstrDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('instrDialog.ui', self)
        self.previousButton.hide()
        self.texts = [
            'Добро пожаловать в приложение CanSatApp - удобное приложение для обработки телеметрии, полученной после '
            'полёта аппарата формата cansat!',
            'Главное окно - простое и понятное окно, встречающее пользователя при открытии приложения, каждая'
            'представленная на нём кнопка открывает своё окно.',
            'Окно измнение данных предназначено для внесения данных в БД. При нажатии на кнопку всплывает'
            'диалоговое окно выбора файла с телеметрией, который потом будет внесён в БД. Дальше появится диалог выбора'
            'числа - номера под которым находится необходимая таблица, при отсутствии такой таблицы она будет создана.',
            'Окно для построение графиков предлагает пользователю возможности pyqtgraph для построения графика. Для '
            'того, чтобы построить график необходимо сначала ввести номер интересующей таблицы, затем при нажатии'
            'кнопки появится диалоговое окно, где выделением можно выбрать интересующие столбцы. При желании можно '
            'выбрать символ и цвет, и, график готов к построению.']
        self.images = ['None.png', 'Wm.png', 'W1.png', 'W2.png']
        self.image = None
        self.textnum = 0
        self.next_shown = True
        self.previous_shown = False
        self.instrEdit.setText(self.texts[self.textnum])
        self.nextButton.clicked.connect(self.next_page)
        self.previousButton.clicked.connect(self.previous_page)

    def next_page(self):
        self.textnum += 1
        self.instrEdit.setText(self.texts[self.textnum])
        self.image = QPixmap(self.images[self.textnum])
        self.piclabel.setPixmap(self.image)
        if self.textnum == 3:
            self.nextButton.hide()
            self.next_shown = False

        if not self.previous_shown:
            self.previousButton.show()
            self.previous_shown = True

    def previous_page(self):
        self.textnum -= 1
        self.instrEdit.setText(self.texts[self.textnum])
        self.image = QPixmap(self.images[self.textnum])
        self.piclabel.setPixmap(self.image)
        if self.textnum == 0:
            self.previousButton.hide()
            self.previous_shown = False

        if not self.next_shown:
            self.nextButton.show()
            self.next_shown = True
