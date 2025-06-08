from PyQt6.QtWidgets import QWidget, QPushButton, QGridLayout

class Indicators(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QGridLayout()

        # Создаем несколько индикаторов
        for i in range(6):
            indicator = QPushButton(f"Индикатор {i+1}")
            indicator.setStyleSheet("background-color: yellow;")
            layout.addWidget(indicator, i // 3, i % 3)

        self.setLayout(layout)