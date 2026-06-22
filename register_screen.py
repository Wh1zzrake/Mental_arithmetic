from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QMessageBox)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from paths import img_path
from background import BackgroundWidget
import auth

class RegisterScreen(BackgroundWidget):
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

        title = QLabel("Создать аккаунт")
        title.setObjectName("display")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

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
        username = self.login_input.text().strip()
        password = self.password_input.text()
        name = self.name_input.text().strip()
        group = self.group_input.text().strip()

        # все поля обязательны
        if username == "" or password == "" or name == "" or group == "":
            QMessageBox.warning(self, "Регистрация", "Заполните все поля.")
            return

        # логин — длина от 3 до 20 символов
        if len(username) < 3 or len(username) > 20:
            QMessageBox.warning(self, "Регистрация",
                                "Логин должен быть от 3 до 20 символов.")
            return

        # логин — только латинские буквы, цифры и символы _ - .
        # Проверяем каждый символ; заодно это отсекает пробелы и кириллицу.
        for c in username:
            if not (("a" <= c <= "z") or ("A" <= c <= "Z")
                    or ("0" <= c <= "9") or c in "_-."):
                QMessageBox.warning(self, "Регистрация",
                                    "Логин может содержать только латинские "
                                    "буквы, цифры и символы _ - .")
                return

        # пароль — не короче 6 символов. Любые символы (буквы, цифры,
        # спецсимволы, пробелы) разрешены, но ничего из них не обязательно.
        if len(password) < 6:
            QMessageBox.warning(self, "Регистрация",
                                "Пароль должен быть не короче 6 символов.")
            return

        user = auth.register(username, password, name, group)
        if user is None:
            QMessageBox.warning(self, "Регистрация", "Такой логин уже занят.")
            return

        # успех: сразу логиним нового пользователя и ведём в меню (вариант Б)
        self.main.current_user = user
        self.login_input.clear()
        self.password_input.clear()
        self.name_input.clear()
        self.group_input.clear()
        self.main.go_to(self.main.menu)

    def go_back(self):
        self.main.go_to(self.main.splash)