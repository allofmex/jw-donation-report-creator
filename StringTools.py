def numberToFinanceStr(number: float|int):
    """ converts 123 to "*ein-zwei-drei*" """
    mapping = {
        '0': 'null',
        '1': 'eins',
        '2': 'zwei',
        '3': 'drei',
        '4': 'vier',
        '5': 'fünf',
        '6': 'sechs',
        '7': 'sieben',
        '8': 'acht',
        '9': 'neun',
    }

    numberStr = f'{number:.0f}'
    result = ""
    prefix = ""
    for idx in range(0, len(numberStr)):
        chr = numberStr[idx]
        result += prefix + mapping[chr]
        prefix = "-"
    return result

def specialCharToAscii(text: str):
    mapping = {
        ord("ä"):  "ae",
        ord("ö"):  "oe",
        ord("ü"):  "ue",
        ord("é"):  "e"
    }
    return text.translate(mapping)
