from PyQt6.QtWidgets import QWidget, QPushButton, QGridLayout
from PyQt6.QtGui import QColor


class Keyboard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QGridLayout()

        # Цвета
        colors = [
            QColor(255, 0, 0), QColor(0, 255, 0), QColor(0, 0, 255),
            QColor(255, 255, 0), QColor(255, 0, 255), QColor(0, 255, 255)
        ]
        for i, color in enumerate(colors):
            button = QPushButton()
            button.setStyleSheet(f"background-color: {color.name()};")
            button.clicked.connect(lambda _, c=color: self.select_color(c))
            layout.addWidget(button, 0, i)


        digits = [str(i) for i in range(10)]
        for i, digit in enumerate(digits):
            button = QPushButton(digit)
            button.clicked.connect(lambda _, d=digit: self.select_digit(d))
            layout.addWidget(button, 1, i)

        self.setLayout(layout)

    def select_color(self, color):
        print(f"Выбран цвет: {color.name()}")

    def select_digit(self, digit):
        print(f"Выбрана цифра: {digit}")