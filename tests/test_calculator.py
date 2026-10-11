import pytest

from toolkit.calculator import evaluate

def test_addition():
    assert evaluate("2 + 2") == 4.0


def test_subtraction():
    assert evaluate("6 - 5") == 1.0


def test_multiplication():
    assert evaluate("9 * 9") == 81.0


def test_division():
    assert evaluate("100 / 5") == 20.0


def test_space_ignore():
    assert evaluate("1         + 3         *          8") == 25.0


def test_unary_minus():
    assert evaluate("-16 - -8") == -8.0


def test_unary_plus():
    assert evaluate("+10 + 3") == 13.0


def test_float_numbers():
    assert evaluate("0.2 * 0.3") == 0.06


def test_negative_number_after_multiplication():
    assert evaluate("2*-2") == -4.0


def test_negative_number_after_division():
    assert evaluate("2/-2") == -1.0


def test_subtract_negative_number():
    assert evaluate("2--2") == 4.0


def test_multiply_negative_numbers():
    assert evaluate("-2*-3") == 6.0


def test_empty():
    with pytest.raises(ValueError):
        evaluate("")


def test_invalid_char():
    with pytest.raises(ValueError):
        evaluate("5 + dfdfdfdf")


def test_miss_oper():
    with pytest.raises(ValueError):
        evaluate("10 2")


def test_two_oper():
    with pytest.raises(ValueError):
        evaluate("2 + / 9")


def test_division_by_zero():
    with pytest.raises(ValueError):
        evaluate("1 / 0")


def test_uncorrect_num():
    with pytest.raises(ValueError):
        evaluate("22 + 1d")


def test_uncorrect_float_char():
    with pytest.raises(ValueError):
        evaluate("34 + 2.4.3")
