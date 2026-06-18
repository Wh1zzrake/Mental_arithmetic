# trainer_screen.py
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QLabel, QLineEdit, QPushButton, QFrame)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap
from paths import img_path
from background import BackgroundWidget
import generators                      # генераторы заданий (text, answer)

# ---------- список тренажёров ----------
class TrainerListScreen(BackgroundWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window

        layout = QVBoxLayout(self)
        layout.setContentsMargins(26, 26, 26, 26)
        layout.setSpacing(16)

        title = QLabel("Выберите тип задания")
        title.setObjectName("sectionTitle")

        grid = QGridLayout()
        grid.setSpacing(11)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)

        task_types = [
            ("×", "Умножение на 11",         "mult11"),
            ("²", "Квадраты чисел на 5",     "square5"),
            ("%", "Проценты",                "percent"),
            ("÷", "Признаки делимости",      "divisibility"),
            ("+", "Сложение / вычитание",    "add_sub"),
            ("×", "Умножение на 5 / 9 / 25", "mult_5_9_25"),
        ]
        for i, (marker, label, key) in enumerate(task_types):
            grid.addWidget(self._task_btn(marker, label, key), i // 2, i % 2)

        mix_btn = QPushButton("  Вперемешку")
        mix_btn.setObjectName("accentBig")
        mix_btn.setIcon(QIcon(img_path("icon_shuffle.png")))
        mix_btn.setIconSize(QSize(24, 24))
        mix_btn.clicked.connect(lambda: self._open("mix"))

        back_btn = QPushButton("  В главное меню")
        back_btn.setObjectName("big")
        back_btn.setIcon(QIcon(img_path("icon_back.png")))
        back_btn.setIconSize(QSize(24, 24))
        back_btn.clicked.connect(lambda: self.main.go_to(self.main.menu))

        layout.addStretch()
        layout.addWidget(title)
        layout.addLayout(grid)
        layout.addWidget(mix_btn)
        layout.addWidget(back_btn)
        layout.addStretch()

    def _task_btn(self, marker, label, key):
        frame = QFrame()
        frame.setObjectName("taskCard")
        frame.setCursor(Qt.CursorShape.PointingHandCursor)

        row = QHBoxLayout(frame)
        row.setContentsMargins(14, 11, 14, 11)
        row.setSpacing(12)

        m = QLabel(marker)
        m.setObjectName("marker")
        m.setFixedSize(28, 28)
        m.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lbl = QLabel(label)
        lbl.setObjectName("cardText")

        row.addWidget(m)
        row.addWidget(lbl)
        row.addStretch()

        frame.mousePressEvent = lambda e, k=key: self._open(k)
        return frame

    def _open(self, kind):
        self.main.trainer_work.set_kind(kind)
        self.main.go_to(self.main.trainer_work)


# ---------- рабочее окно тренажёра ----------
class TrainerWorkScreen(BackgroundWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window

        # --- состояние сессии ---
        self.current_kind = "mix"      # какой тип сейчас решаем
        self.current_answer = None     # правильный ответ текущего задания
        self.solved = 0                # сколько всего решено
        self.correct = 0               # сколько из них верно

        layout = QVBoxLayout(self)
        layout.setContentsMargins(26, 26, 26, 26)
        layout.setSpacing(16)

        top_row = QHBoxLayout()

        self.type_title = QLabel("Тип задания")
        self.type_title.setObjectName("chipBig")

        self.counter = QLabel("Решено 0 · Верно 0")
        self.counter.setObjectName("muted")

        top_row.addWidget(self.type_title)
        top_row.addStretch()
        top_row.addWidget(self.counter)

        self.task = QLabel('35² = <span style="color:#D9822B;">?</span>')
        self.task.setObjectName("equation")
        self.task.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.answer_input = QLineEdit()
        self.answer_input.setPlaceholderText("ответ")
        self.answer_input.setFixedWidth(360)
        self.answer_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.answer_input.returnPressed.connect(self.check_answer)   # Enter = «Ответ»
        input_row = QHBoxLayout()
        input_row.addStretch()
        input_row.addWidget(self.answer_input)
        input_row.addStretch()

        self.feedback_icon = QLabel()
        pix = QPixmap(img_path("icon_correct.png"))
        pix = pix.scaledToWidth(20, Qt.TransformationMode.SmoothTransformation)
        self.feedback_icon.setPixmap(pix)

        self.feedback = QLabel("Верно")
        self.feedback.setObjectName("success")

        feedback_row = QHBoxLayout()
        feedback_row.setSpacing(6)
        feedback_row.addStretch()
        feedback_row.addWidget(self.feedback_icon)
        feedback_row.addWidget(self.feedback)
        feedback_row.addStretch()

        answer_btn = QPushButton("  Ответ")
        answer_btn.setObjectName("accentBig")
        answer_btn.setIcon(QIcon(img_path("icon_check.png")))
        answer_btn.setIconSize(QSize(22, 22))
        answer_btn.clicked.connect(self.check_answer)                # проверка ответа

        list_btn = QPushButton("  К списку")
        list_btn.setObjectName("big")
        list_btn.setIcon(QIcon(img_path("icon_list.png")))
        list_btn.setIconSize(QSize(22, 22))
        list_btn.clicked.connect(lambda: self.main.go_to(self.main.trainer_list))

        menu_btn = QPushButton("  Меню")
        menu_btn.setObjectName("big")
        menu_btn.setIcon(QIcon(img_path("icon_home.png")))
        menu_btn.setIconSize(QSize(22, 22))
        menu_btn.clicked.connect(lambda: self.main.go_to(self.main.menu))

        secondary_row = QHBoxLayout()
        secondary_row.setSpacing(11)
        secondary_row.addWidget(list_btn)
        secondary_row.addWidget(menu_btn)

        btn_col = QVBoxLayout()
        btn_col.setSpacing(11)
        btn_col.addWidget(answer_btn)
        btn_col.addLayout(secondary_row)

        btn_box = QWidget()
        btn_box.setFixedWidth(440)
        btn_box.setLayout(btn_col)
        btn_wrap = QHBoxLayout()
        btn_wrap.addStretch()
        btn_wrap.addWidget(btn_box)
        btn_wrap.addStretch()

        layout.addLayout(top_row)
        layout.addStretch()
        layout.addWidget(self.task)
        layout.addLayout(input_row)
        layout.addLayout(feedback_row)
        layout.addSpacing(22)
        layout.addLayout(btn_wrap)
        layout.addStretch()

    def set_kind(self, kind):
        """Вызывается из списка при выборе типа: ставит название,
        обнуляет счётчики сессии и сразу даёт первое задание."""
        labels = {
            "mult11": "Умножение на 11",
            "square5": "Квадраты чисел на 5",
            "percent": "Проценты",
            "divisibility": "Признаки делимости",
            "add_sub": "Сложение / вычитание",
            "mult_5_9_25": "Умножение на 5 / 9 / 25",
            "mix": "Вперемешку",
        }
        self.type_title.setText(labels.get(kind, kind))

        # запоминаем тип и обнуляем сессию
        self.current_kind = kind
        self.solved = 0
        self.correct = 0
        self.counter.setText("Решено 0 · Верно 0")

        # прячем подпись до первого ответа (пробел держит высоту строки)
        self.feedback.setText(" ")
        self.feedback_icon.setVisible(False)

        # первое задание
        self.next_task()

    def next_task(self):
        """Берёт у генератора новое задание и показывает его."""
        text, answer = generators.random_task(self.current_kind)
        self.current_answer = answer
        # красим «?» в оранжевый, как в макете (QLabel понимает HTML)
        html = text.replace("?", '<span style="color:#D9822B;">?</span>')
        self.task.setText(html)
        self.answer_input.clear()
        self.answer_input.setFocus()   # курсор сразу в поле ввода

    def check_answer(self):
        """Проверяет введённый ответ, обновляет счётчик и даёт следующее задание."""
        user = self.answer_input.text().strip()
        if user == "":
            return                     # пустой ответ не засчитываем

        # сравниваем как текст в нижнем регистре —
        # работает и для чисел, и для ответа «да/нет» в делимости
        right = str(self.current_answer).strip().lower()
        self.solved += 1
        if user.lower() == right:
            self.correct += 1
            self.feedback.setText("Верно")
            self.feedback.setStyleSheet("color:#1C8A52; font-weight:600;")
            self.feedback_icon.setVisible(True)
        else:
            self.feedback.setText("Неверно")
            self.feedback.setStyleSheet("color:#C0392B; font-weight:600;")
            self.feedback_icon.setVisible(False)

        self.counter.setText(f"Решено {self.solved} · Верно {self.correct}")
        self.next_task()               # сразу следующее задание