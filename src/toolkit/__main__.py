"""Командный интерфейс калькулятора и конвертера."""

import argparse
import sys

from .calculator import evaluate
from .converter import convert
from .errors import ToolkitError


def main() -> int:
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
        help="Математическое выражение, например '2 + 3 * 4'",
    )

    convert_parser = commands.add_parser(
        "convert",
        help="Преобразовать значение между единицами",
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
        help="Исходная единица измерения",
    )
    convert_parser.add_argument(
        "--to",
        dest="to_unit",
        required=True,
        help="Целевая единица измерения",
    )

    args = parser.parse_args()

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
