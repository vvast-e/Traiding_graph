from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton
from PyQt6.QtGui import QColor


class GridDisplay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.rows = 10
        self.cols = 10
        self.current_index = 0  # Текущая позиция для заполнения

        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)
        self.setFixedSize(700, 400)

        # Создаем ячейки
        self.cells = []
        for row in range(self.rows):
            row_cells = []
            for col in range(self.cols):
                cell = QPushButton()
                cell.setFixedSize(30, 30)
                cell.setStyleSheet("background-color: white;")
                self.grid_layout.addWidget(cell, row, col)
                row_cells.append(cell)
            self.cells.append(row_cells)

    def update_grid(self, data):
        """Обновляет сетку по данным"""
        for row in range(self.rows):
            for col in range(self.cols):
                color, digit = data[row][col]
                cell = self.cells[row][col]
                cell.setStyleSheet(f"background-color: {color.name()};")
                if digit is not None:
                    cell.setText(str(digit))
                else:
                    cell.setText("")

    def add_next_cell(self, color, number):
        """Добавляет цвет и номер в следующую ячейку"""
        row = self.current_index // self.cols
        col = self.current_index % self.cols

        cell = self.cells[row][col]
        cell.setStyleSheet(f"background-color: {color.name()};")
        if number==0:
            cell.setText("")
        else:
            cell.setText(str(number))

        self.current_index += 1