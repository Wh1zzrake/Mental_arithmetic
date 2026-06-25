from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QLabel, QLineEdit, QPushButton)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap, QIntValidator

from core.paths import img_path
from core.background import BackgroundWidget
from logic import stats, generators


# --- список тренажёров ---
class TrainerListScreen(BackgroundWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window

        layout = QVBoxLayout(self)
        layout.setContentsMargins(26, 26, 26, 26)
        layout.setSpacing(16)

        title = QLabel("Выберите тип задания")
        title.setObjectName("sectionTitle")

        grid = QGridLayout()
        grid.setSpacing(11)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)

        # шесть кнопок типов заданий — каждая создаётся явно (как в меню),
        # у каждой свой clicked.connect со своим ключом тренажёра
        mult11_btn = self._task_btn("Умножение на 11", "op_times.png")        # кнопка Умножение на 11
        mult11_btn.clicked.connect(lambda: self._open("mult11"))             #  тренажёр n × 11

        square5_btn = self._task_btn("Квадраты чисел на 5", "op_times.png")   # кнопка Квадраты чисел на 5
        square5_btn.clicked.connect(lambda: self._open("square5"))          #  тренажёр n5²

        percent_btn = self._task_btn("Проценты", "op_percent.png")           # кнопка Проценты
        percent_btn.clicked.connect(lambda: self._open("percent"))          #  тренажёр p % от n

        divis_btn = self._task_btn("Признаки делимости", "op_div.png")        # кнопка Признаки делимости
        divis_btn.clicked.connect(lambda: self._open("divisibility"))       #  тренажёр делится ли n на d

        addsub_btn = self._task_btn("Сложение / вычитание", "op_plus.png")    # кнопка Сложение / вычитание
        addsub_btn.clicked.connect(lambda: self._open("add_sub"))           #  тренажёр сложение/вычитание

        mult59_btn = self._task_btn("Умножение на 5 / 9 / 25", "op_times.png")  # кнопка Умножение на 5 / 9 / 25
        mult59_btn.clicked.connect(lambda: self._open("mult_5_9_25"))        #  тренажёр n × {5,9,25}

        # раскладка 2 колонки по 3 ряда
        grid.addWidget(mult11_btn,  0, 0)
        grid.addWidget(square5_btn, 0, 1)
        grid.addWidget(percent_btn, 1, 0)
        grid.addWidget(divis_btn,   1, 1)
        grid.addWidget(addsub_btn,  2, 0)
        grid.addWidget(mult59_btn,  2, 1)

        mix_btn = QPushButton("  Вперемешку")   # кнопка Вперемешку
        mix_btn.setObjectName("accentBig")
        mix_btn.setIcon(QIcon(img_path("icon_shuffle.png")))
        mix_btn.setIconSize(QSize(24, 24))
        mix_btn.clicked.connect(lambda: self._open("mix"))   #  запустить смешанный режим

        back_btn = QPushButton("  В главное меню")   # кнопка В главное меню
        back_btn.setObjectName("big")
        back_btn.setIcon(QIcon(img_path("icon_back.png")))
        back_btn.setIconSize(QSize(24, 24))
        back_btn.clicked.connect(lambda: self.main.go_to(self.main.menu))   #  вернуться в меню

        layout.addStretch()
        layout.addWidget(title)
        layout.addLayout(grid)
        layout.addWidget(mix_btn)
        layout.addWidget(back_btn)
        layout.addStretch()

    def _task_btn(self, text, icon_name):
        btn = QPushButton("  " + text)
        btn.setObjectName("menu")
        btn.setIcon(QIcon(img_path(icon_name)))
        btn.setIconSize(QSize(32, 32))
        return btn

    def _open(self, kind):
        # обработчик клика по карточке/кнопке Вперемешку:
        # задаём тип задания в рабочем окне и открываем его
        self.main.trainer_work.set_kind(kind)
        self.main.go_to(self.main.trainer_work)


