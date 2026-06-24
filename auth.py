# auth.py — регистрация и вход.
# Пользователи хранятся в data/users.json, пароль — не в открытом виде,
# а в виде хеша (SHA-256, модуль hashlib).

import json
import hashlib

from paths import data_path


def _users_file():
    return data_path("users.json")


def load_users():
    """Читает список пользователей из users.json.
    Если файла нет или он пустой/битый — возвращает пустой список."""
    try:
        with open(_users_file(), encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_users(users):
    """Записывает список пользователей обратно в users.json."""
    with open(_users_file(), "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


def hash_password(password):
    """Превращает пароль в SHA-256-хеш (строка из 64 символов)."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def register(username, password, name, group):
    """Создаёт нового пользователя. Возвращает его данные (dict)
    при успехе или None, если такой логин уже занят."""
    users = load_users()
    for u in users:
        if u["username"] == username:
            return None                 # логин уже занят

    new_user = {
        "username": username,
        "password": hash_password(password),
        "name": name,
        "group": group,
        "tests": [],
        "trainer": {"solved": 0, "correct": 0},
    }
    users.append(new_user)
    save_users(users)
    return new_user


def check_login(username, password):
    """Проверяет логин и пароль. Возвращает данные пользователя (dict)
    при совпадении или None, если не подошло."""
    h = hash_password(password)
    for u in load_users():
        if u["username"] == username and u["password"] == h:
            return u
    return None
