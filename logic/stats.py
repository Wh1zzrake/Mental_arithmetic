from datetime import datetime

from logic.auth import load_users, save_users


def _find(users, username):
    """Ищет пользователя по логину в списке. Возвращает его словарь или None."""
    for u in users:
        if u["username"] == username:
            return u
    return None


def record_test(username, score, total, percent, grade_value):
    """Дописывает один пройденный тест в историю пользователя и сохраняет файл.
    score — сколько верных, total — всего вопросов, percent — процент,
    grade_value — оценка по 5-балльной шкале."""
    users = load_users()
    user = _find(users, username)
    if user is None:
        return                          # на всякий случай: пользователя нет
    user["tests"].append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "score": score,
        "total": total,
        "percent": percent,
        "grade": grade_value,
    })
    save_users(users)


def record_trainer(username, solved, correct):
    """Прибавляет итог одной сессии тренажёра к общим счётчикам пользователя
    (сколько решено и сколько верно) и сохраняет файл."""
    users = load_users()
    user = _find(users, username)
    if user is None:
        return
    user["trainer"]["solved"] += solved
    user["trainer"]["correct"] += correct
    save_users(users)


def get_stats(username):
    """Возвращает данные одного пользователя (словарь) или None.
    Читает из файла, поэтому данные всегда свежие."""
    return _find(load_users(), username)


def get_all_users():
    """Возвращает список всех пользователей — нужен экрану общей статистики
    (рейтингу), чтобы построить таблицу лидеров."""
    return load_users()
