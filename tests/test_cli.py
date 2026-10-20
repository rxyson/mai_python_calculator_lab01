import subprocess
import sys


def test_cli_calculate():
    # Тесты ниже проверяют запуск программы через CLI, а не отдельные функции.
    result = subprocess.run(
        [
            sys.executable,
            '-m',
            'toolkit',
            'calc',
            '5 + 10 * 8',
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert result.stdout == "85\n"
    assert result.stderr == ""


def test_cli_division_by_zero() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "toolkit",
            "calc",
            "10 / 0",
        ],
        capture_output=True,
        text=True,
        check=False,
       )

    assert result.returncode == 2
    assert 'Ошибка' in result.stderr


def test_cli_help() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "toolkit", "--help"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "calc" in result.stdout
    assert "convert" in result.stdout


def test_cli_convert() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "toolkit",
            "convert",
            "100",
            "--from",
            "cm",
            "--to",
            "m"
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert result.stdout == "1.0\n"
    assert result.stderr == ""


def test_cli_incompatible_units() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "toolkit",
            "convert",
            "100",
            "--from",
            "cm",
            "--to",
            "kg",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 2
    assert "Ошибка" in result.stderr
