import json

from paths import data_path   # путь к файлам в папке data/


def load_lessons():
    """Читаем лекции из data/lessons.json и возвращаем список.
    Если файла нет или он повреждён — возвращаем пустой список,
    чтобы программа не упала (экран обучения покажет сообщение)."""
    try:
        with open(data_path("lessons.json"), encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def load_questions():
    """Читаем вопросы теста из data/questions.json и возвращаем список.
    Если файла нет или он повреждён — возвращаем пустой список,
    чтобы программа не упала (экран теста покажет сообщение)."""
    try:
        with open(data_path("questions.json"), encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
