from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QRadioButton, QButtonGroup, QPushButton, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from paths import img_path

BEAD_EMPTY  = "background:#FFFCF7; border:2px solid #E2C79A; border-radius:8px;"
BEAD_FILLED = "background:#D9822B; border:2px solid #B4691E; border-radius:8px;"


class TestScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window

        layout = QVBoxLayout(self)
        layout.setContentsMargins(26, 26, 26, 26)
        layout.setSpacing(16)

        # ----- верхняя строка: плашка «Вопрос N из 15» + группа -----
        top_row = QHBoxLayout()

        # плашка-чип: иконка-соробан + текст в одной «таблетке»
        chip = QFrame()
        chip.setObjectName("chipFrame")
        chip_row = QHBoxLayout(chip)
        chip_row.setContentsMargins(13, 6, 14, 6)
        chip_row.setSpacing(8)

        chip_icon = QLabel()
        pix = QPixmap(img_path("logo_inv.png"))
        pix = pix.scaledToWidth(32, Qt.TransformationMode.SmoothTransformation)
        chip_icon.setPixmap(pix)

        self.progress_chip = QLabel("Вопрос 1 из 15")
        self.progress_chip.setObjectName("chipText")

        chip_row.addWidget(chip_icon)
        chip_row.addWidget(self.progress_chip)

        self.group_label = QLabel("Группа —")
        self.group_label.setObjectName("muted")

        top_row.addWidget(chip)
        top_row.addStretch()
        top_row.addWidget(self.group_label)

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

        # ----- вопрос-равенство ----- («?» — оранжевый, как в мокапе)
        self.question = QLabel('47 × 11 = <span style="color:#D9822B;">?</span>')
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

        self.next_btn = QPushButton("→  Далее")
        self.next_btn.setObjectName("accent")
        self.next_btn.setMinimumWidth(300)
        # пока что «Далее» сразу открывает экран результата
        self.next_btn.clicked.connect(lambda: self.main.go_to(self.main.result))

        menu_btn = QPushButton("×  В меню")
        menu_btn.setMinimumWidth(150)
        menu_btn.clicked.connect(lambda: self.main.go_to(self.main.menu))

        buttons_row.addWidget(self.next_btn, 2)
        buttons_row.addWidget(menu_btn, 1)

        layout.addLayout(top_row)
        layout.addLayout(beads_row)
        layout.addWidget(self.question)
        layout.addSpacing(6)
        layout.addLayout(options_box)
        layout.addStretch()
        layout.addLayout(buttons_row)