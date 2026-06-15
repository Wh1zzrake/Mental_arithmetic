from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton)
from PyQt6.QtCore import Qt


# ---------- список тренажёров ----------
class TrainerListScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window

        layout = QVBoxLayout(self)
        layout.setContentsMargins(26, 26, 26, 26)
        layout.setSpacing(11)

        title = QLabel("Тренажёр")
        title.setObjectName("h1")
        layout.addWidget(title)

        types = [
            "Умножение на 11",
            "Квадраты чисел на 5",
            "Проценты",
            "Признаки делимости",
            "Сложение / вычитание",
            "Умножение на 5 / 9 / 25",
            "Вперемешку",
        ]
        for name in types:
            btn = QPushButton(name)
            btn.clicked.connect(lambda _, n=name: self.open_trainer(n))
            layout.addWidget(btn)

        menu_btn = QPushButton("В главное меню")
        menu_btn.clicked.connect(lambda: self.main.go_to(self.main.menu))
        layout.addWidget(menu_btn)

    def open_trainer(self, name):
        # позже сюда передаётся выбранный генератор
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

        # ----- кнопки -----
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
