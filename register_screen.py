from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from paths import img_path


class RegisterScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window

        # внешний слой — центрирует форму по окну
        outer = QVBoxLayout(self)
        outer.setContentsMargins(26, 26, 26, 26)
        outer.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # сама форма фиксированной ширины
        form = QWidget()
        form.setFixedWidth(560)
        layout = QVBoxLayout(form)
        layout.setSpacing(14)

        title = QLabel("Создать аккаунт")
        title.setObjectName("h1")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Логин")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Имя")

        self.group_input = QLineEdit()
        self.group_input.setPlaceholderText("Группа")

        # кнопки в ряд: «Зарегистрироваться» (широкая) + «Назад» (узкая)
        buttons_row = QHBoxLayout()
        buttons_row.setSpacing(12)

        register_btn = QPushButton("Зарегистрироваться")
        register_btn.setObjectName("accent")
        register_btn.setMinimumWidth(300)
        register_btn.setIcon(QIcon(img_path("icon_register_white.png")))
        register_btn.setIconSize(QSize(20, 20))
        register_btn.clicked.connect(self.do_register)

        back_btn = QPushButton("Назад")
        back_btn.setMinimumWidth(120)
        back_btn.setIcon(QIcon(img_path("icon_back.png")))
        back_btn.setIconSize(QSize(20, 20))
        back_btn.clicked.connect(self.go_back)

        buttons_row.addWidget(register_btn)
        buttons_row.addWidget(back_btn)
        buttons_row.addStretch()

        layout.addWidget(title)
        layout.addSpacing(6)
        layout.addWidget(self.login_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.name_input)
        layout.addWidget(self.group_input)
        layout.addLayout(buttons_row)

        outer.addWidget(form)

    def do_register(self):
        # логика регистрации + авто-вход добавляется позже
        self.main.go_to(self.main.menu)

    def go_back(self):
        self.main.go_to(self.main.splash)