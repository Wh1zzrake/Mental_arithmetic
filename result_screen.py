from PyQt6.QtWidgets import (QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from paths import img_path
from background import BackgroundWidget

class ResultScreen(BackgroundWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window

        layout = QVBoxLayout(self)
        layout.setContentsMargins(26, 26, 26, 26)
        layout.setSpacing(16)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # круглая иконка-галочка сверху (стиль #checkCircle из styles.py)
        check = QLabel("✓")
        check.setObjectName("checkCircle")
        check.setFixedSize(64, 64)
        check.setAlignment(Qt.AlignmentFlag.AlignCenter)
        check_row = QHBoxLayout()
        check_row.addStretch()
        check_row.addWidget(check)
        check_row.addStretch()

        # счёт «N из 15» (текст задаётся в TestScreen.finish_test)
        self.score = QLabel("")
        self.score.setObjectName("equation")
        self.score.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.percent = QLabel("")
        self.percent.setObjectName("muted")
        self.percent.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # чип-плашка «Оценка: N» — в ряду с растяжками, чтобы была «таблеткой»
        self.grade = QLabel("")
        self.grade.setObjectName("chip")
        grade_row = QHBoxLayout()
        grade_row.addStretch()
        grade_row.addWidget(self.grade)
        grade_row.addStretch()

        # контурная кнопка «В главное меню» — по центру, по содержимому
        back_btn = QPushButton("  В главное меню")
        back_btn.setObjectName("big")
        back_btn.setIcon(QIcon(img_path("icon_back.png")))   # стрелка-картинка вместо символа ←
        back_btn.setIconSize(QSize(22, 22))
        back_btn.clicked.connect(lambda: self.main.go_to(self.main.menu))
        back_row = QHBoxLayout()
        back_row.addStretch()
        back_row.addWidget(back_btn)
        back_row.addStretch()

        layout.addLayout(check_row)
        layout.addWidget(self.score)
        layout.addWidget(self.percent)
        layout.addSpacing(4)
        layout.addLayout(grade_row)
        layout.addSpacing(8)
        layout.addLayout(back_row)
