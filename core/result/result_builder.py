def build_result(state: dict) -> dict:
    processed_text = state.get("processed_text", "")
    structure_score = state.get("structure_score", 0)
    found_elements = state.get("found_elements", [])
    missing_elements_raw = state.get("missing_elements_raw", [])
    risks = state.get("risks", [])
    questions = state.get("questions", [])

    missing_elements = [f"Не виявлено: {item}" for item in missing_elements_raw]

    notes = [
        f"Покриття структури: {structure_score}%",
        f"Знайдено елементів: {len(found_elements)} із {len(found_elements) + len(missing_elements_raw)}",
    ]

    if structure_score >= 80:
        structure_status = "структура виглядає сильною"
    elif structure_score >= 60:
        structure_status = "структура виглядає базово достатньою"
    elif structure_score >= 40:
        structure_status = "структура виглядає слабкою"
    else:
        structure_status = "структура виглядає дуже неповною"

    summary = (
        f"Базовий аналіз завершено. Покриття структури: "
        f"{structure_score}%. Загалом {structure_status}."
    )

    simplified_text = processed_text[:500] if processed_text else "Текст відсутній."

    return {
        "summary": summary,
        "simplified_text": simplified_text,
        "risks": risks,
        "missing_elements": missing_elements,
        "questions": questions,
        "notes": notes,
        "structure_score": structure_score,
        "found_elements": found_elements,
    }
