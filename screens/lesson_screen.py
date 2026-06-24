import os

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QListWidget, QPushButton, QScrollArea, QFrame)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QIcon

from logic.data_loader import load_lessons   # читает data/lessons.json
from core.paths import BASE, img_path                 # базовая папка проекта (для картинок)


class LessonScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window
        self.lessons = []              # сюда загрузим список лекций

        layout = QVBoxLayout(self)
        layout.setContentsMargins(26, 26, 26, 26)
        layout.setSpacing(16)

        # ----- две колонки -----
        columns = QHBoxLayout()
        columns.setSpacing(16)

        # слева — список тем
        self.topics = QListWidget()
        self.topics.setFixedWidth(260)
        self.topics.setWordWrap(True)  # длинные названия переносятся на 2 строки
        self.topics.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # как только выбрали другую строку — обновим правую часть
        self.topics.currentRowChanged.connect(self.show_lesson)

        # справа — содержимое выбранной темы
        right = QVBoxLayout()
        right.setSpacing(11)

        self.topic_lesson_no = QLabel("")
        self.topic_lesson_no.setObjectName("chipBig")

        self.topic_title = QLabel("")
        self.topic_title.setObjectName("lessonTitle")

        self.topic_theory = QLabel("")
        self.topic_theory.setObjectName("theory")
        self.topic_theory.setWordWrap(True)

        self.topic_example = QLabel("")
        self.topic_example.setObjectName("block")
        self.topic_example.setWordWrap(True)

        self.topic_image = QLabel("")
        self.topic_image.setObjectName("block")
        self.topic_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.topic_image.setMinimumHeight(160)

        # строка с плашкой «Урок N» — прижата влево, чтобы была компактной
        chip_row = QHBoxLayout()
        chip_row.addWidget(self.topic_lesson_no)
        chip_row.addStretch()
        right.addLayout(chip_row)

        right.addWidget(self.topic_title)
        right.addWidget(self.topic_theory)
        right.addWidget(self.topic_example)
        right.addWidget(self.topic_image)
        right.addStretch()

        # правую часть кладём в прокрутку (лекции длинные)
        right_box = QWidget()
        right_box.setLayout(right)
        scroll = QScrollArea()
        scroll.setWidget(right_box)
        scroll.setWidgetResizable(True)             # содержимое тянется по ширине
        scroll.setFrameShape(QFrame.Shape.NoFrame)  # убрать рамку прокрутки

        columns.addWidget(self.topics)
        columns.addWidget(scroll)

        back_btn = QPushButton("  В главное меню")
        back_btn.setObjectName("big")
        back_btn.setIcon(QIcon(img_path("icon_back.png")))   # стрелка-картинка вместо символа ←
        back_btn.setIconSize(QSize(20, 20))
        back_btn.clicked.connect(lambda: self.main.go_to(self.main.menu))

        # кладём кнопку в строку и прижимаем влево (не на всю ширину)
        back_row = QHBoxLayout()
        back_row.addWidget(back_btn)
        back_row.addStretch()

        layout.addLayout(columns)
        layout.addLayout(back_row)

        # загружаем лекции при создании экрана
        self.load_topics()

    def load_topics(self):
        """Читаем лекции и заполняем список тем слева."""
        self.lessons = load_lessons()
        self.topics.clear()
        for lesson in self.lessons:
            self.topics.addItem(lesson["title"])
        # сразу выбираем первую тему, чтобы экран не был пустым
        if self.lessons:
            self.topics.setCurrentRow(0)
        else:
            # уроки не загрузились (файла нет или он повреждён) —
            # показываем понятное сообщение вместо пустого экрана
            self.topic_lesson_no.setText("—")
            self.topic_title.setText("Уроки не загружены")
            self.topic_theory.setText("Проверьте файл data/lessons.json.")
            self.topic_example.setText("")
            self.topic_image.setPixmap(QPixmap())
            self.topic_image.setText("[ нет данных ]")

    def show_lesson(self, index):
        """Показываем выбранную тему. index — номер строки в списке слева."""
        if index < 0:
            return                                  # ничего не выбрано
        lesson = self.lessons[index]

        self.topic_lesson_no.setText("Урок " + str(lesson["id"]))
        self.topic_title.setText(lesson["title"])
        self.topic_theory.setText(lesson["theory"])
        self.topic_example.setText(lesson["example"])

        # картинка: строим полный путь и пробуем загрузить
        image_path = os.path.join(BASE, lesson["image"])
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            # файла нет — показываем заглушку
            self.topic_image.setPixmap(QPixmap())   # очистить старую картинку
            self.topic_image.setText("[ нет картинки ]")
        else:
            # если картинка широкая — уменьшим по ширине, пропорции сохранятся
            if pixmap.width() > 500:
                pixmap = pixmap.scaledToWidth(
                    500, Qt.TransformationMode.SmoothTransformation)
            self.topic_image.setText("")
            self.topic_image.setPixmap(pixmap)
