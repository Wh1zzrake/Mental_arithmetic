# trainer_screen.py
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QLabel, QLineEdit, QPushButton, QFrame)
from PyQt6.QtCore import Qt


# ---------- список тренажёров ----------
class TrainerListScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window

        layout = QVBoxLayout(self)
        layout.setContentsMargins(26, 26, 26, 26)
        layout.setSpacing(16)

        title = QLabel("Выберите тип задания")
        title.setObjectName("h1")

        # ----- сетка карточек: 2 колонки -----
        grid = QGridLayout()
        grid.setSpacing(11)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)

        # (маркер-знак, название, ключ генератора)
        task_types = [
            ("×", "Умножение на 11",         "mult11"),
            ("²", "Квадраты чисел на 5",     "square5"),
            ("%", "Проценты",                "percent"),
            ("÷", "Признаки делимости",      "divisibility"),
            ("+", "Сложение / вычитание",    "add_sub"),
            ("×", "Умножение на 5 / 9 / 25", "mult_5_9_25"),
        ]
        # раскладываем по двум колонкам: i//2 — строка, i%2 — колонка
        for i, (marker, label, key) in enumerate(task_types):
            grid.addWidget(self._task_btn(marker, label, key), i // 2, i % 2)

        # акцентная кнопка «Вперемешку» во всю ширину
        mix_btn = QPushButton("⇄   Вперемешку")
        mix_btn.setObjectName("accent")
        mix_btn.clicked.connect(lambda: self._open("mix"))

        # контурная кнопка «В главное меню» во всю ширину
        back_btn = QPushButton("←  В главное меню")
        back_btn.clicked.connect(lambda: self.main.go_to(self.main.menu))

        layout.addWidget(title)
        layout.addLayout(grid)
        layout.addWidget(mix_btn)
        layout.addWidget(back_btn)
        layout.addStretch()

    def _task_btn(self, marker, label, key):
        """Создаёт одну карточку-кнопку с плашкой-маркером слева."""
        # QFrame вместо QPushButton — чтобы внутри был горизонтальный ряд
        frame = QFrame()
        frame.setObjectName("taskCard")
        frame.setStyleSheet("""
            QFrame#taskCard {
                background: #FFFFFF;
                border: 1px solid #E7DECF;
                border-radius: 10px;
            }
            QFrame#taskCard:hover { background: #FBF4E9; }
        """)
        frame.setCursor(Qt.CursorShape.PointingHandCursor)

        row = QHBoxLayout(frame)
        row.setContentsMargins(14, 11, 14, 11)
        row.setSpacing(12)

        # плашка-маркер со знаком (квадратик 28×28)
        m = QLabel(marker)
        m.setFixedSize(28, 28)
        m.setAlignment(Qt.AlignmentFlag.AlignCenter)
        m.setStyleSheet(
            "background:#FBEFD9; border-radius:7px;"
            "font-size:14px; font-weight:700; color:#C58A2E; border:none;"
        )

        lbl = QLabel(label)
        lbl.setStyleSheet(
            "font-size:14px; font-weight:600; color:#2A2118;"
            "background:transparent; border:none;"
        )

        row.addWidget(m)
        row.addWidget(lbl)
        row.addStretch()

        # нажатие через mousePressEvent (у QFrame нет сигнала clicked)
        frame.mousePressEvent = lambda e, k=key: self._open(k)
        return frame

    def _open(self, kind):
        """Переходим на рабочее окно с нужным типом."""
        self.main.trainer_work.set_kind(kind)
        self.main.go_to(self.main.trainer_work)


# ---------- рабочее окно тренажёра ----------
class TrainerWorkScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window

        layout = QVBoxLayout(self)
        layout.setContentsMargins(26, 26, 26, 26)
        layout.setSpacing(16)

        # ----- верхняя строка: чип с типом (слева) + счётчик (справа) -----
        top_row = QHBoxLayout()

        chip = QFrame()
        chip.setObjectName("chipFrame")
        chip_in = QHBoxLayout(chip)
        chip_in.setContentsMargins(13, 6, 14, 6)
        self.type_title = QLabel("Тип задания")
        self.type_title.setObjectName("chipText")
        chip_in.addWidget(self.type_title)

        self.counter = QLabel("Решено 0 · Верно 0")
        self.counter.setObjectName("muted")

        top_row.addWidget(chip)
        top_row.addStretch()
        top_row.addWidget(self.counter)

        # ----- большое равенство с оранжевым «?» -----
        self.task = QLabel('35² = <span style="color:#D9822B;">?</span>')
        self.task.setObjectName("equation")
        self.task.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ----- поле ввода — по центру, уже окна -----
        self.answer_input = QLineEdit()
        self.answer_input.setPlaceholderText("ответ")
        self.answer_input.setFixedWidth(360)
        self.answer_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        input_row = QHBoxLayout()
        input_row.addStretch()
        input_row.addWidget(self.answer_input)
        input_row.addStretch()

        # ----- подпись «Верно / Неверно» (зелёная) -----
        self.feedback = QLabel("Верно")
        self.feedback.setObjectName("success")
        self.feedback.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ----- нижний ряд кнопок: Ответ (шире) + К списку + Меню -----
        buttons_row = QHBoxLayout()
        answer_btn = QPushButton("✓  Ответ")
        answer_btn.setObjectName("accent")
        list_btn = QPushButton("К списку")
        list_btn.clicked.connect(lambda: self.main.go_to(self.main.trainer_list))
        menu_btn = QPushButton("Меню")
        menu_btn.clicked.connect(lambda: self.main.go_to(self.main.menu))
        buttons_row.addWidget(answer_btn, 2)
        buttons_row.addWidget(list_btn, 1)
        buttons_row.addWidget(menu_btn, 1)

        layout.addLayout(top_row)
        layout.addStretch()
        layout.addWidget(self.task)
        layout.addLayout(input_row)
        layout.addWidget(self.feedback)
        layout.addStretch()
        layout.addLayout(buttons_row)

    def set_kind(self, kind):
        """Вызывается из списка при выборе типа. Пока заглушка."""
        self.type_title.setText(kind)