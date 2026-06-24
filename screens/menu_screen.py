from PyQt6.QtWidgets import (QVBoxLayout, QHBoxLayout, QGridLayout,
                             QLabel, QPushButton, QFrame, QWidget, QApplication)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QIcon

from core.paths import img_path
from core.background import BackgroundWidget


class MenuScreen(BackgroundWidget):
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
        pix = pix.scaledToWidth(64, Qt.TransformationMode.SmoothTransformation)
        logo.setPixmap(pix)

        greet_box = QVBoxLayout()
        greet_box.setSpacing(2)
        self.greeting = QLabel("Здравствуйте! ")
        self.greeting.setObjectName("greeting")
        subtitle = QLabel("Выберите раздел")
        subtitle.setObjectName("subtitle")
        greet_box.addWidget(self.greeting)
        greet_box.addWidget(subtitle)

        header.addWidget(logo)
        header.addLayout(greet_box)
        header.addStretch()

        # ----- сетка кнопок: 2 колонки -----
        grid = QGridLayout()
        grid.setSpacing(11)
        grid.setColumnStretch(0, 7)   # левая колонка ~70%
        grid.setColumnStretch(1, 3)   # правая колонка ~30%

        # левый столбец — действия
        learn_btn = self._menu_button("Обучение", "op_plus_accent.png", accent=True)
        learn_btn.clicked.connect(lambda: self.main.go_to(self.main.lesson))

        test_btn = self._menu_button("Тест", "op_minus.png")
        test_btn.clicked.connect(lambda: self.main.go_to(self.main.test))

        trainer_btn = self._menu_button("Тренажёр", "op_times.png")
        trainer_btn.clicked.connect(lambda: self.main.go_to(self.main.trainer_list))

        # правый столбец — статистика и выход
        personal_btn = self._menu_button("Личная статистика", "op_percent.png")
        personal_btn.clicked.connect(lambda: self.main.go_to(self.main.personal_stats))

        overall_btn = self._menu_button("Общая статистика", "op_plus.png")
        overall_btn.clicked.connect(lambda: self.main.go_to(self.main.overall_stats))

        exit_btn = self._menu_button("Выход", "icon_power.png")
        exit_btn.clicked.connect(self.show_exit_menu)

        # раскладка как на мокапе: слева действия, справа статистика + выход
        grid.addWidget(learn_btn,    0, 0)
        grid.addWidget(personal_btn, 0, 1)
        grid.addWidget(test_btn,     1, 0)
        grid.addWidget(overall_btn,  1, 1)
        grid.addWidget(trainer_btn,  2, 0)
        grid.addWidget(exit_btn,     2, 1)

        layout.addStretch(1)            # сверху отступ меньше — блок поднят выше центра
        layout.addLayout(header)
        layout.addSpacing(26)
        layout.addLayout(grid)
        layout.addStretch(2)            # снизу больше

        # полупрозрачное окно выхода (создаём один раз, прячем)
        self._build_exit_overlay()

    # создаёт кнопку меню с маркером-иконкой слева (чтобы не повторять код 6 раз)
    def _menu_button(self, text, icon_name, accent=False):
        # два пробела перед текстом — отступ от иконки, чтобы она не «заплывала» на текст
        btn = QPushButton("  " + text)
        btn.setObjectName("menuAccent" if accent else "menu")
        btn.setIcon(QIcon(img_path(icon_name)))
        btn.setIconSize(QSize(32, 32))
        return btn

    # ----- полупрозрачное окно «Выход» (затемнение + карточка с тремя кнопками) -----
    def _build_exit_overlay(self):
        # слой поверх всего меню; WA_StyledBackground — чтобы рисовался полупрозрачный фон из QSS
        self.overlay = QWidget(self)
        self.overlay.setObjectName("overlay")
        self.overlay.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.overlay.hide()

        ov = QVBoxLayout(self.overlay)
        ov.setAlignment(Qt.AlignmentFlag.AlignCenter)   # карточка по центру экрана

        card = QFrame()
        card.setObjectName("dialogCard")
        card.setFixedWidth(360)
        box = QVBoxLayout(card)
        box.setContentsMargins(22, 22, 22, 22)
        box.setSpacing(14)

        title = QLabel("Выход")
        title.setObjectName("h2")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        logout_btn = QPushButton("Выйти из аккаунта")
        logout_btn.setObjectName("big")
        logout_btn.clicked.connect(self.logout)

        quit_btn = QPushButton("Выйти из программы")
        quit_btn.setObjectName("accentBig")
        quit_btn.clicked.connect(QApplication.quit)

        close_btn = QPushButton("Закрыть")
        close_btn.setObjectName("big")
        close_btn.clicked.connect(self.overlay.hide)

        box.addWidget(title)
        box.addWidget(logout_btn)
        box.addWidget(quit_btn)
        box.addWidget(close_btn)

        ov.addWidget(card)

    # показать окно выхода: растянуть слой на весь экран и поднять поверх кнопок
    def show_exit_menu(self):
        self.overlay.resize(self.size())
        self.overlay.raise_()
        self.overlay.show()

    # если окно меняет размер — слой выхода тоже подгоняем под него
    def resizeEvent(self, event):
        if hasattr(self, "overlay"):
            self.overlay.resize(self.size())
        super().resizeEvent(event)

    # обновляет приветствие именем вошедшего пользователя
    def refresh(self):
        user = self.main.current_user
        name = user.get("username", "") if isinstance(user, dict) else ""
        self.greeting.setText(f"Здравствуйте, {name}" if name else "Здравствуйте!")

    def logout(self):
        self.overlay.hide()
        self.main.current_user = None
        self.main.go_to(self.main.login)
