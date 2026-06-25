import random


def gen_mult_by_11():
    """Умножение двузначного числа на 11."""
    n = random.randint(10, 99)
    text = f"{n} × 11 = ?"
    answer = n * 11
    return text, answer


def gen_square5():
    """Квадрат числа, оканчивающегося на 5 (15, 25, ... 95)."""
    k = random.randint(1, 9)
    n = k * 10 + 5                    # 15, 25, 35, ... 95
    text = f"{n}² = ?"
    answer = n * n
    return text, answer


def gen_percent():
    """Сколько процентов от числа. Число кратно 20 — ответ всегда целый."""
    p = random.choice([5, 10, 15, 20, 25, 50])
    n = random.randint(1, 10) * 20    # 20, 40, 60, ... 200
    text = f"{p}% от {n} = ?"
    answer = n * p // 100
    return text, answer


def gen_divisible():
    """Делится ли число на делитель. Ответ — слово «да» или «нет»."""
    n = random.randint(100, 999)
    d = random.choice([2, 3, 4, 5, 6, 9, 11])
    text = f"{n} делится на {d}? (да / нет)"
    if n % d == 0:
        answer = "да"
    else:
        answer = "нет"
    return text, answer


def gen_add_sub():
    """Сложение или вычитание двух двузначных чисел."""
    a = random.randint(10, 99)
    b = random.randint(10, 99)
    if random.choice([True, False]):
        text = f"{a} + {b} = ?"
        answer = a + b
    else:
        if a < b:                     # чтобы ответ не получился отрицательным
            a, b = b, a
        text = f"{a} − {b} = ?"
        answer = a - b
    return text, answer


def gen_mult_5_9_25():
    """Умножение двузначного числа на 5, 9 или 25."""
    n = random.randint(10, 99)
    m = random.choice([5, 9, 25])
    text = f"{n} × {m} = ?"
    answer = n * m
    return text, answer


# Словарь: ключ типа задания -> функция-генератор.
# Ключи использует экран тренажёра, чтобы выбрать нужный тип.
TASKS = {
    "mult11":       gen_mult_by_11,
    "square5":      gen_square5,
    "percent":      gen_percent,
    "divisibility": gen_divisible,
    "add_sub":      gen_add_sub,
    "mult_5_9_25":  gen_mult_5_9_25,
}


def random_task(kind):
    """Создать одно задание выбранного типа.
    Если kind == "mix" — режим «вперемешку»: берём случайный тип."""
    if kind == "mix":
        kind = random.choice(list(TASKS.keys()))
    return TASKS[kind]()
