LENGTH_UNITS = {
    "mm": 0.001,
    "cm": 0.01,
    "m": 1.0,
    "km": 1000.0,
}

MASS_UNITS = {
    "g": 1.0,
    "kg": 1000.0,
}

TEMPERATUE_UNITS = {"c", "f", "k"}

all_units = set(LENGTH_UNITS) | set(MASS_UNITS) | set(TEMPERATUE_UNITS)

def convert(value: float, from_unit: str, to_unit: str):
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()

    if from_unit not in all_units or to_unit not in all_units:
        raise ValueError("Неизвестная единица")
    if from_unit in TEMPERATUE_UNITS and to_unit in TEMPERATUE_UNITS:
        if from_unit == "c":
            celsius = value
        elif from_unit == "f":
            celsius = (value - 32) * 5 / 9
        elif from_unit == "k":
            celsius = value - 273.15

        if celsius < -273.15:
            raise ValueError("Температура ниже абсолютного нуля")

        if to_unit == "c":
            return(float(celsius))
        elif to_unit == "f":
            return float(celsius * 9 / 5 + 32)
        elif to_unit == "k":
            return float(celsius + 273.15)

    if from_unit in LENGTH_UNITS and to_unit in LENGTH_UNITS:
        if value < 0:
            raise ValueError("Длина не может быть отрицательной")
        units = LENGTH_UNITS
    elif from_unit in MASS_UNITS and to_unit in MASS_UNITS:
        if value < 0:
            raise ValueError("Масса не может быть отрицательной")
        units = MASS_UNITS
    else:
        raise ValueError(f"Невозможно конвертировать между разными группами единиц: {from_unit} и {to_unit}")

    from_value = units[from_unit]
    to_value = units[to_unit]

    result = value * from_value / to_value

    return float(result)
