import re


def analyze_document(text: str) -> dict:

    dates = re.findall(r"\b\d{2}\.\d{2}\.\d{4}\b", text)

    numbers = re.findall(r"\b№?\s*\d+\b", text)

    unit_words = [
        "рота",
        "батальйон",
        "бригада",
        "взвод",
        "підрозділ"
    ]

    has_unit = any(word in text.lower() for word in unit_words)

    result = {
        "length": len(text),
        "dates": dates,
        "numbers": numbers,
        "unit_detected": has_unit
    }

    return result
