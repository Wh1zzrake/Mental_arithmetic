from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QIcon
from paths import img_path


class LoginScreen(QWidget):
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

        # логотип-квадрат
        logo = QLabel()
        pixmap = QPixmap(img_path("logo.png"))
        pixmap = pixmap.scaledToWidth(64, Qt.TransformationMode.SmoothTransformation)
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Вход в аккаунт")
        title.setObjectName("h1")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Логин")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        enter_btn = QPushButton("Войти")
        enter_btn.setObjectName("accent")
        enter_btn.setIcon(QIcon(img_path("icon_login.png")))
        enter_btn.setIconSize(QSize(20, 20))
        enter_btn.clicked.connect(self.do_login)

        # ссылка-текст: серое "Нет аккаунта?" + оранжевое "Зарегистрироваться"
        register_link = QLabel(
            '<span style="color:#8A7355;">Нет аккаунта?</span> '
            '<a href="#" style="color:#D9822B; text-decoration:none;">Зарегистрироваться</a>'
        )
        register_link.setAlignment(Qt.AlignmentFlag.AlignCenter)
        register_link.linkActivated.connect(self.open_register)

        layout.addWidget(logo)
        layout.addWidget(title)
        layout.addSpacing(6)
        layout.addWidget(self.login_input)
        layout.addWidget(self.password_input)
        layout.addWidget(enter_btn)
        layout.addWidget(register_link)

        outer.addWidget(form)

    def do_login(self):
        # логика входа добавляется позже
        self.main.go_to(self.main.menu)

    def open_register(self):
        self.main.go_to(self.main.register)