import json
from paths import data_path   # путь к файлам в папке data/


def load_lessons():
    """Читаем лекции из data/lessons.json и возвращаем список."""
    with open(data_path("lessons.json"), encoding="utf-8") as f:
        return json.load(f)


def load_questions():
    """Читаем вопросы теста из data/questions.json и возвращаем список."""
    with open(data_path("questions.json"), encoding="utf-8") as f:
        return json.load(f)