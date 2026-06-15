from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QLabel, QPushButton, QApplication)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QIcon
from paths import img_path


class MenuScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window

        layout = QVBoxLayout(self)
        layout.setContentsMargins(26, 26, 26, 26)
        layout.setSpacing(16)

        # ----- шапка: логотип + приветствие -----
        header = QHBoxLayout()
        header.setSpacing(12)

        logo = QLabel()
        pix = QPixmap(img_path("logo.png"))
        pix = pix.scaledToWidth(48, Qt.TransformationMode.SmoothTransformation)
        logo.setPixmap(pix)

        greet_box = QVBoxLayout()
        greet_box.setSpacing(2)
        self.greeting = QLabel("Здравствуйте!")
        self.greeting.setObjectName("h1")
        subtitle = QLabel("Выберите раздел")
        subtitle.setObjectName("muted")
        greet_box.addWidget(self.greeting)
        greet_box.addWidget(subtitle)

        header.addWidget(logo)
        header.addLayout(greet_box)
        header.addStretch()

        # ----- сетка кнопок: 2 колонки -----
        grid = QGridLayout()
        grid.setSpacing(11)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)

        learn_btn = self._menu_button("Обучение", "op_plus_accent.png", accent=True)
        learn_btn.clicked.connect(lambda: self.main.go_to(self.main.lesson))

        test_btn = self._menu_button("Тест", "op_minus.png")
        test_btn.clicked.connect(lambda: self.main.go_to(self.main.test))

        trainer_btn = self._menu_button("Тренажёр", "op_times.png")
        trainer_btn.clicked.connect(lambda: self.main.go_to(self.main.trainer_list))

        overall_btn = self._menu_button("Общая статистика", "op_div.png")
        overall_btn.clicked.connect(lambda: self.main.go_to(self.main.overall_stats))

        personal_btn = self._menu_button("Личная статистика", "op_percent.png")
        personal_btn.clicked.connect(lambda: self.main.go_to(self.main.personal_stats))

        logout_btn = self._menu_button("Выйти из аккаунта", "op_equals.png")
        logout_btn.clicked.connect(self.logout)

        grid.addWidget(learn_btn,    0, 0)
        grid.addWidget(test_btn,     0, 1)
        grid.addWidget(trainer_btn,  1, 0)
        grid.addWidget(overall_btn,  1, 1)
        grid.addWidget(personal_btn, 2, 0)
        grid.addWidget(logout_btn,   2, 1)

        # ----- кнопка «Выход» во всю ширину -----
        quit_btn = QPushButton("Выход")
        quit_btn.setIcon(QIcon(img_path("icon_power.png")))
        quit_btn.setIconSize(QSize(18, 18))
        quit_btn.clicked.connect(QApplication.quit)

        layout.addStretch()
        layout.addLayout(header)
        layout.addSpacing(4)
        layout.addLayout(grid)
        layout.addWidget(quit_btn)
        layout.addStretch()

    # создаёт кнопку меню с маркером-иконкой слева (чтобы не повторять код 6 раз)
    def _menu_button(self, text, icon_name, accent=False):
        btn = QPushButton(text)
        btn.setObjectName("menuAccent" if accent else "menu")
        btn.setIcon(QIcon(img_path(icon_name)))
        btn.setIconSize(QSize(26, 26))
        return btn

    # обновляет приветствие именем вошедшего пользователя
    def refresh(self):
        user = self.main.current_user
        name = user.get("username", "") if isinstance(user, dict) else ""
        self.greeting.setText(f"Здравствуйте, {name}" if name else "Здравствуйте!")

    def logout(self):
        self.main.current_user = None
        self.main.go_to(self.main.login)