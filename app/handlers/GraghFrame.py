from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QPen, QLinearGradient, QBrush, QCursor
from PyQt6.QtCore import Qt, QPoint

import random


class GraphFrame(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.data = [(0,0,0)]  # [(x, y, color)]
        self.colors = [QColor(255, 0, 0), QColor(0, 255, 0), QColor(0, 0, 255)]
        self.scale_x = 50  # 1 единица X = 50 пикселей
        self.scale_y = 44  # 1 единица Y ≈ 44 пикселя
        self.origin_x = 50  # Отступ слева
        self.origin_y = 240  # Центр по Y (высота 480 / 2)
        self.setFixedSize(700, 480)  # График всегда 700x480

        # Перетаскивание
        self.dragging = False
        self.last_mouse_pos = QPoint()

        # Режим автоскролла
        self.auto_scroll = True  # По умолчанию включен


    def add_point(self, force, direction, color, number):
        x = len(self.data)
        y = 0
        if self.data:
            prev_y = self.data[-1][1]
            if direction == "вверх":
                y = prev_y + force
            else:
                y = prev_y - force

        new_point = (x, y, color, number)
        self.data.append(new_point)
        self.setMinimumWidth(max(self.minimumWidth(), self.origin_x + x * self.scale_x + 100))
        self.update()

        if self.main_window is not None:
            self.main_window.auto_scroll_to_last_point()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.last_mouse_pos = event.position().toPoint()
            self.setCursor(QCursor(Qt.CursorShape.ClosedHandCursor))

            # При начале перетаскивания выключаем автоскролл
            self.auto_scroll = False
            if self.main_window is not None:
                self.main_window.follow_button.setChecked(False)

    def mouseMoveEvent(self, event):
        if self.dragging and self.main_window is not None:
            delta = event.position().toPoint() - self.last_mouse_pos

            h_scroll = self.main_window.scroll_area.horizontalScrollBar()
            v_scroll = self.main_window.scroll_area.verticalScrollBar()

            h_scroll.setValue(h_scroll.value() - delta.x())
            v_scroll.setValue(v_scroll.value() - delta.y())

            self.last_mouse_pos = event.position().toPoint()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
            self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)

        # Фон
        painter.fillRect(self.rect(), QColor(40, 40, 40))  # Темно-серый цвет

        # Оси
        pen = QPen(Qt.GlobalColor.white, 2)
        painter.setPen(pen)

        # Ось OY — фиксированная (от верха до низа графика)
        painter.drawLine(int(self.origin_x), 0, int(self.origin_x), self.height())  # Полностью от верха до низа

        # Ось OX — горизонтальная
        painter.drawLine(int(self.origin_x), int(self.origin_y), int(self.width() - 50), int(self.origin_y))

        # Подписи на оси Y (от -5 до 5)
        for i in range(-5, 6):  # Диапазон от -5 до 5
            y = self.origin_y - i * self.scale_y  # Расположение деления
            if 0 <= y <= self.height():  # Проверяем, чтобы деление находилось внутри области
                y_int = int(y)
                painter.drawLine(int(self.origin_x) - 5, y_int, int(self.origin_x) + 5, y_int)  # Деление
                #painter.drawText(20, y_int + 5, str(i))  # Подпись

        # Подписи на оси X
        max_x = len(self.data) if self.data else 10
        for i in range(1, max_x + 1):
            x_pos = self.origin_x + i * self.scale_x
            if self.origin_x <= x_pos <= self.width() - 50:
                x_int = int(x_pos)
                painter.drawLine(x_int, int(self.origin_y - 5), x_int, int(self.origin_y + 5))

        # Рисуем график
        pen.setWidth(2)
        for i in range(len(self.data) - 1):
            x1, y1 = self.data[i][0], self.data[i][1]
            x2, y2 = self.data[i + 1][0], self.data[i + 1][1]
            color = self.data[i+1][2]

            screen_x1 = self.origin_x + x1 * self.scale_x
            screen_y1 = self.origin_y - y1 * self.scale_y
            screen_x2 = self.origin_x + x2 * self.scale_x
            screen_y2 = self.origin_y - y2 * self.scale_y

            painter.setPen(color)
            painter.drawLine(int(screen_x1), int(screen_y1), int(screen_x2), int(screen_y2))
            painter.drawEllipse(int(screen_x2) - 4, int(screen_y2) - 4, 8, 8)
