import sys

from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QFrame, QApplication, QPushButton, QScrollArea, QLabel
from PyQt6.QtCore import Qt

from handlers.GridDisplay import GridDisplay
from handlers.GraghFrame import GraphFrame
from handlers.Keyboard import Keyboard


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Графический Интерфейс")
        self.setGeometry(100, 100, 1000, 600)

        # Основной layout
        main_layout = QVBoxLayout()

        # Фрейм для графика / сетки
        self.display_widget = QFrame()
        self.display_layout = QVBoxLayout(self.display_widget)
        self.display_widget.setFixedSize(700,480)

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

        self.buttons_widget = QWidget()
        self.buttons_layout =QHBoxLayout()
        self.buttons_widget.setFixedSize(270,40)

        self.follow_button = QPushButton("Слежение: ВКЛ")
        self.follow_button.setFixedSize(100, 20)
        self.follow_button.setCheckable(True)
        self.follow_button.setChecked(True)
        self.follow_button.clicked.connect(self.toggle_follow_mode)
        self.display_layout.addWidget(self.follow_button)

        # Переключатель
        self.switch_button = QPushButton("Переключить отображение")
        self.switch_button.setFixedSize(160, 20)
        self.switch_button.clicked.connect(self.toggle_display)
        self.display_layout.addWidget(self.switch_button)

        self.buttons_layout.addWidget(self.follow_button)
        self.buttons_layout.addWidget(self.switch_button)
        self.buttons_widget.setLayout(self.buttons_layout)

        # Клавиатура ввода
        self.keyboard_widget=QWidget()
        self.keyboard_widget.setFixedSize(700,120)
        self.keyboard_layout = QHBoxLayout()

        self.keyboard = Keyboard(main_window=self)
        self.keyboard_layout.addWidget(self.keyboard)

        self.keyboard_widget.setLayout(self.keyboard_layout)

        # Собираем всё вместе
        main_layout.addWidget(self.display_widget)  # График и сетка
        main_layout.addWidget(self.buttons_widget)
        main_layout.addWidget(self.keyboard_widget)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def toggle_follow_mode(self, checked):
        self.graph_frame.auto_scroll = checked
        self.follow_button.setText("Слежение: ВКЛ" if checked else "Слежение: ВЫКЛ")
    def toggle_display(self):
        if self.grid_display.isVisible():
            self.grid_display.hide()
            self.scroll_area.show()
        else:
            self.scroll_area.hide()
            self.grid_display.show()

    def auto_scroll_to_last_point(self):
        """Автоматически прокручивает к последней точке так, чтобы она была в центре"""
        if not self.graph_frame.data or not self.graph_frame.auto_scroll:
            return

        last_x, last_y = self.graph_frame.data[-1][0], self.graph_frame.data[-1][1]

        screen_x = self.graph_frame.origin_x + last_x * self.graph_frame.scale_x
        screen_y = self.graph_frame.origin_y - last_y * self.graph_frame.scale_y

        viewport_width = self.scroll_area.viewport().width()
        viewport_height = self.scroll_area.viewport().height()

        h_scroll = self.scroll_area.horizontalScrollBar()
        v_scroll = self.scroll_area.verticalScrollBar()

        h_scroll.setValue(int(screen_x - viewport_width // 2))
        v_scroll.setValue(int(screen_y - viewport_height // 2))

    def add_point(self):
        """Добавляет точку через клавиатуру"""
        default_color = QColor(255, 0, 0)  # например, красный
        self.keyboard.on_color_clicked(default_color)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())