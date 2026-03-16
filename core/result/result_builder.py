def build_result(text: str, structure: dict, risks: list, questions: list) -> dict:
    missing_elements = [name for name, exists in structure.items() if not exists]
    found_elements = [name for name, exists in structure.items() if exists]

    total = len(structure)
    score = round((len(found_elements) / total) * 100) if total else 0

    if score >= 80:
        status = "структура виглядає сильною"
    elif score >= 60:
        status = "структура виглядає базово достатньою"
    elif score >= 40:
        status = "структура виглядає слабкою"
    else:
        status = "структура виглядає дуже неповною"

    summary = f"Базовий аналіз завершено. Покриття структури: {score}%. Загалом {status}."

    notes = [
        f"Покриття структури: {score}%",
        f"Знайдено елементів: {len(found_elements)} із {total}"
    ]

    return {
        "summary": summary,
        "simplified_text": text[:500] if text else "",
        "risks": risks,
        "missing_elements": [f"Не виявлено: {item}" for item in missing_elements],
        "questions": questions,
        "notes": notes,
    }
