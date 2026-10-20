"""Функции для разбора и вычисления математических выражений."""

def tokenize(expression: str) -> list[tuple[str, str | float | int]]:
    """Разбивает математическое выражение на токены."""
    tokens: list[tuple[str, str | float | int]] = []
    state = "START"
    current_token = ""
    unary = True
    id = 1

    for char in expression:
        if state == "START":
            if char == "(":
                tokens.append(("PAREN", char))
                unary = True
            elif char == ")":
                tokens.append(("PAREN", char))
                unary = False
            elif char.isdigit():
                state = "NUMBER"
                current_token = char
                unary = False
            elif char in "+-":
                if unary:
                    if char == "-":
                        id *= -1

                    current_token = char
                    state = "SIGNED_NUMBER"
                else:
                    tokens.append(("OPERATOR", char))
                    unary = True
            elif char in "*/":
                tokens.append(("OPERATOR", char))
                unary = True
            elif char.isspace():
                continue
            else:
                raise ValueError(f"Неизвестный символ: {char}")

        elif state == "SIGNED_NUMBER":
            if char in "+-":
                if char == "-":
                    id *= -1
                current_token += char
            elif char.isdigit():
                current_token += char
                state = "NUMBER"
                unary = False
            elif char.isspace():
                continue
            else:
                raise ValueError("После знака ожидалось число")

        elif state == "NUMBER":
            if char.isdigit():
                current_token += char
            elif char == ".":
                current_token += char
                state = "DOT_AFTER_INT"
            else:
                number_text = current_token.lstrip("+-")
                number = float(number_text) if "." in number_text else int(number_text)
                tokens.append(("NUMBER", id * number))
                id = 1
                current_token = ""
                state = "START"
                unary = False

                if char in "+-*/":
                    tokens.append(("OPERATOR", char))
                    unary = True
                elif char == "(":
                    tokens.append(("PAREN", char))
                    unary = True
                elif char == ")":
                    tokens.append(("PAREN", char))
                    unary = False
                elif char.isspace():
                    continue
                else:
                    raise ValueError(f"Неизвестный символ: {char}")

        elif state == "DOT_AFTER_INT":
            if char.isdigit():
                current_token += char
                state = "NUMBER"
            elif char.isspace():
                continue
            else:
                raise ValueError("Некорректное число")

    if state == "NUMBER":
        number_text = current_token.lstrip("+-")
        number = float(number_text) if "." in number_text else int(number_text)
        tokens.append(("NUMBER", id * number))
        id = 1

    return tokens

def validate(tokens: list[tuple[str, str | float | int]]) -> None:
    """Проверяет последовательность токенов математического выражения.
    Проверяет наличие чисел и допустимое расположение операторов."""
    if len(tokens) == 0:
        raise ValueError("Пустое выражение")

    if tokens[0][0] != "NUMBER":
        raise ValueError("Выражение должно начинаться с числа")

    if tokens[-1][0] != "NUMBER":
        raise ValueError("Выражение должно заканчиваться числом")

    for i in range(len(tokens) - 1):
        current_type, current_value = tokens[i]
        next_type, next_value = tokens[i + 1]

        if current_type == "OPERATOR" and next_type == "OPERATOR":
            raise ValueError("Два оператора подряд недопустимы")

        if current_type == "NUMBER" and next_type == "NUMBER":
            raise ValueError("Два числа подряд недопустимы")

    last_type, last_value = tokens[-1]
    if last_type == "OPERATOR":
        raise ValueError("Выражение не может заканчиваться оператором")


def calc_paren(tokens):
    while ("PAREN", "(") in tokens:
        start = -1

        for i in range(len(tokens)):
            if tokens[i] == ("PAREN", "("):
                start = i

        end = -1
        for i in range(start+1, len(tokens)):
            if tokens[i] == ("PAREN", ")"):
                end = i
                break

        if end == -1:
            raise ValueError("Не закрыта скобка")

        new_par = tokens[start + 1: end]
        validate(new_par)
        result = calculate(new_par)

        tokens = tokens[:start] + [("NUMBER", result)] + tokens[end + 1:]

    if ("PAREN", ")") in tokens:
        raise ValueError("Лишняя закрывающая скобка")

    return tokens


def calculate(tokens: list[tuple[str, str | float | int]]) -> int | float:
    """Вычисляет выражение по последовательности проверенных токенов.
    Сначала выполняет умножение и деление, затем сложение и вычитание."""
    result = tokens[0][1]
    if not isinstance(result, (int, float)):
        raise ValueError("Ожидалось число")
    priority: list[int | float | str] = []
    i = 1

    while i < len(tokens):
        operator = tokens[i][1]
        number = tokens[i+1][1]
        if not isinstance(number, (int, float)):
            raise ValueError("Ожидалось число")

        if operator == "*":
            result *= number
            i += 2
            continue

        if operator == "/":
            if number == 0:
                raise ValueError("Деление на ноль недопустимо")
            result /= number
            i += 2
            continue

        priority.append(result)
        priority.append(operator)
        result = number
        i += 2

    priority.append(result)

    result = priority[0]
    if not isinstance(result, (int, float)):
        raise ValueError("Ожидалось число")
    i = 1

    while i < len(priority):
        operator = priority[i]
        number = priority[i+1]

        if not isinstance(operator, str):
            raise ValueError("Ожидался оператор")
        if not isinstance(number, (int, float)):
            raise ValueError("Ожидалось число")

        if operator == "+":
            result += number
        elif operator == "-":
            result -= number

        i += 2

    return result

def evaluate(expression: str) -> int | float:
    """Проверяет и вычисляет математическое выражение.
    Последовательно разбивает выражение на токены, проверяет их
    корректность и передаёт на вычисление."""
    tokens = tokenize(expression)
    tokens = calc_paren(tokens)
    validate(tokens)
    return calculate(tokens)
