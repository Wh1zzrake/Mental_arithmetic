import sys
import os


if getattr(sys, "frozen", False):      # запущено как .exe
    BASE = os.path.dirname(sys.executable)
else:                                  # запущено как .py
    BASE = os.path.dirname(os.path.abspath(__file__))


def data_path(name):
    return os.path.join(BASE, "data", name)


def img_path(name):
    return os.path.join(BASE, "img", name)
