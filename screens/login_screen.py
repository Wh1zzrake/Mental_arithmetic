from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit,
                             QPushButton, QMessageBox)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QIcon

from core.paths import img_path
from core.background import BackgroundWidget
from logic import auth


class LoginScreen(BackgroundWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window

        outer = QVBoxLayout(self)
        outer.setContentsMargins(26, 26, 26, 26)
        outer.setAlignment(Qt.AlignmentFlag.AlignCenter)

        form = QWidget()
        form.setFixedWidth(560)
        layout = QVBoxLayout(form)
        layout.setSpacing(14)

        logo = QLabel()
        pixmap = QPixmap(img_path("logo.png"))
        pixmap = pixmap.scaledToWidth(84, Qt.TransformationMode.SmoothTransformation)
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Вход в аккаунт")
        title.setObjectName("display")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Логин")
        self.login_input.setObjectName("big")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setObjectName("big")
        self.password_input.returnPressed.connect(self.do_login)   # Enter в поле - do_login()

        # глазик внутри поля пароля: показать/скрыть введённый пароль
        self.eye_icon_on = QIcon(img_path("icon_eye.png"))         # открытый глаз — пароль скрыт
        self.eye_icon_off = QIcon(img_path("icon_eye_off.png"))    # перечёркнутый глаз — пароль виден
        self.eye_action = self.password_input.addAction(           # иконка-кнопка справа внутри поля
            self.eye_icon_on, QLineEdit.ActionPosition.TrailingPosition)
        self.eye_action.triggered.connect(self.toggle_password)    # клик по глазику  toggle_password()

        enter_btn = QPushButton("  Войти")            # КНОПКА Войти
        enter_btn.setObjectName("accentBig")
        enter_btn.setIcon(QIcon(img_path("icon_login.png")))
        enter_btn.setIconSize(QSize(22, 22))
        enter_btn.clicked.connect(self.do_login)      #  обработчик do_login()

        register_link = QLabel(                       # ССЫЛКА-текст Зарегистрироваться
            '<span style="color:#8A7355;">Нет аккаунта?</span> '
            '<a href="#" style="color:#D9822B; text-decoration:none;">Зарегистрироваться</a>'
        )
        register_link.setStyleSheet("font-size:22px;")
        register_link.setAlignment(Qt.AlignmentFlag.AlignCenter)
        register_link.linkActivated.connect(self.open_register)   # клик по ссылке  open_register()

        layout.addWidget(logo)
        layout.addWidget(title)
        layout.addSpacing(6)
        layout.addWidget(self.login_input)
        layout.addWidget(self.password_input)
        layout.addWidget(enter_btn)
        layout.addWidget(register_link)

        outer.addWidget(form)

    def do_login(self):
        # обработчик КНОПКИ Войти (и Enter в поле пароля):
        # проверяет логин/пароль и при успехе переводит в меню
        username = self.login_input.text().strip()
        password = self.password_input.text()

        if username == "" or password == "":
            QMessageBox.warning(self, "Вход", "Введите логин и пароль.")
            return

        user = auth.check_login(username, password)
        if user is None:
            QMessageBox.warning(self, "Вход", "Неверный логин или пароль.")
            return

        # запоминаем вошедшего и переходим в меню
        self.main.current_user = user
        self.login_input.clear()
        self.password_input.clear()
        self.main.go_to(self.main.menu)

    def open_register(self):
        # обработчик ССЫЛКИ Зарегистрироваться: показать экран регистрации
        self.main.go_to(self.main.register)

    def toggle_password(self):
        # переключатель глазика: меняет режим отображения пароля и саму иконку
        if self.password_input.echoMode() == QLineEdit.EchoMode.Password:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)    # показать пароль
            self.eye_action.setIcon(self.eye_icon_off)                    # глаз перечёркнут
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)  # снова скрыть
            self.eye_action.setIcon(self.eye_icon_on)                     # глаз открыт