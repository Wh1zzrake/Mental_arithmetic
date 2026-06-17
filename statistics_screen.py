from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QTableWidget, QTableWidgetItem, QPushButton, QFrame,
                             QHeaderView, QAbstractItemView)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QIcon
from paths import img_path


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

    # вызывается при заходе на экран — заполняет рейтинг
    def refresh(self):
        # --- ЗАГЛУШКА: пока нет реальных пользователей, показываем примерный рейтинг ---
        rows = [
            ("1", "Вы", "15 / 15"),
            ("2", "Пользователь 1", "14 / 15"),
            ("3", "Пользователь 2", "13 / 15"),
        ]
        fill_table(self.table, rows)


# ---------- личная статистика ----------
class PersonalStatsScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window

        layout = QVBoxLayout(self)
        layout.setContentsMargins(26, 26, 26, 26)
        layout.setSpacing(16)

        # ----- шапка пользователя: имя + группа -----
        self.user_name = QLabel("Имя: логин")
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

    def _metric(self, caption, value):
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
        # имя и группа берём из вошедшего пользователя; если входа ещё нет — заглушка
        user = self.main.current_user
        if isinstance(user, dict):
            name = user.get("name", "")
            username = user.get("username", "")
            group = user.get("group", "")
            self.user_name.setText(f"{name}: {username}" if name else username)
            self.user_group.setText(f"Группа {group}")
        else:
            self.user_name.setText("Николай: kolya733")
            self.user_group.setText("Группа С422")

        # --- ЗАГЛУШКА: примерные метрики и история (пока нет реальной статистики) ---
        self.avg_val.setText("11.3")
        self.best_val.setText("15")
        self.acc_val.setText("88%")

        rows = [
            ("08.06.2026", "12 / 15", "80%", "4"),
            ("07.06.2026", "10 / 15", "67%", "3"),
            ("06.06.2026", "15 / 15", "100%", "5"),
        ]
        fill_table(self.history, rows)