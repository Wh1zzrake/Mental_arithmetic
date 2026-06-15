from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QTableWidget, QPushButton, QFrame)
from PyQt6.QtCore import Qt


# ---------- общая статистика (рейтинг) ----------
class OverallStatsScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window

        layout = QVBoxLayout(self)
        layout.setContentsMargins(26, 26, 26, 26)
        layout.setSpacing(16)

        title = QLabel("Общая статистика")
        title.setObjectName("h1")

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(
            ["Место", "Имя", "Группа", "Лучший результат"])

        back_btn = QPushButton("В главное меню")
        back_btn.clicked.connect(lambda: self.main.go_to(self.main.menu))

        layout.addWidget(title)
        layout.addWidget(self.table)
        layout.addWidget(back_btn)


# ---------- личная статистика ----------
class PersonalStatsScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window

        layout = QVBoxLayout(self)
        layout.setContentsMargins(26, 26, 26, 26)
        layout.setSpacing(16)

        title = QLabel("Личная статистика")
        title.setObjectName("h1")

        # ----- карточки-метрики -----
        metrics_row = QHBoxLayout()
        metrics_row.setSpacing(16)
        for caption in ("Средний результат", "Лучший результат", "Точность тренажёра"):
            metrics_row.addWidget(self._metric(caption, "—"))

        # ----- история тестов -----
        history_label = QLabel("ИСТОРИЯ ТЕСТОВ")
        history_label.setObjectName("muted")

        self.history = QTableWidget(0, 4)
        self.history.setHorizontalHeaderLabels(
            ["Дата", "Баллы", "Процент", "Оценка"])

        back_btn = QPushButton("В главное меню")
        back_btn.clicked.connect(lambda: self.main.go_to(self.main.menu))

        layout.addWidget(title)
        layout.addLayout(metrics_row)
        layout.addWidget(history_label)
        layout.addWidget(self.history)
        layout.addWidget(back_btn)

    def _metric(self, caption, value):
        card = QFrame()
        card.setObjectName("metric")
        box = QVBoxLayout(card)
        box.setContentsMargins(16, 16, 16, 16)

        cap = QLabel(caption)
        cap.setObjectName("muted")
        val = QLabel(value)
        val.setObjectName("h1")

        box.addWidget(cap)
        box.addWidget(val)
        return card
