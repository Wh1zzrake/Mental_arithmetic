from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QFont


class BackgroundWidget(QWidget):
    def paintEvent(self, event):
        p = QPainter(self)
        p.fillRect(self.rect(), QColor("#FFFCF7"))        # фон окна
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setPen(QColor("#EFE6D6"))                        # бледный цвет знаков
        p.setFont(QFont("Manrope", 54, QFont.Weight.Bold))

        w = self.width()
        h = self.height()
        # четыре знака по углам
        p.drawText(45, 100, "+")
        p.drawText(w - 100, 115, "×")
        p.drawText(45, h - 45, "−")
        p.drawText(w - 110, h - 45, "÷")
        p.end()
