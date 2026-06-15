from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QRadioButton, QButtonGroup, QPushButton)
from PyQt6.QtCore import Qt

BEAD_EMPTY = "background:#FFFCF7; border:2px solid #E2C79A; border-radius:8px;"
BEAD_FILLED = "background:#D9822B; border:2px solid #B4691E; border-radius:8px;"


class TestScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window

        layout = QVBoxLayout(self)
        layout.setContentsMargins(26, 26, 26, 26)
        layout.setSpacing(16)

        title = QLabel("Тест")
        title.setObjectName("h1")

        # ----- ряд бусин прогресса (15 штук) -----
        beads_row = QHBoxLayout()
        beads_row.setSpacing(6)
        beads_row.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.beads = []
        for _ in range(15):
            bead = QLabel()
            bead.setFixedSize(16, 16)
            bead.setStyleSheet(BEAD_EMPTY)
            self.beads.append(bead)
            beads_row.addWidget(bead)

        # ----- вопрос-равенство -----
        self.question = QLabel("47 × 11 = ?")
        self.question.setObjectName("equation")

        # ----- варианты ответа (радиокнопки) -----
        self.options_group = QButtonGroup(self)
        self.options = []
        options_box = QVBoxLayout()
        options_box.setSpacing(10)
        for i in range(4):
            rb = QRadioButton("Вариант ответа")
            self.options_group.addButton(rb, i)
            self.options.append(rb)
            options_box.addWidget(rb)

        # ----- кнопки -----
        buttons_row = QHBoxLayout()
        self.next_btn = QPushButton("Далее")
        self.next_btn.setObjectName("accent")

        menu_btn = QPushButton("В главное меню")
        menu_btn.clicked.connect(lambda: self.main.go_to(self.main.menu))

        buttons_row.addWidget(menu_btn)
        buttons_row.addStretch()
        buttons_row.addWidget(self.next_btn)

        layout.addWidget(title)
        layout.addLayout(beads_row)
        layout.addWidget(self.question)
        layout.addLayout(options_box)
        layout.addStretch()
        layout.addLayout(buttons_row)
