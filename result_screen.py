from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton)
from PyQt6.QtCore import Qt
from background import BackgroundWidget

class ResultScreen(BackgroundWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window

        layout = QVBoxLayout(self)
        layout.setContentsMargins(26, 26, 26, 26)
        layout.setSpacing(16)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # круглая иконка-галочка сверху (как в мокапе)
        check = QLabel("✓")
        check.setFixedSize(64, 64)
        check.setAlignment(Qt.AlignmentFlag.AlignCenter)
        check.setStyleSheet(
            "background:#FBEFD9; border-radius:32px;"
            "color:#D9822B; font-size:30px; font-weight:800;"
        )
        check_row = QHBoxLayout()
        check_row.addStretch()
        check_row.addWidget(check)
        check_row.addStretch()

        # «12 из 15» — слово «из» приглушённого цвета
        self.score = QLabel('12 <span style="color:#8A7355;">из</span> 15')
        self.score.setObjectName("equation")
        self.score.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.percent = QLabel("Правильных ответов 80%")
        self.percent.setObjectName("muted")
        self.percent.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # чип-плашка «Оценка: 4» — в ряду со «растяжками», чтобы была «таблеткой»
        self.grade = QLabel("Оценка: 4")
        self.grade.setObjectName("chip")
        grade_row = QHBoxLayout()
        grade_row.addStretch()
        grade_row.addWidget(self.grade)
        grade_row.addStretch()

        # контурная кнопка «В главное меню» — по центру, по содержимому
        back_btn = QPushButton("←  В главное меню")
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