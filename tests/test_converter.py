import pytest

from toolkit.converter import convert


def test_length_cm_to_m():
    assert convert(300, "cm", "m") == 3.0


def test_length_km_to_m():
    assert convert(2, "km", "m") == 2000.0


def test_length_mm_to_m():
    assert convert(5000, "mm", "m") == 5.0


def test_mass_kg_to_g():
    assert convert(2, "kg", "g") == 2000.0


def test_mass_g_to_kg():
    assert convert(500, "g", "kg") == 0.5


def test_temperature_c_to_f():
    assert convert(0, "c", "f") == 32.0


def test_temperature_c_to_k():
    assert convert(100, "c", "k") == 373.15


def test_temperature_k_to_c():
    assert convert(273.15, "k", "c") == 0.0


def test_temperature_f_to_c():
    assert convert(32, "f", "c") == 0.0


def test_same_unit():
    assert convert(300, "k", "k") == 300.0


def test_units_are_case_insensitive():
    assert convert(100, "CM", "M") == 1.0


def test_unknown_unit():
    with pytest.raises(ValueError, match="Неизвестная единица"):
        convert(10, "cm", "abc")


def test_incompatible_units():
    from_unit = "cm"
    to_unit = "kg"

    with pytest.raises(
        ValueError, match=f"Невозможно конвертировать между разными группами единиц: {from_unit} и {to_unit}"):
        convert(1, from_unit, to_unit)


def test_temperature_below_absolute_zero():
    with pytest.raises(ValueError, match="Температура ниже абсолютного нуля"):
        convert(-1, "k", "c")


def test_negative_length():
    with pytest.raises(ValueError, match="Длина не может быть отрицательной",):
        convert(-1, "m", "cm")


def test_negative_mass():
    with pytest.raises(ValueError, match="Масса не может быть отрицательной",):
        convert(-36, "kg", "g")
