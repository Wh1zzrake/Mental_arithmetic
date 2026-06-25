import os


BASE = os.path.dirname(os.path.abspath(__file__))


def data_path(name):
    return os.path.join(BASE, "../data", name)


def img_path(name):
    return os.path.join(BASE, "../img", name)
