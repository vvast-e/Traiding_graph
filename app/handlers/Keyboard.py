from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFormLayout, QLineEdit, QComboBox, QColorDialog, QDialog, \
    QHBoxLayout, QGridLayout
from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtCore import Qt


class TemplateButton(QPushButton):
    def __init__(self, color, force, parent=None):
        super().__init__(parent)
        self.color = color
        self.force = force
        self.setFixedSize(50, 50)

    def paintEvent(self, event):
        painter = QPainter(self)

        # Цветной круг
        painter.setBrush(self.color)
        painter.setPen(Qt.GlobalColor.black)
        painter.drawEllipse(10, 10, 30, 30)

        # Номер внутри
        painter.setPen(Qt.GlobalColor.white)
        painter.drawText(20, 30, str(int(self.force)))


class InputDialog(QDialog):
    def __init__(self, last_number=0, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Настройки Точки")

        self.force_input = QLineEdit()
        self.direction_combo = QComboBox()
        self.direction_combo.addItems(["вверх", "вниз"])
        self.color_button = QPushButton("Выбрать цвет")
        self.number_input = QLineEdit(str(last_number + 1))
        self.save_button = QPushButton("Сохранить (Пробел)")

        layout = QFormLayout()
        layout.addRow("Сила:", self.force_input)
        layout.addRow("Направление:", self.direction_combo)
        layout.addRow("Цвет:", self.color_button)
        layout.addRow("Номер:", self.number_input)
        layout.addRow(self.save_button)

        self.setLayout(layout)

        self.color = QColor(255, 0, 0)
        self.force = 0
        self.direction = "вверх"
        self.number = last_number + 1

        self.color_button.clicked.connect(self.choose_color)
        self.save_button.clicked.connect(self.accept)  # Сохранение по кнопке
        self.save_button.setShortcut(Qt.Key.Key_Space)  # Горячая клавиша Пробел

    def choose_color(self):
        color = QColorDialog.getColor(initial=self.color, parent=self)
        if color.isValid():
            self.color = color
            self.color_button.setStyleSheet(f"background-color: {color.name()}; color: white;")

    def get_values(self):
        try:
            self.force = float(self.force_input.text())
            self.direction = self.direction_combo.currentText()
            self.number = int(self.number_input.text())
            return self.force, self.direction, self.color, self.number
        except Exception as e:
            print("Ошибка ввода:", e)
            return None

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Space or event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return:
            self.accept()  # Сохранение при нажатии Пробела/Enter


class Keyboard(QWidget):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.last_number = 0
        self.templates = []

        # Основной layout
        main_layout = QGridLayout()

        # Область шаблонов (сетка 2x10)
        self.template_grid = QGridLayout()
        self.template_grid.setSpacing(5)  # Расстояние между ячейками

        # Кнопка "Добавить точку"
        add_button = QPushButton("Добавить точку")
        add_button.setFixedSize(100, 30)

        add_button.clicked.connect(self.open_input_dialog)


        # Размещаем шаблоны и кнопку
        main_layout.addLayout(self.template_grid, 0,0,2,10)
        main_layout.addWidget(add_button, 0, 10, 2, 1)

        self.setLayout(main_layout)

    def open_input_dialog(self):
        dialog = InputDialog(self.last_number, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            result = dialog.get_values()
            if not result:
                return

            force, direction, color, number = result

            self.main_window.graph_frame.add_point(force, direction, color, number)
            self.main_window.grid_display.add_next_cell(color, number)

            # Сохраняем как шаблон
            btn = TemplateButton(color, number, self)
            btn.clicked.connect(lambda _, f=force, d=direction, c=color, n=number:
                                self.add_from_template(f, d, c, n))
            self.add_template_button(btn)

            self.last_number = number

    def add_template_button(self, button):
        """Добавляет кнопку шаблона в сетку"""
        row = len(self.templates) // 10  # Строка
        col = len(self.templates) % 10  # Столбец
        self.template_grid.addWidget(button, row, col)
        self.templates.append(button)

    def add_from_template(self, force, direction, color, number):
        if self.main_window.graph_frame.isVisible():
            self.main_window.graph_frame.add_point(force, direction, color, number)
        elif self.main_window.grid_display.isVisible():
            self.main_window.grid_display.add_next_cell(color, number)