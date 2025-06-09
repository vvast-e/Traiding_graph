from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFormLayout, QLineEdit, QComboBox, QColorDialog, QDialog, \
    QHBoxLayout, QGridLayout
from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtCore import Qt


class TemplateButton(QPushButton):
    def __init__(self, color, number, parent=None):
        super().__init__(parent)
        self.color = color
        self.number = number
        self.setFixedSize(50, 50)

    def paintEvent(self, event):
        painter = QPainter(self)

        # Цветной круг
        painter.setBrush(self.color)
        painter.setPen(Qt.GlobalColor.black)
        painter.drawEllipse(10, 10, 30, 30)

        # Номер внутри
        painter.setPen(Qt.GlobalColor.white)
        if self.number == 0:
            painter.drawText(20, 30, "")
        else:
            painter.drawText(20, 30, str(int(self.number)))

class InputDialog(QDialog):
    def __init__(self, last_number=0, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Настройки Точки")

        self.force_input = QLineEdit()
        self.direction_combo = QComboBox()
        self.direction_combo.addItems(["вверх", "вниз"])
        self.save_button = QPushButton("Сохранить (Пробел)")

        layout = QFormLayout()
        layout.addRow("Сила:", self.force_input)
        layout.addRow("Направление:", self.direction_combo)
        layout.addRow(self.save_button)

        self.setLayout(layout)

        self.color = QColor(255, 0, 0)
        self.force = 0
        self.direction = "вверх"
        self.number = last_number + 1

        self.save_button.clicked.connect(self.accept)  # Сохранение по кнопке
        self.save_button.setShortcut(Qt.Key.Key_Space)  # Горячая клавиша Пробел

    def get_values(self):
        try:
            force = float(self.force_input.text())
            direction = self.direction_combo.currentText()
            return force, direction
        except Exception as e:
            print("Ошибка ввода:", e)
            return None

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Space or event.key() == Qt.Key.Enter or event.key() == Qt.Key.Return:
            self.accept()  # Сохранение при нажатии Пробела/Enter


class Keyboard(QWidget):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.color_buttons = []
        self.main_window = main_window
        self.number_input = QLineEdit()
        self.number_input.setPlaceholderText("Цифра")
        self.number_input.setFixedSize(60, 20)

        # Для уникальности чисел
        self.used_numbers = set()

        # Сохраняем параметры цветов: {QColor: (сила, направление)}
        self.color_params = {}

        # Фиксированные цвета (20 штук)
        fixed_colors = [
            QColor(255, 0, 0), QColor(0, 255, 0), QColor(0, 0, 255),
            QColor(255, 255, 0), QColor(255, 0, 255), QColor(0, 255, 255),
            QColor(128, 0, 0), QColor(0, 128, 0), QColor(0, 0, 128),
            QColor(128, 128, 0), QColor(128, 0, 128), QColor(0, 128, 128),
            QColor(255, 128, 0), QColor(128, 255, 0), QColor(0, 128, 255),
            QColor(255, 128, 128), QColor(128, 255, 128), QColor(128, 128, 255),
            QColor(255, 255, 128), QColor(255, 128, 255)
        ]

        # Создаём сетку для 20 кругов
        self.template_grid = QGridLayout()
        self.template_grid.setSpacing(5)

        # Добавляем круги
        for i, color in enumerate(fixed_colors):
            btn = TemplateButton(color=color, number=0)  # Без номера
            btn.clicked.connect(lambda _, c=color: self.on_color_clicked(c))
            self.template_grid.addWidget(btn, i // 10, i % 10)
            self.color_buttons.append(btn)

        # Основной layout
        grid_with_input = QHBoxLayout()
        grid_with_input.addLayout(self.template_grid)
        grid_with_input.addWidget(self.number_input)

        main_layout = QVBoxLayout()
        main_layout.addLayout(grid_with_input)
        self.setLayout(main_layout)

    def on_color_clicked(self, color):
        color_key = color.name()

        if color_key in self.color_params:
            force, direction = self.color_params[color_key]
            self.add_point(force, direction, color, self.color_buttons[self.get_button_index_by_color(color)])
        else:
            dialog = InputDialog(parent=self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                result = dialog.get_values()
                if not result:
                    return

                force, direction = result
                self.color_params[color_key] = (force, direction)
                self.add_point(force, direction, color)

        self.number_input.setText(str(int(self.number_input.text() or "0") + 1))

    def get_button_index_by_color(self, color):
        """Находит индекс круга по цвету"""
        for idx, btn in enumerate(self.color_buttons):
            if btn.color.name() == color.name():
                return idx
        return -1

    def add_point(self, force, direction, color, button=None):
        """Добавляет точку на график или в сетку"""
        number_text = self.number_input.text()
        if number_text.isdigit():
            number = int(number_text)
        else:
            number = 0

        while number < 9999 and number in self.used_numbers:
            number += 1
        self.used_numbers.add(number)

        # Если была передана кнопка — обновляем её номер
        if button:
            button.number = number
            button.update()

        # Добавляем точку
        if self.main_window.graph_frame.isVisible():
            self.main_window.graph_frame.add_point(force, direction, color, number)
        elif self.main_window.grid_display.isVisible():
            self.main_window.grid_display.add_next_cell(color, number)

        # Автоинкремент поля ввода
        self.number_input.setText(str(number + 1))