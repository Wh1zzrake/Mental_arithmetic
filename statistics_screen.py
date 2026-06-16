from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QTableWidget, QPushButton, QFrame,
                             QHeaderView, QAbstractItemView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from paths import img_path


# делает таблицу «чистой»: без сетки, без нумерации строк, колонки на всю ширину
def clean_table(table):
    table.verticalHeader().setVisible(False)        # убрать номера строк слева
    table.setShowGrid(False)                        # убрать линии сетки
    table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
    table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
    table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    table.horizontalHeader().setSectionResizeMode(
        QHeaderView.ResizeMode.Stretch)             # колонки тянутся на всю ширину


# ---------- общая статистика (рейтинг) ----------
class OverallStatsScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window

        layout = QVBoxLayout(self)
        layout.setContentsMargins(26, 26, 26, 26)
        layout.setSpacing(16)

        # ----- заголовок: иконка-кубок (в цвет палитры) + текст -----
        title_row = QHBoxLayout()
        title_row.setSpacing(10)

        trophy = QLabel()
        pix = QPixmap(img_path("trophy.png"))
        pix = pix.scaledToWidth(30, Qt.TransformationMode.SmoothTransformation)
        trophy.setPixmap(pix)

        title = QLabel("Рейтинг пользователей")
        title.setObjectName("h1")

        title_row.addWidget(trophy)
        title_row.addWidget(title)
        title_row.addStretch()

        # 3 колонки, как в мокапе
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Место", "Ученик", "Лучший результат"])
        clean_table(self.table)

        # кнопка «В главное меню» — слева, по содержимому (не на всю ширину)
        back_btn = QPushButton("←  В главное меню")
        back_btn.clicked.connect(lambda: self.main.go_to(self.main.menu))
        back_row = QHBoxLayout()
        back_row.addWidget(back_btn)
        back_row.addStretch()

        layout.addLayout(title_row)
        layout.addWidget(self.table)
        layout.addLayout(back_row)


# ---------- личная статистика ----------
class PersonalStatsScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window

        layout = QVBoxLayout(self)
        layout.setContentsMargins(26, 26, 26, 26)
        layout.setSpacing(16)

        # ----- шапка пользователя: имя + группа -----
        self.user_name = QLabel("Имя: логин")
        self.user_name.setObjectName("h1")
        self.user_group = QLabel("Группа —")
        self.user_group.setObjectName("muted")
        head = QVBoxLayout()
        head.setSpacing(2)
        head.addWidget(self.user_name)
        head.addWidget(self.user_group)

        # ----- карточки-метрики (по центру) -----
        metrics_row = QHBoxLayout()
        metrics_row.setSpacing(16)
        for caption in ("Средний", "Лучший", "Точность тренажёров"):
            metrics_row.addWidget(self._metric(caption, "—"))

        # ----- история тестов -----
        history_label = QLabel("История тестов:")
        history_label.setObjectName("muted")

        self.history = QTableWidget(0, 4)
        self.history.setHorizontalHeaderLabels(["Дата", "Баллы", "Процент", "Оценка"])
        clean_table(self.history)

        back_btn = QPushButton("←  В главное меню")
        back_btn.clicked.connect(lambda: self.main.go_to(self.main.menu))
        back_row = QHBoxLayout()
        back_row.addWidget(back_btn)
        back_row.addStretch()

        layout.addLayout(head)
        layout.addLayout(metrics_row)
        layout.addWidget(history_label)
        layout.addWidget(self.history)
        layout.addLayout(back_row)

    def _metric(self, caption, value):
        card = QFrame()
        card.setObjectName("metric")
        box = QVBoxLayout(card)
        box.setContentsMargins(16, 14, 16, 14)
        box.setSpacing(4)

        cap = QLabel(caption)
        cap.setObjectName("muted")
        cap.setAlignment(Qt.AlignmentFlag.AlignCenter)   # подпись по центру
        val = QLabel(value)
        val.setObjectName("h1")
        val.setAlignment(Qt.AlignmentFlag.AlignCenter)   # число по центру

        box.addWidget(cap)
        box.addWidget(val)
        return card