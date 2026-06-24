import random

from PyQt6.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel,
                             QRadioButton, QButtonGroup, QPushButton,
                             QFrame, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from core.paths import img_path
from core.background import BackgroundWidget
from logic import stats, results
from logic.data_loader import load_questions


BEAD_EMPTY  = "background:#FFFCF7; border:2px solid #E2C79A; border-radius:8px;"
BEAD_FILLED = "background:#D9822B; border:2px solid #B4691E; border-radius:8px;"


class TestScreen(BackgroundWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window

        # --- состояние теста ---
        self.questions = []    # 15 случайных вопросов текущего прогона
        self.index = 0         # номер текущего вопроса (0..14)
        self.correct = 0       # сколько верных ответов набрано

        layout = QVBoxLayout(self)
        layout.setContentsMargins(26, 26, 26, 26)
        layout.setSpacing(16)

        # ----- верхняя строка: плашка «Вопрос N из 15» + группа -----
        top_row = QHBoxLayout()

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

        # ----- вопрос-равенство ----- (текст задаётся в show_question)
        self.question = QLabel("")
        self.question.setObjectName("equation")
        self.question.setWordWrap(True)   # длинный текстовый вопрос переносится

        # ----- варианты ответа (радиокнопки) -----
        self.options_group = QButtonGroup(self)
        self.options = []
        options_box = QVBoxLayout()
        options_box.setSpacing(10)
        # создаём 4 пустые радиокнопки (4 — максимум вариантов);
        # тексты вариантов подставляются в show_question()
        for i in range(4):
            rb = QRadioButton("")
            self.options_group.addButton(rb, i)
            self.options.append(rb)
            options_box.addWidget(rb)

        # ----- кнопки -----
        buttons_row = QHBoxLayout()

        self.next_btn = QPushButton("→  Далее")
        self.next_btn.setObjectName("accentBig")
        self.next_btn.setMinimumWidth(300)
        self.next_btn.clicked.connect(self.next_question)

        menu_btn = QPushButton("×  В меню")
        menu_btn.setObjectName("big")
        menu_btn.setMinimumWidth(150)
        menu_btn.clicked.connect(self.interrupt)

        buttons_row.addWidget(self.next_btn, 2)
        buttons_row.addWidget(menu_btn, 1)

        layout.addLayout(top_row)
        layout.addLayout(beads_row)
        layout.addWidget(self.question)
        layout.addSpacing(6)
        layout.addLayout(options_box)
        layout.addSpacing(22)
        layout.addLayout(buttons_row)
        layout.addStretch()

    def refresh(self):
        """Вызывается автоматически при открытии экрана (через go_to):
        начинает новый тест — 15 случайных вопросов без повторов."""
        all_questions = load_questions()

        # защита: если вопросов не удалось загрузить (файла нет / повреждён)
        # или их меньше 15 — тест не начинаем, показываем сообщение.
        # Кнопка «В меню» вернёт на главный экран.
        if len(all_questions) < 15:
            self.questions = []
            self.question.setText("Не удалось загрузить вопросы теста.")
            QMessageBox.warning(self, "Тест",
                                "Не удалось загрузить вопросы теста.\n"
                                "Проверьте файл data/questions.json.")
            return

        self.questions = random.sample(all_questions, 15)
        self.index = 0
        self.correct = 0

        # группа из учётной записи (если пользователь вошёл)
        user = self.main.current_user
        if user:
            self.group_label.setText("Группа " + user.get("group", "—"))
        else:
            self.group_label.setText("Группа —")

        self.show_question()

    def show_question(self):
        """Показывает текущий вопрос: текст, варианты, прогресс, кнопку."""
        if not self.questions:
            return                         # вопросы не загрузились — показывать нечего
        q = self.questions[self.index]

        # плашка прогресса
        self.progress_chip.setText(f"Вопрос {self.index + 1} из 15")

        # бусины: первые (index+1) закрашены, остальные пустые
        for i, bead in enumerate(self.beads):
            bead.setStyleSheet(BEAD_FILLED if i <= self.index else BEAD_EMPTY)

        # текст вопроса; «?» красим оранжевым, как в макете
        html = q["q"].replace("?", '<span style="color:#D9822B;">?</span>')
        self.question.setText(html)

        # подставляем варианты; лишние радиокнопки прячем
        # (есть вопросы «да/нет» всего с 2 вариантами)
        count = len(q["options"])
        for i, rb in enumerate(self.options):
            if i < count:
                rb.setText(q["options"][i])
                rb.setVisible(True)
            else:
                rb.setVisible(False)

        # снимаем прошлый выбор (группа эксклюзивная — временно отключаем)
        self.options_group.setExclusive(False)
        for rb in self.options:
            rb.setChecked(False)
        self.options_group.setExclusive(True)

        # на последнем вопросе меняем надпись кнопки
        if self.index == 14:
            self.next_btn.setText("✓  Завершить тест")
        else:
            self.next_btn.setText("→  Далее")

    def next_question(self):
        """Кнопка «Далее» / «Завершить тест»: проверяем выбор и идём дальше."""
        if not self.questions:
            return                         # тест не идёт (вопросы не загрузились)
        chosen = self.options_group.checkedId()   # -1, если ничего не выбрано
        if chosen == -1:
            QMessageBox.information(self, "Тест", "Выберите вариант ответа.")
            return

        # сравниваем индекс выбранного варианта с правильным
        if chosen == self.questions[self.index]["answer"]:
            self.correct += 1

        if self.index < 14:
            self.index += 1
            self.show_question()
        else:
            self.finish_test()

    def finish_test(self):
        """Считает итог, заполняет экран результата и показывает его."""
        total = 15
        percent = round(self.correct / total * 100)
        grade_value = results.grade(self.correct, total)

        # заполняем подписи на экране результата перед показом
        self.main.result.score.setText(
            f'{self.correct} <span style="color:#8A7355;">из</span> {total}')
        self.main.result.percent.setText(f"Правильных ответов {percent}%")
        self.main.result.grade.setText(f"Оценка: {grade_value}")

        # сохраняем результат в статистику текущего пользователя
        user = self.main.current_user
        if isinstance(user, dict):
            stats.record_test(user["username"], self.correct, total,
                              percent, grade_value)

        self.main.go_to(self.main.result)

    def interrupt(self):
        """Кнопка «В меню»: прерываем тест с подтверждением; результат не сохраняем."""
        # если тест не идёт (вопросы не загрузились) — выходим без подтверждения
        if not self.questions:
            self.main.go_to(self.main.menu)
            return
        ans = QMessageBox.question(
            self, "Прервать тест?",
            "Если выйти сейчас, результат не сохранится. Прервать тест?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if ans == QMessageBox.StandardButton.Yes:
            self.main.go_to(self.main.menu)
