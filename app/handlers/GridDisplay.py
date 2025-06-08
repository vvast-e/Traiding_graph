from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton


class GridDisplay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)

        # Размер сетки (например, 10x10)
        self.rows = 10
        self.cols = 10


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

        # Данные для отображения
        self.data = [[None for _ in range(self.cols)] for _ in range(self.rows)]

    def update_grid(self, data):
        """
        Обновляет сетку на основе входных данных.
        :param data: Список списков [(color, digit), ...]
        """
        for row in range(self.rows):
            for col in range(self.cols):
                color, digit = data[row][col]
                cell = self.cells[row][col]
                cell.setStyleSheet(f"background-color: {color.name()};")
                if digit is not None:
                    cell.setText(str(digit))
                else:
                    cell.setText("")