# --- рабочее окно тренажёра ---
class TrainerWorkScreen(BackgroundWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window

        # --- состояние сессии ---
        self.current_kind = "mix"      # какой тип сейчас решаем
        self.current_answer = None     # правильный ответ текущего задания
        self.solved = 0                # сколько всего решено
        self.correct = 0               # сколько из них верно

        layout = QVBoxLayout(self)
        layout.setContentsMargins(26, 26, 26, 26)
        layout.setSpacing(16)

        top_row = QHBoxLayout()

        self.type_title = QLabel("Тип задания")
        self.type_title.setObjectName("chipBig")

        self.counter = QLabel("Решено 0 · Верно 0")
        self.counter.setObjectName("muted")

        top_row.addWidget(self.type_title)
        top_row.addStretch()
        top_row.addWidget(self.counter)

        self.task = QLabel("") # текст задания задаётся в next_task
        self.task.setObjectName("equation")
        self.task.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.answer_input = QLineEdit()
        self.answer_input.setPlaceholderText("ответ")
        self.answer_input.setFixedWidth(360)
        self.answer_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # в поле ответа можно вводить только цифры (целое число от 0)
        self.answer_input.setValidator(QIntValidator(0, 1000000000, self))
        self.answer_input.returnPressed.connect(self.check_answer)   # Enter в поле check_answer()

        # кнопки Да / Нет — показываются вместо поля в заданиях на
        # признаки делимости (там ответ не число, а да/нет)
        self.yes_btn = QPushButton("Да")              # кнопка Да (только в делимости)
        self.yes_btn.setObjectName("big")
        self.yes_btn.setFixedWidth(120)
        self.yes_btn.clicked.connect(lambda: self.submit_answer("да"))
        self.no_btn = QPushButton("Нет")              # кнопка Нет (только в делимости)
        self.no_btn.setObjectName("big")
        self.no_btn.setFixedWidth(120)
        self.no_btn.clicked.connect(lambda: self.submit_answer("нет"))
        self.yesno_widget = QWidget()
        yesno_box = QHBoxLayout(self.yesno_widget)
        yesno_box.setContentsMargins(0, 0, 0, 0)
        yesno_box.setSpacing(12)
        yesno_box.addWidget(self.yes_btn)
        yesno_box.addWidget(self.no_btn)

        input_row = QHBoxLayout()
        input_row.addStretch()
        input_row.addWidget(self.answer_input)
        input_row.addWidget(self.yesno_widget)
        input_row.addStretch()

        self.feedback_icon = QLabel()
        pix = QPixmap(img_path("icon_correct.png"))
        pix = pix.scaledToWidth(20, Qt.TransformationMode.SmoothTransformation)
        self.feedback_icon.setPixmap(pix)

        self.feedback = QLabel(" ")       # подпись Верно/Неверно появляется после ответа
        self.feedback.setObjectName("success")

        feedback_row = QHBoxLayout()
        feedback_row.setSpacing(6)
        feedback_row.addStretch()
        feedback_row.addWidget(self.feedback_icon)
        feedback_row.addWidget(self.feedback)
        feedback_row.addStretch()

        self.answer_btn = QPushButton("  Ответ")   # кнопка Ответ
        self.answer_btn.setObjectName("accentBig")
        self.answer_btn.setIcon(QIcon(img_path("icon_check.png")))
        self.answer_btn.setIconSize(QSize(22, 22))
        self.answer_btn.clicked.connect(self.check_answer)           #  обработчик check_answer()

        list_btn = QPushButton("  К списку")        # кнопка К списку
        list_btn.setObjectName("big")
        list_btn.setIcon(QIcon(img_path("icon_list.png")))
        list_btn.setIconSize(QSize(22, 22))
        list_btn.clicked.connect(self.go_to_list)               #  сохранить сессию и к списку

        menu_btn = QPushButton("  Меню")            # кнопка Меню
        menu_btn.setObjectName("big")
        menu_btn.setIcon(QIcon(img_path("icon_home.png")))
        menu_btn.setIconSize(QSize(22, 22))
        menu_btn.clicked.connect(self.go_to_menu)               #  сохранить сессию и в меню

        secondary_row = QHBoxLayout()
        secondary_row.setSpacing(11)
        secondary_row.addWidget(list_btn)
        secondary_row.addWidget(menu_btn)

        btn_col = QVBoxLayout()
        btn_col.setSpacing(11)
        btn_col.addWidget(self.answer_btn)
        btn_col.addLayout(secondary_row)

        btn_box = QWidget()
        btn_box.setFixedWidth(440)
        btn_box.setLayout(btn_col)
        btn_wrap = QHBoxLayout()
        btn_wrap.addStretch()
        btn_wrap.addWidget(btn_box)
        btn_wrap.addStretch()

        layout.addLayout(top_row)
        layout.addStretch()
        layout.addWidget(self.task)
        layout.addLayout(input_row)
        layout.addLayout(feedback_row)
        layout.addSpacing(22)
        layout.addLayout(btn_wrap)
        layout.addStretch()

    def set_kind(self, kind):
        """Вызывается из списка при выборе типа: ставит название,
        обнуляет счётчики сессии и сразу даёт первое задание."""
        labels = {
            "mult11": "Умножение на 11",
            "square5": "Квадраты чисел на 5",
            "percent": "Проценты",
            "divisibility": "Признаки делимости",
            "add_sub": "Сложение / вычитание",
            "mult_5_9_25": "Умножение на 5 / 9 / 25",
            "mix": "Вперемешку",
        }
        self.type_title.setText(labels.get(kind, kind))

        # запоминаем тип и обнуляем сессию
        self.current_kind = kind
        self.solved = 0
        self.correct = 0
        self.counter.setText("Решено 0 · Верно 0")

        # прячем подпись до первого ответа (пробел держит высоту строки)
        self.feedback.setText(" ")
        self.feedback_icon.setVisible(False)

        # первое задание
        self.next_task()

    def next_task(self):
        """Берёт у генератора новое задание и показывает его."""
        text, answer = generators.random_task(self.current_kind)
        self.current_answer = answer
        # красим ? в оранжевый, как в макете (QLabel понимает HTML)
        html = text.replace("?", '<span style="color:#D9822B;">?</span>')
        self.task.setText(html)

        # Ответ да/нет (признаки делимости) приходит строкой, а число — int.
        # По типу ответа и выбираем способ: поле для числа или кнопки Да/Нет.
        is_yes_no = isinstance(answer, str)
        self.answer_input.setVisible(not is_yes_no)
        self.answer_btn.setVisible(not is_yes_no)
        self.yesno_widget.setVisible(is_yes_no)

        if not is_yes_no:
            self.answer_input.clear()
            self.answer_input.setFocus()   # курсор сразу в поле ввода

    def check_answer(self):
        """кнопка Ответ / Enter в поле: берём число из поля и проверяем."""
        user = self.answer_input.text().strip()
        if user == "":
            return                     # пустой ответ не засчитываем
        self.submit_answer(user)

    def submit_answer(self, user_answer):
        """Общая проверка ответа — и для числа из поля, и для кнопок Да/Нет.
        Обновляет счётчик и сразу даёт следующее задание."""
        # сравниваем как текст в нижнем регистре —
        # работает и для чисел, и для ответа да/нет в делимости
        right = str(self.current_answer).strip().lower()
        self.solved += 1
        if str(user_answer).strip().lower() == right:
            self.correct += 1
            self.feedback.setText("Верно")
            self.feedback.setStyleSheet("color:#1C8A52; font-weight:600;")
            self.feedback_icon.setVisible(True)
        else:
            self.feedback.setText("Неверно")
            self.feedback.setStyleSheet("color:#C0392B; font-weight:600;")
            self.feedback_icon.setVisible(False)

        self.counter.setText(f"Решено {self.solved} · Верно {self.correct}")
        self.next_task()               # сразу следующее задание

    def save_session(self):
        """Сохраняет итог сессии (решено / верно) в статистику пользователя.
        После сохранения обнуляет счётчики, чтобы при повторном входе
        те же ответы не записались второй раз."""
        user = self.main.current_user
        if isinstance(user, dict) and self.solved > 0:
            stats.record_trainer(user["username"], self.solved, self.correct)
        self.solved = 0
        self.correct = 0

    def go_to_list(self):
        """кнопка К списку: сохранить сессию и вернуться к выбору типа."""
        self.save_session()
        self.main.go_to(self.main.trainer_list)

    def go_to_menu(self):
        """кнопка Меню: сохранить сессию и выйти в главное меню."""
        self.save_session()
        self.main.go_to(self.main.menu)