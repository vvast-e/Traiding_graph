import random
import sys

from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QFrame, QApplication, QPushButton, \
    QScrollArea
from PyQt6.QtCore import QTimer, Qt

from handlers.GraghFrame import GraphFrame
from handlers.IntervalSettings import IntervalSettings
from handlers.indicators import Indicators
from handlers.Keyboard import Keyboard
from handlers.GridDisplay import GridDisplay


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Графический Интерфейс")
        self.setGeometry(100, 100, 1000, 600)

        # Основной layout
        main_layout = QVBoxLayout()

        # Фрейм для графика / сетки
        self.display_widget = QFrame()
        self.display_widget.setMaximumWidth(700)
        self.display_layout = QVBoxLayout(self.display_widget)

        # График
        self.graph_frame = GraphFrame(main_window=self)

        # Горизонтальная и вертикальная прокрутка для графика
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(False)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setWidget(self.graph_frame)

        # Сетка
        self.grid_display = GridDisplay(self)

        # Добавляем оба виджета, но скрываем один из них
        self.display_layout.addWidget(self.scroll_area)
        self.display_layout.addWidget(self.grid_display)
        self.grid_display.hide()

        # Кнопка "Слежение"
        self.follow_button = QPushButton("Слежение")
        self.follow_button.setCheckable(True)
        self.follow_button.setChecked(True)
        self.follow_button.clicked.connect(self.toggle_follow_mode)
        self.display_layout.addWidget(self.follow_button)

        # Переключатель
        self.switch_button = QPushButton("Переключить отображение")
        self.switch_button.clicked.connect(self.toggle_display)
        self.display_layout.addWidget(self.switch_button)

        # Клавиатура ввода
        keyboard = Keyboard(self)
        self.display_layout.addWidget(keyboard)

        # Собираем всё вместе
        main_layout.addWidget(self.display_widget)  # График и сетка

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Таймер для обновления данных
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)  # Обновление каждую секунду

    def toggle_follow_mode(self, checked):
        self.graph_frame.auto_scroll = checked
        self.follow_button.setText("Слежение" if checked else "Слежение: ВЫКЛ")

    def toggle_display(self):
        if self.grid_display.isVisible():
            self.grid_display.hide()
            self.scroll_area.show()
        else:
            self.scroll_area.hide()
            self.grid_display.show()

    def update_data(self):
        """Обновление данных для обоих типов отображения"""
        self.graph_frame.update_data()

        grid_data = []
        for row in range(10):
            row_data = []
            for col in range(10):
                color = random.choice([QColor(255, 0, 0), QColor(0, 255, 0), QColor(0, 0, 255)])
                digit = random.randint(0, 9) if random.random() > 0.5 else None
                row_data.append((color, digit))
            grid_data.append(row_data)
        self.grid_display.update_grid(grid_data)

    def auto_scroll_to_last_point(self):
        """Автоматически прокручивает к последней точке графика так, чтобы она была в центре"""
        if not self.graph_frame.data or not self.graph_frame.auto_scroll:
            return

        last_x, last_y, color = self.graph_frame.data[-1]

        screen_x = self.graph_frame.origin_x + last_x * self.graph_frame.scale_x
        screen_y = self.graph_frame.origin_y - last_y * self.graph_frame.scale_y

        viewport_width = self.scroll_area.viewport().width()
        viewport_height = self.scroll_area.viewport().height()

        h_scroll = self.scroll_area.horizontalScrollBar()
        v_scroll = self.scroll_area.verticalScrollBar()

        h_scroll.setValue(int(screen_x - viewport_width // 2))
        v_scroll.setValue(int(screen_y - viewport_height // 2))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())