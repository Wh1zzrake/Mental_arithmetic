from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPainter, QColor, QFont, QPixmap, QIcon
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

        # картинка соробана из файла img/soroban.png
        soroban = QLabel()
        pixmap = QPixmap(img_path("soroban.png"))
        pixmap = pixmap.scaledToWidth(200, Qt.TransformationMode.SmoothTransformation)
        soroban.setPixmap(pixmap)
        soroban.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Тренажёр устного счёта")
        title.setObjectName("h1")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Ментальная арифметика — считай в уме как на счётах")
        subtitle.setObjectName("muted")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # две кнопки в ряд (с иконками)
        buttons_row = QHBoxLayout()
        buttons_row.setSpacing(12)
        buttons_row.setAlignment(Qt.AlignmentFlag.AlignCenter)

        login_btn = QPushButton("Вход")
        login_btn.setObjectName("accent")
        login_btn.setMinimumWidth(170)
        login_btn.setIcon(QIcon(img_path("icon_login.png")))
        login_btn.setIconSize(QSize(22, 22))
        login_btn.clicked.connect(self.open_login)

        register_btn = QPushButton("Регистрация")
        register_btn.setMinimumWidth(170)
        register_btn.setIcon(QIcon(img_path("icon_register.png")))
        register_btn.setIconSize(QSize(22, 22))
        register_btn.clicked.connect(self.open_register)

        buttons_row.addWidget(login_btn)
        buttons_row.addWidget(register_btn)

        author = QLabel("Автор: Щипер Н., группа С422")
        author.setObjectName("muted")
        author.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(soroban)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(6)
        layout.addLayout(buttons_row)
        layout.addSpacing(6)
        layout.addWidget(author)

    # фоновые знаки + × % по углам
    def paintEvent(self, event):
        p = QPainter(self)
        p.fillRect(self.rect(), QColor("#FFFCF7"))          # фон окна
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setPen(QColor("#EFE6D6"))                         # бледный цвет водяных знаков
        p.setFont(QFont("Manrope", 54, QFont.Weight.Bold))

        w = self.width()
        h = self.height()
        p.drawText(45, 100, "+")
        p.drawText(w - 100, 115, "×")
        p.drawText(45, h - 45, "+")
        p.drawText(w - 110, h - 45, "%")
        p.end()

    def open_login(self):
        self.main.go_to(self.main.login)

    def open_register(self):
        self.main.go_to(self.main.register)