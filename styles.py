STYLE = """
/* ===== Базовый фон и текст ===== */
QWidget {
    background: #FFFCF7;
    color: #2A2118;
    font-family: 'Manrope';
    font-size: 14px;
}

/* подписи всегда прозрачные — иначе на тёплых карточках видны белые полосы */
QLabel { background: transparent; }

/* ===== Заголовки ===== */
QLabel#display { font-size: 40px; font-weight: 400; color: #2A2118; }  /* самый крупный, не жирный */
QLabel#h1 { font-size: 24px; font-weight: 800; color: #2A2118; }
QLabel#h2 { font-size: 18px; font-weight: 700; color: #2A2118; }
QLabel#muted { color: #8A7355; font-size: 16px; }
QLabel#theory { color: #6B5A42; font-size: 16px; line-height: 1.6; }

/* ===== Большое равенство в тренажёре ===== */
QLabel#equation { font-size: 40px; font-weight: 800; color: #2A2118; }

/* ===== Контурная кнопка (по умолчанию) ===== */
QPushButton {
    background: #FFFFFF;
    color: #2A2118;
    border: 1px solid #E7DECF;
    border-radius: 10px;
    padding: 11px 15px;
    font-weight: 600;
}
QPushButton:hover  { background: #FBF4E9; }
QPushButton:pressed { background: #F3E9D8; }

/* ===== Поле ввода ===== */
QLineEdit {
    background: #FFFFFF;
    border: 1px solid #E7DECF;
    border-radius: 10px;
    padding: 11px 14px;
    color: #2A2118;
}
QLineEdit:focus { border: 1px solid #D9822B; }

/* ===== Плашка-чип с иконкой ===== */
QFrame#chipFrame {
    background: #FBEFD9;
    border: 1px solid #FBEFD9;   /* граница того же цвета — нужна, иначе скругление не рисуется */
    border-radius: 16px;
}
QLabel#chipText {
    color: #9A5E12;
    font-weight: 700;
    background: transparent;
}

/* ===== Тёплая карточка-метрика (статистика) ===== */
QFrame#metric {
    background: #FBF4E9;
    border-radius: 12px;
}

/* ===== Тёплый блок (картинка-заглушка, пример) ===== */
QLabel#block {
    background: #FBF4E9;
    border-radius: 12px;
    color: #8A7355;
    font-size: 16px;
}

/* ===== Список тем в обучении ===== */
QListWidget {
    background: #FFFFFF;
    border: 1px solid #E7DECF;
    border-radius: 10px;
    padding: 4px;
    outline: none;
    font-size: 18px;
}
QListWidget::item { padding: 9px 11px; border-radius: 8px; color: #6B5A42; }
QListWidget::item:selected { background: #D9822B; color: #FFFFFF; }

/* ===== Варианты ответа (радиокнопки) ===== */
QRadioButton {
    background: #FFFFFF;
    border: 1px solid #E7DECF;
    border-radius: 10px;
    padding: 11px 14px;
    color: #2A2118;
    outline: none;
}
QRadioButton:checked { border: 1px solid #D9822B; background: #FFF6EA; }

/* сам кружок индикатора (без него на Windows кружок пропадает) */
QRadioButton::indicator {
    width: 16px;
    height: 16px;
    border: 2px solid #E2C79A;
    border-radius: 10px;
    background: #FFFFFF;
}
QRadioButton::indicator:checked {
    border: 2px solid #D9822B;
    background: #D9822B;
}

/* ===== Кнопки меню (маркер слева, текст по левому краю) ===== */
QPushButton#menu {
    text-align: left;
    padding: 12px 14px;
    font-size: 24px;
    font-weight: 400;
}
QPushButton#menuAccent {
    text-align: left;
    padding: 12px 14px;
    font-size: 24px;
    font-weight: 400;
    background: #D9822B;
    color: #FFFFFF;
    border: none;
}
QPushButton#menuAccent:hover   { background: #C0731F; }
QPushButton#menuAccent:pressed { background: #A8631A; }

/* ===== Чип-плашка как текст («Урок N», «Оценка: 4») ===== */
QLabel#chip {
    background: #FBEFD9;
    color: #9A5E12;
    border-radius: 12px;
    padding: 6px 13px;
    font-weight: 700;
}

/* ===== Надпись «Верно» (зелёный) ===== */
QLabel#success {font-size: 20px; color: #1C8A52; font-weight: 700; }

/* ===== Таблицы (рейтинг, история тестов) ===== */
QTableWidget {
    background: #FFFFFF;
    border: 1px solid #E7DECF;
    border-radius: 10px;
    color: #2A2118;
    font-size: 16px;                 /* крупнее шрифт данных */
    gridline-color: #F0E8DA;         /* цвет линий сетки (мягкий, в тон палитре) */
}
QTableWidget::item { padding: 8px 12px; border: none; }   /* левый отступ 12 — совпадает с заголовком */
QHeaderView::section {
    background: #FBF4E9;
    color: #8A7355;
    border: none;
    border-bottom: 1px solid #F0E8DA;
    padding: 8px 12px;               /* тот же левый отступ 12, что и у данных */
    font-weight: 700;
    font-size: 16px;                 /* крупнее шрифт заголовков */
}

QTableCornerButton::section { background: #FBF4E9; border: none; }

/* ===== Полосы прокрутки (тонкие, в тон палитре) ===== */
QScrollBar:vertical { background: transparent; width: 8px; margin: 2px; }
QScrollBar::handle:vertical {
    background: #E2C79A; border-radius: 4px; min-height: 24px;
}
QScrollBar::handle:vertical:hover { background: #D9822B; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }

/* акцент-кнопка покрупнее (главное действие экрана) */
QPushButton#accentBig {
    background: #D9822B; color: #FFFFFF; border: none;
    border-radius: 10px; padding: 12px 15px;
    font-size: 24px; font-weight: 400;
}
QPushButton#accentBig:hover   { background: #C0731F; }
QPushButton#accentBig:pressed { background: #A8631A; }

/* контурная кнопка покрупнее (рамку и фон берёт от базовой QPushButton) */
QPushButton#big { font-size: 20px; font-weight: 400; padding: 12px 15px; }

/* поле ввода покрупнее (остальное — от базовой QLineEdit) */
QLineEdit#big { font-size: 18px; }

/* ===== Заголовки экранов и подписи ===== */
QLabel#sectionTitle { font-size: 32px; font-weight: 400; color: #2A2118; }  /* «Выберите тип задания» */
QLabel#greeting     { font-size: 32px; font-weight: 500; color: #2A2118; }  /* «Здравствуйте, …» */
QLabel#lessonTitle  { font-size: 24px; font-weight: 700; color: #2A2118; }  /* название темы в лекции */
QLabel#subtitle     { font-size: 20px; color: #8A7355; }                    /* подпись под заголовком, автор */

/* ===== Чип-плашка покрупнее («Урок N», тип тренажёра) ===== */
QLabel#chipBig {
    background: #FBEFD9; color: #9A5E12;
    border-radius: 18px; padding: 7px 16px;
    font-weight: 700; font-size: 22px;
}

/* ===== Карточка-кнопка в списке тренажёров ===== */
QFrame#taskCard {
    background: #FFFFFF; border: 1px solid #E7DECF; border-radius: 10px;
}
QFrame#taskCard:hover { background: #FBF4E9; }
QLabel#cardText { font-size: 24px; font-weight: 400; color: #2A2118; }  /* подпись на карточке */
QLabel#marker {                                                         /* квадратик-маркер со знаком */
    background: #FBEFD9; color: #C58A2E;
    border-radius: 7px; font-weight: 700; font-size: 14px;
}

/* ===== Круглая иконка-галочка на экране результата ===== */
QLabel#checkCircle {
    background: #FBEFD9; color: #D9822B;
    border-radius: 32px; font-size: 30px; font-weight: 800;
}

/* ===== Полупрозрачное окно выхода (затемнение + карточка) ===== */
QWidget#overlay { background: rgba(42, 33, 24, 0.45); }
QFrame#dialogCard {
    background: #FFFCF7;
    border: 1px solid #ECE3D5;
    border-radius: 14px;
}

"""


def apply(app):
    app.setStyleSheet(STYLE)
