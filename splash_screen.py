from PyQt6.QtWidgets import (QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QIcon
from paths import img_path
from background import BackgroundWidget

class SplashScreen(BackgroundWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window

        layout = QVBoxLayout(self)
        layout.setContentsMargins(26, 26, 26, 26)
        layout.setSpacing(14)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # картинка
        soroban = QLabel()
        pixmap = QPixmap(img_path("soroban.png"))
        pixmap = pixmap.scaledToWidth(200, Qt.TransformationMode.SmoothTransformation)
        soroban.setPixmap(pixmap)
        soroban.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # заголовок — уровень display (40px, не жирный)
        title = QLabel("Тренажёр устного счёта")
        title.setObjectName("display")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # подпись под заголовком (стиль #subtitle из styles.py)
        subtitle = QLabel("Ментальная арифметика — считай в уме как на счётах")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # две кнопки в ряд (с иконками), размер 230×70.
        # стиль — общий из styles.py (#accentBig / #big), здесь только размер и иконка
        buttons_row = QHBoxLayout()
        buttons_row.setSpacing(12)
        buttons_row.setAlignment(Qt.AlignmentFlag.AlignCenter)

        login_btn = QPushButton("Вход")
        login_btn.setObjectName("accentBig")
        login_btn.setFixedSize(230, 70)
        login_btn.setIcon(QIcon(img_path("icon_login.png")))
        login_btn.setIconSize(QSize(22, 22))
        login_btn.clicked.connect(self.open_login)

        register_btn = QPushButton("Регистрация")
        register_btn.setObjectName("big")
        register_btn.setFixedSize(230, 70)
        register_btn.setIcon(QIcon(img_path("icon_register.png")))
        register_btn.setIconSize(QSize(22, 22))
        register_btn.clicked.connect(self.open_register)

        buttons_row.addWidget(login_btn)
        buttons_row.addWidget(register_btn)

        # надпись автора (тот же приглушённый стиль #subtitle)
        author = QLabel("Автор: Щипер Н., группа С422")
        author.setObjectName("subtitle")
        author.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(soroban)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(6)
        layout.addLayout(buttons_row)
        layout.addSpacing(22)
        layout.addWidget(author)

    def open_login(self):
        self.main.go_to(self.main.login)

    def open_register(self):
        self.main.go_to(self.main.register)