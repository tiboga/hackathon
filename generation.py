import random


def get_numbers(level):
    if level == 'easy':
        return random.randint(1, 10), random.randint(1, 10)
    elif level == 'medium':
        return random.randint(10, 100), random.randint(10, 100)
    elif level == 'hard':
        return random.randint(100, 1000), random.randint(100, 1000)


def generate_example(level='easy', example_type='addition'):
    """
    Генерирует математический пример в зависимости от уровня сложности и типа примера.

    Args:
    - level (str): Уровень сложности ('easy', 'medium', 'hard').
    - example_type (str): Тип примера ('addition', 'subtraction', 'multiplication', 'division', 'equality', 'quadratic', 'x_inequality').

    Returns:
    - str: Сгенерированный пример.
    - str: Правильный ответ на пример.
    """

    a, b = get_numbers(level)

    if example_type == 'addition':
        example = f"{a} + {b}"
        answer = str(a + b)
    elif example_type == 'subtraction':
        example = f"{a} - {b}"
        answer = str(a - b)
    elif example_type == 'multiplication':
        example = f"{a} * {b}"
        answer = str(a * b)
    elif example_type == 'division':
        while b == 0 or a % b != 0 or a == b or b == 1:
            a, b = get_numbers(level)
        example = f"{a} / {b}"
        answer = str(a // b)
    elif example_type == 'equality':
        x = random.randint(1, 10)
        example = f"{a} * x = {a * x}"
        answer = str(x)
    elif example_type == 'quadratic':
        # Ensure integer roots for quadratic equations: (x - r1)(x - r2) = 0
        if level == 'easy':
            r1, r2 = random.randint(2, 10), random.randint(2, 10)
        elif level == 'medium':
            r1, r2 = random.randint(10, 15), random.randint(10, 15)
        else:
            r1, r2 = random.randint(15, 20), random.randint(15, 20)
        while r1 == r2:
            r2 = random.randint(2, 10)
        a = 1  # To simplify, we take a as 1
        b = -(r1 + r2)
        c = r1 * r2
        example = f"x²-{-b}x+{c}=0"
        answer = f"x = {r1}, x = {r2}"
    elif example_type == 'x_inequality':
        a = random.randint(1, 10)
        while a == 1:  # Avoid a = 1 to make the example more interesting
            a = random.randint(1, 10)
        b = random.randint(-10, 10)
        c = random.randint(-10, 10)
        operator = random.choice(['<', '>', '<=', '>='])

        # Ensure the solution (c - b) / a is an integer
        while (c - b) % a != 0:
            a, b, c = random.randint(1, 10), random.randint(-10, 10), random.randint(-10, 10)

        example = f"{a if a != 1 else ''}x {'+' if b >= 0 else '-'} {abs(b)} {operator} {c}"
        result = (c - b) // a

        if operator == '<':
            answer = f"x < {result}"
        elif operator == '>':
            answer = f"x > {result}"
        elif operator == '<=':
            answer = f"x <= {result}"
        elif operator == '>=':
            answer = f"x >= {result}"
    else:
        raise ValueError("Invalid example type provided.")

    return example, answer


# Примеры использования функции
# examples = [
#     generate_example('easy', 'addition'),
#     generate_example('medium', 'subtraction'),
#     generate_example('hard', 'multiplication'),
#     generate_example('easy', 'division'),
#     generate_example('hard', 'equality'),
#     generate_example('hard', 'quadratic'),
#     generate_example('easy', 'x_inequality')
# ]
#
# for example, answer in examples:
#     print(f"Example: {example}, Answer: {answer}")
