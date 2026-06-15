# paths.py — пути к файлам проекта (работают и из .py, и из .exe)

import sys
import os

# BASE — это папка, относительно которой ищем все файлы (data/, img/ и т.д.)
if getattr(sys, "frozen", False):      # программа запущена как собранный .exe
    BASE = os.path.dirname(sys.executable)
else:                                  # программа запущена как обычный .py
    BASE = os.path.dirname(os.path.abspath(__file__))


def data_path(name):
    """Возвращает полный путь к файлу внутри папки data/.
       Пример: data_path("lessons.json") -> .../ustny_schet/data/lessons.json"""
    return os.path.join(BASE, "data", name)