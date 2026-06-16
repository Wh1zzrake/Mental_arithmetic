# trainer_screen.py
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QFrame, QScrollArea)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor, QFont


# ---------- список тренажёров ----------
class TrainerListScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Шапка ──────────────────────────────────────────────────────────
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background: #FFFDF9;
                border-bottom: 1px solid #F0E8DA;
            }
        """)
        h_lay = QHBoxLayout(header)
        h_lay.setContentsMargins(26, 16, 26, 16)
        h_lay.setSpacing(14)

        # Иконка-логотип (квадрат с символом)
        logo = QLabel("⊞")
        logo.setFixedSize(38, 38)
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setStyleSheet("""
            background: #FBF4E9;
            border: 1px solid #E7DECF;
            border-radius: 10px;
            font-size: 20px;
            color: #D9822B;
        """)

        # Текст рядом с иконкой
        title_col = QVBoxLayout()
        title_col.setSpacing(2)
        title_lbl = QLabel("Тренажёр")
        title_lbl.setStyleSheet(
            "font-size: 20px; font-weight: 800; color: #2A2118;"
            "background: transparent; border: none;"
        )
        sub_lbl = QLabel("Выбери тип заданий")
        sub_lbl.setStyleSheet(
            "font-size: 12px; font-weight: 500; color: #8A7355;"
            "background: transparent; border: none;"
        )
        title_col.addWidget(title_lbl)
        title_col.addWidget(sub_lbl)

        h_lay.addWidget(logo)
        h_lay.addLayout(title_col)
        h_lay.addStretch()
        root.addWidget(header)

        # ── Тело ───────────────────────────────────────────────────────────
        body = QWidget()
        body_lay = QVBoxLayout(body)
        body_lay.setContentsMargins(26, 20, 26, 22)
        body_lay.setSpacing(8)

        # Метка-раздел
        section_lbl = QLabel("ТИПЫ ЗАДАНИЙ")
        section_lbl.setStyleSheet(
            "font-size: 11px; font-weight: 700; color: #8A7355;"
            "letter-spacing: 1px; background: transparent;"
        )
        body_lay.addWidget(section_lbl)
        body_lay.addSpacing(2)

        # Кнопки типов: (маркер, название, ключ генератора)
        task_types = [
            ("×",  "Умножение на 11",         "mult11"),
            ("²",  "Квадраты чисел на 5",     "square5"),
            ("%",  "Проценты",                "percent"),
            ("÷",  "Признаки делимости",      "divisibility"),
            ("+",  "Сложение / вычитание",    "add_sub"),
            ("×",  "Умножение на 5 / 9 / 25", "mult_5_9_25"),
        ]
        for marker, label, key in task_types:
            body_lay.addWidget(self._task_btn(marker, label, key))

        # Акцентная кнопка «Вперемешку»
        body_lay.addSpacing(6)
        mix_btn = QPushButton("⊕   Вперемешку — все типы")
        mix_btn.setStyleSheet("""
            QPushButton {
                background: #D9822B;
                color: #FFFFFF;
                border: none;
                border-radius: 10px;
                padding: 13px 16px;
                font-size: 14px;
                font-weight: 700;
                text-align: center;
            }
            QPushButton:hover   { background: #C0731F; }
            QPushButton:pressed { background: #A8631A; }
        """)
        mix_btn.clicked.connect(lambda: self._open("mix"))
        body_lay.addWidget(mix_btn)

        # Разделитель
        body_lay.addSpacing(10)
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("color: #F0E8DA;")
        body_lay.addWidget(line)
        body_lay.addSpacing(6)

        # Кнопка «В главное меню»
        back_btn = QPushButton("← В главное меню")
        back_btn.setStyleSheet("""
            QPushButton {
                background: #FFFFFF;
                color: #8A7355;
                border: 1px solid #E7DECF;
                border-radius: 10px;
                padding: 11px 16px;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton:hover { background: #FBF4E9; }
        """)
        back_btn.clicked.connect(lambda: self.main.go_to(self.main.menu))
        body_lay.addWidget(back_btn)

        root.addWidget(body)
        root.addStretch()

    def _task_btn(self, marker, label, key):
        """Создаёт одну строку-кнопку с плашкой-маркером."""
        # QFrame вместо QPushButton — чтобы внутри был горизонтальный ряд
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background: #FFFFFF;
                border: 1px solid #E7DECF;
                border-radius: 10px;
            }
            QFrame:hover { background: #FBF4E9; }
        """)
        frame.setCursor(Qt.CursorShape.PointingHandCursor)

        row = QHBoxLayout(frame)
        row.setContentsMargins(14, 10, 14, 10)
        row.setSpacing(12)

        # Плашка-маркер со знаком
        m = QLabel(marker)
        m.setFixedSize(28, 28)
        m.setAlignment(Qt.AlignmentFlag.AlignCenter)
        m.setStyleSheet("""
            background: #FBEFD9;
            border-radius: 7px;
            font-size: 14px;
            font-weight: 700;
            color: #C58A2E;
            border: none;
        """)

        # Название типа
        lbl = QLabel(label)
        lbl.setStyleSheet(
            "font-size: 14px; font-weight: 600; color: #2A2118;"
            "background: transparent; border: none;"
        )

        # Стрелка
        arrow = QLabel("›")
        arrow.setStyleSheet(
            "font-size: 18px; color: #C58A2E;"
            "background: transparent; border: none;"
        )

        row.addWidget(m)
        row.addWidget(lbl)
        row.addStretch()
        row.addWidget(arrow)

        # Нажатие через mousePressEvent (QFrame не имеет clicked)
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

        self.type_title = QLabel("Тип задания")
        self.type_title.setObjectName("h2")

        self.task = QLabel("35² = ?")
        self.task.setObjectName("equation")
        self.task.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.answer_input = QLineEdit()
        self.answer_input.setPlaceholderText("Ваш ответ")

        self.feedback = QLabel("")
        self.feedback.setObjectName("muted")
        self.feedback.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.counter = QLabel("Решено: 0   Правильно: 0")
        self.counter.setObjectName("muted")
        self.counter.setAlignment(Qt.AlignmentFlag.AlignCenter)

        answer_btn = QPushButton("Ответ")
        answer_btn.setObjectName("accent")

        buttons_row = QHBoxLayout()
        list_btn = QPushButton("В список тренажёров")
        list_btn.clicked.connect(lambda: self.main.go_to(self.main.trainer_list))
        menu_btn = QPushButton("В главное меню")
        menu_btn.clicked.connect(lambda: self.main.go_to(self.main.menu))
        buttons_row.addWidget(list_btn)
        buttons_row.addWidget(menu_btn)

        layout.addWidget(self.type_title)
        layout.addWidget(self.task)
        layout.addWidget(self.answer_input)
        layout.addWidget(answer_btn)
        layout.addWidget(self.feedback)
        layout.addWidget(self.counter)
        layout.addStretch()
        layout.addLayout(buttons_row)

    def set_kind(self, kind):
        """Вызывается из списка при выборе типа. Пока заглушка."""
        self.type_title.setText(kind)