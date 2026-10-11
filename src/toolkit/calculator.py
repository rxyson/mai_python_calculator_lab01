def tokenize(expression: str) -> list[tuple[str, str | float]]:
    tokens: list[tuple[str, str | float]] = []
    state = "START"
    current_token = ""
    unary = True

    for char in expression:
        if state == "START":
            if char.isdigit():
                state = "NUMBER"
                current_token = char
                unary = False
            elif char in "+-":
                if unary:
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
            if char.isdigit():
                current_token += char
                state = "NUMBER"
                unary = False
            else:
                raise ValueError("После знака ожидалось число")

        elif state == "NUMBER":
            if char.isdigit():
                current_token += char
            elif char == ".":
                current_token += char
                state = "DOT_AFTER_INT"
            else:
                tokens.append(("NUMBER", float(current_token)))
                current_token = ""
                state = "START"
                unary = False

                if char in "+-*/":
                    tokens.append(("OPERATOR", char))
                    unary = True
                elif char.isspace():
                    continue
                else:
                    raise ValueError(f"Неизвестный символ: {char}")

        elif state == "DOT_AFTER_INT":
            if char.isdigit():
                current_token += char
                state = "NUMBER"
            else:
                raise ValueError("Некорректное число")

    if state == "NUMBER":
        tokens.append(("NUMBER", float(current_token)))

    return tokens

def validate(tokens: list[tuple[str, str | float]]) -> None:
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


def calculate(tokens):
    result = tokens[0][1]
    priority = []
    i = 1

    while i < len(tokens):
        operator = tokens[i][1]
        number = tokens[i+1][1]

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
    i = 1

    while i < len(priority):
        operator = priority[i]
        number = priority[i+1]

        if operator == "+":
            result += number
        elif operator == "-":
            result -= number

        i += 2

    return result

def evaluate(expression):
    tokens = tokenize(expression)
    validate(tokens)
    return calculate(tokens)
