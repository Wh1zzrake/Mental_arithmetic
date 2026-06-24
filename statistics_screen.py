from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QTableWidget, QTableWidgetItem, QPushButton, QFrame,
                             QHeaderView, QAbstractItemView)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QIcon

from paths import img_path
import stats                       # чтение статистики из users.json


# делает таблицу «чистой»: без сетки, без нумерации строк, колонки на всю ширину
def clean_table(table):
    table.verticalHeader().setVisible(False)        # убрать номера строк слева
    table.verticalHeader().setDefaultSectionSize(40)  # высота строки (чтобы не было тесно)
    table.setShowGrid(True)                         # видимая сетка — видно разграничение колонок и строк
    table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
    table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
    table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    table.horizontalHeader().setSectionResizeMode(
        QHeaderView.ResizeMode.Stretch)             # колонки тянутся на всю ширину
    # заголовки по левому краю — тогда данные встают точно под ними (без смещения)
    table.horizontalHeader().setDefaultAlignment(
        Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)


# заполняет таблицу строками: rows — список кортежей (значения по колонкам)
def fill_table(table, rows):
    table.setRowCount(len(rows))                    # столько строк, сколько данных
    for r, row in enumerate(rows):
        for c, value in enumerate(row):
            item = QTableWidgetItem(str(value))
            item.setFlags(Qt.ItemFlag.ItemIsEnabled)  # нельзя редактировать/выделять
            table.setItem(r, c, item)


# превращает дату из файла '2026-06-08 14:30' в вид '08.06.2026' (как в макете)
def format_date(date_str):
    date_part = date_str.split(" ")[0]              # часть до пробела: '2026-06-08'
    bits = date_part.split("-")                     # ['2026', '06', '08']
    if len(bits) == 3:
        return f"{bits[2]}.{bits[1]}.{bits[0]}"     # переставляем: день.месяц.год
    return date_str                                 # если формат другой — как есть


# ---------- общая статистика (рейтинг) ----------
class OverallStatsScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window

        layout = QVBoxLayout(self)
        layout.setContentsMargins(26, 26, 26, 26)
        layout.setSpacing(16)

        # ----- заголовок: иконка-кубок (в цвет палитры) + текст -----
        title_row = QHBoxLayout()
        title_row.setSpacing(10)

        trophy = QLabel()
        pix = QPixmap(img_path("trophy.png"))
        pix = pix.scaledToWidth(30, Qt.TransformationMode.SmoothTransformation)
        trophy.setPixmap(pix)

        title = QLabel("Рейтинг пользователей")
        title.setObjectName("h1")

        title_row.addWidget(trophy)
        title_row.addWidget(title)
        title_row.addStretch()

        # 3 колонки, как в мокапе
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Место", "Ученик", "Лучший результат"])
        clean_table(self.table)

        # кнопка «В главное меню» — слева, по содержимому (не на всю ширину)
        back_btn = QPushButton("  В главное меню")
        back_btn.setObjectName("big")
        back_btn.setIcon(QIcon(img_path("icon_back.png")))   # стрелка-картинка вместо символа ←
        back_btn.setIconSize(QSize(22, 22))
        back_btn.clicked.connect(lambda: self.main.go_to(self.main.menu))
        back_row = QHBoxLayout()
        back_row.addWidget(back_btn)
        back_row.addStretch()

        layout.addLayout(title_row)
        layout.addWidget(self.table)
        layout.addLayout(back_row)

    # вызывается при заходе на экран — строит рейтинг из реальных данных
    def refresh(self):
        users = stats.get_all_users()           # все пользователи из users.json

        # логин текущего пользователя — чтобы пометить его строку «(вы)»
        me = self.main.current_user
        my_username = me.get("username", "") if isinstance(me, dict) else ""

        # для каждого пользователя считаем лучший результат теста
        ranking = []                            # список (лучший_балл, всего, имя_для_показа)
        for u in users:
            tests = u.get("tests", [])
            best_score = 0
            best_total = 15
            for t in tests:                     # ищем тест с наибольшим числом верных
                if t["score"] > best_score:
                    best_score = t["score"]
                    best_total = t["total"]

            # в колонке «Ученик» показываем логин пользователя,
            # свою строку дополнительно помечаем «(вы)»
            if u["username"] == my_username:
                name = u["username"] + " (вы)"
            else:
                name = u["username"]

            ranking.append((best_score, best_total, name))

        # сортируем по лучшему баллу по убыванию (первый кортеж сравнивается первым)
        ranking.sort(reverse=True)

        # собираем строки таблицы с номерами мест
        rows = []
        place = 1
        for best_score, best_total, name in ranking:
            if best_score > 0:                  # есть хотя бы один пройденный тест
                result_text = f"{best_score} / {best_total}"
            else:
                result_text = "—"               # тестов ещё не было
            rows.append((str(place), name, result_text))
            place += 1

        fill_table(self.table, rows)


