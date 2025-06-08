from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel, QLineEdit

class IntervalSettings(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()

        # Интервалы
        intervals = [5, 15, 30]
        self.interval_buttons = []
        for interval in intervals:
            button = QPushButton(f"{interval} минут")
            button.clicked.connect(lambda _, i=interval: self.set_interval(i))
            layout.addWidget(button)
            self.interval_buttons.append(button)

        # Кастомный интервал
        custom_layout = QHBoxLayout()
        custom_layout.addWidget(QLabel("Кастомный интервал:"))
        self.custom_input = QLineEdit()
        custom_layout.addWidget(self.custom_input)
        layout.addLayout(custom_layout)

        self.setLayout(layout)

    def set_interval(self, interval):
        print(f"Интервал установлен: {interval}")