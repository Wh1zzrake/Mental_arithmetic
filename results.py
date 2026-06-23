# results.py — подсчёт оценки по 5-балльной шкале.

def grade(score, total):
    """По числу правильных (score) и общему числу вопросов (total)
    возвращает оценку от 2 до 5."""
    percent = score / total * 100
    if percent >= 90:
        return 5
    if percent >= 75:
        return 4
    if percent >= 50:
        return 3
    return 2