# ---------- личная статистика ----------
class PersonalStatsScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window

        layout = QVBoxLayout(self)
        layout.setContentsMargins(26, 26, 26, 26)
        layout.setSpacing(16)

        # ----- шапка пользователя: имя + группа (заполняется в refresh) -----
        self.user_name = QLabel("")
        self.user_name.setObjectName("h1")
        self.user_group = QLabel("Группа —")
        self.user_group.setObjectName("muted")
        head = QVBoxLayout()
        head.setSpacing(2)
        head.addWidget(self.user_name)
        head.addWidget(self.user_group)

        # ----- карточки-метрики (по центру) -----
        # сохраняем ссылки на значения, чтобы потом обновлять их в refresh()
        metrics_row = QHBoxLayout()
        metrics_row.setSpacing(16)
        avg_card,  self.avg_val  = self._metric("Средний", "—")
        best_card, self.best_val = self._metric("Лучший", "—")
        acc_card,  self.acc_val  = self._metric("Точность тренажёров", "—")
        metrics_row.addWidget(avg_card)
        metrics_row.addWidget(best_card)
        metrics_row.addWidget(acc_card)

        # ----- история тестов -----
        history_label = QLabel("История тестов:")
        history_label.setObjectName("muted")

        self.history = QTableWidget(0, 4)
        self.history.setHorizontalHeaderLabels(["Дата", "Баллы", "Процент", "Оценка"])
        clean_table(self.history)

        back_btn = QPushButton("  В главное меню")
        back_btn.setObjectName("big")
        back_btn.setIcon(QIcon(img_path("icon_back.png")))   # стрелка-картинка вместо символа ←
        back_btn.setIconSize(QSize(22, 22))
        back_btn.clicked.connect(lambda: self.main.go_to(self.main.menu))
        back_row = QHBoxLayout()
        back_row.addWidget(back_btn)
        back_row.addStretch()

        layout.addLayout(head)
        layout.addLayout(metrics_row)
        layout.addWidget(history_label)
        layout.addWidget(self.history)
        layout.addLayout(back_row)

    @staticmethod
    def _metric(caption, value):
        card = QFrame()
        card.setObjectName("metric")
        box = QVBoxLayout(card)
        box.setContentsMargins(16, 14, 16, 14)
        box.setSpacing(4)

        cap = QLabel(caption)
        cap.setObjectName("muted")
        cap.setAlignment(Qt.AlignmentFlag.AlignCenter)   # подпись по центру
        val = QLabel(value)
        val.setObjectName("h1")
        val.setAlignment(Qt.AlignmentFlag.AlignCenter)   # число по центру

        box.addWidget(cap)
        box.addWidget(val)
        return card, val      # возвращаем и карточку, и ярлык значения (чтобы менять текст)

    # вызывается при заходе на экран — заполняет шапку, метрики и историю
    def refresh(self):
        user = self.main.current_user
        username = user.get("username", "") if isinstance(user, dict) else ""

        # берём СВЕЖИЕ данные из файла (в current_user они могут устареть
        # после прохождения теста или тренажёра)
        data = stats.get_stats(username)
        if data is None:
            data = user if isinstance(user, dict) else {}

        # шапка: имя и группа
        name = data.get("name", "")
        group = data.get("group", "")
        self.user_name.setText(f"{name}: {username}" if name else username)
        self.user_group.setText(f"Группа {group}")

        tests = data.get("tests", [])
        trainer = data.get("trainer", {"solved": 0, "correct": 0})

        # средний и лучший балл по тестам
        if tests:
            total_score = 0
            best = 0
            for t in tests:
                total_score += t["score"]
                if t["score"] > best:
                    best = t["score"]
            average = round(total_score / len(tests), 1)   # 1 знак после запятой
            self.avg_val.setText(str(average))
            self.best_val.setText(str(best))
        else:
            self.avg_val.setText("—")
            self.best_val.setText("—")

        # точность тренажёра = верно / решено * 100
        solved = trainer.get("solved", 0)
        correct = trainer.get("correct", 0)
        if solved > 0:
            accuracy = round(correct / solved * 100)
            self.acc_val.setText(f"{accuracy}%")
        else:
            self.acc_val.setText("—")

        # история тестов — новые сверху (поэтому reversed)
        rows = []
        for t in reversed(tests):
            rows.append((
                format_date(t["date"]),
                f'{t["score"]} / {t["total"]}',
                f'{t["percent"]}%',
                str(t["grade"]),
            ))
        fill_table(self.history, rows)
