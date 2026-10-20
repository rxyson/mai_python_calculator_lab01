"""Командный интерфейс калькулятора и конвертера."""

import argparse
import sys

from .calculator import evaluate
from .converter import convert
from .errors import ToolkitError


def main() -> int:

    """Обрабатывает команды CLI и возвращает код завершения.

    Returns:
        0 при успешном выполнении команды;
        2 при ошибке вычисления или преобразования.
    """

    parser = argparse.ArgumentParser(
        prog="python -m toolkit",
        description="Калькулятор и конвертер единиц измерения",
    )

    commands = parser.add_subparsers(
        dest="command",
        required=True,
    )

    calc_parser = commands.add_parser(
        "calc",
        help="Вычислить математическое выражение",
    )
    calc_parser.add_argument(
        "expression",
        help="Математическое выражение, например '(2 + 3) * 4'",
    )

    convert_parser = commands.add_parser(
        "convert",
        help="Конвертировать значение из одной единицы в другую",
    )
    convert_parser.add_argument(
        "value",
        type=float,
        help="Значение для преобразования",
    )
    convert_parser.add_argument(
        "--from",
        dest="from_unit",
        required=True,
        help="Начальная единица измерения",
    )
    convert_parser.add_argument(
        "--to",
        dest="to_unit",
        required=True,
        help="Новая единица измерения",
    )

    argv = sys.argv[1:]

    if len(argv) >= 2 and argv[0] == "calc" and argv[1].startswith("-"):
        argv.insert(1, "--")

    args = parser.parse_args(argv)

    try:
        if args.command == "calc":
            result = evaluate(args.expression)
        else:
            result = convert(
                args.value,
                args.from_unit,
                args.to_unit,
            )
    except (ToolkitError, ValueError, ZeroDivisionError) as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 2

    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
