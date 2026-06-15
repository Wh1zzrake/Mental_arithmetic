from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt


class ResultScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window

        layout = QVBoxLayout(self)
        layout.setContentsMargins(26, 26, 26, 26)
        layout.setSpacing(16)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Результат теста")
        title.setObjectName("h1")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.score = QLabel("12 из 15")
        self.score.setObjectName("equation")
        self.score.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.percent = QLabel("80% правильных ответов")
        self.percent.setObjectName("muted")
        self.percent.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.grade = QLabel("Оценка 4")
        self.grade.setObjectName("chip")
        self.grade.setAlignment(Qt.AlignmentFlag.AlignCenter)

        back_btn = QPushButton("В главное меню")
        back_btn.setObjectName("accent")
        back_btn.clicked.connect(lambda: self.main.go_to(self.main.menu))

        layout.addWidget(title)
        layout.addWidget(self.score)
        layout.addWidget(self.percent)
        layout.addWidget(self.grade)
        layout.addWidget(back_btn)
