from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from paths import img_path
from background import BackgroundWidget

class RegisterScreen(BackgroundWidget):
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

        # заголовок — уровень display (40px, не жирный)
        title = QLabel("Создать аккаунт")
        title.setObjectName("display")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # поля ввода — крупный стиль #big из styles.py
        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Логин")
        self.login_input.setObjectName("big")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setObjectName("big")

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Имя")
        self.name_input.setObjectName("big")

        self.group_input = QLineEdit()
        self.group_input.setPlaceholderText("Группа")
        self.group_input.setObjectName("big")

        # кнопки в ряд: «Зарегистрироваться» (широкая) + «Назад» (узкая), шрифт 24
        buttons_row = QHBoxLayout()
        buttons_row.setSpacing(12)

        register_btn = QPushButton("  Зарегистрироваться")
        register_btn.setObjectName("accentBig")
        register_btn.setMinimumWidth(300)
        register_btn.setIcon(QIcon(img_path("icon_register_white.png")))
        register_btn.setIconSize(QSize(22, 22))
        register_btn.clicked.connect(self.do_register)

        back_btn = QPushButton("  Назад")
        back_btn.setObjectName("big")
        back_btn.setMinimumWidth(150)
        back_btn.setIcon(QIcon(img_path("icon_back.png")))
        back_btn.setIconSize(QSize(22, 22))
        back_btn.clicked.connect(self.go_back)

        buttons_row.addWidget(register_btn)
        buttons_row.addWidget(back_btn, 1)

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