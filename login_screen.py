from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QIcon
from paths import img_path
from background import BackgroundWidget

class LoginScreen(BackgroundWidget):
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

        # логотип-квадрат (чуть крупнее — 84px)
        logo = QLabel()
        pixmap = QPixmap(img_path("logo.png"))
        pixmap = pixmap.scaledToWidth(84, Qt.TransformationMode.SmoothTransformation)
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # заголовок — уровень display (40px, не жирный)
        title = QLabel("Вход в аккаунт")
        title.setObjectName("display")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # общий стиль полей ввода со шрифтом 24 (пишем целиком,
        # чтобы не потерять рамку и скругление)
        field_style = (
            "QLineEdit{background:#FFFFFF; border:1px solid #E7DECF;"
            "border-radius:10px; padding:11px 14px; color:#2A2118; font-size:24px;}"
            "QLineEdit:focus{border:1px solid #D9822B;}"
        )

        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Логин")
        self.login_input.setStyleSheet(field_style)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet(field_style)

        # кнопка «Войти» — шрифт 24, стиль целиком (фон + шрифт)
        enter_btn = QPushButton("Войти")
        enter_btn.setStyleSheet(
            "QPushButton{background:#D9822B; color:#FFFFFF; border:none;"
            "border-radius:10px; padding:11px 15px; font-size:24px; font-weight:400;}"
            "QPushButton:hover{background:#C0731F;}"
            "QPushButton:pressed{background:#A8631A;}"
        )
        enter_btn.setIcon(QIcon(img_path("icon_login.png")))
        enter_btn.setIconSize(QSize(22, 22))
        enter_btn.clicked.connect(self.do_login)

        # ссылка-текст: серое "Нет аккаунта?" + оранжевое "Зарегистрироваться", шрифт 22
        register_link = QLabel(
            '<span style="color:#8A7355;">Нет аккаунта?</span> '
            '<a href="#" style="color:#D9822B; text-decoration:none;">Зарегистрироваться</a>'
        )
        register_link.setStyleSheet("font-size:22px;")
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