def run_core(text, mode="document"):
    result = {
        "summary": "",
        "simplified_text": "",
        "risks": [],
        "missing_elements": [],
        "questions": [],
        "notes": [],
        "structure_score": 0,
        "found_elements": [],
    }

    text_lower = text.lower()

    # Базові структурні перевірки для document/contract-first MVP
    checks = {
        "Дата": any(ch.isdigit() for ch in text),
        "Сторони": (
            "agreement" in text_lower
            or "contract" in text_lower
            or "company" in text_lower
            or "party" in text_lower
        ),
        "Оплата / сума": (
            "$" in text
            or "usd" in text_lower
            or "eur" in text_lower
            or "uah" in text_lower
            or "payment" in text_lower
            or "price" in text_lower
            or "cost" in text_lower
        ),
        "Предмет / опис": (
            "service" in text_lower
            or "product" in text_lower
            or "goods" in text_lower
            or "subject" in text_lower
            or "work" in text_lower
        ),
        "Строк / термін": (
            "term" in text_lower
            or "duration" in text_lower
            or "period" in text_lower
            or "until" in text_lower
            or "deadline" in text_lower
        ),
        "Відповідальність / санкції": (
            "penalty" in text_lower
            or "liability" in text_lower
            or "fine" in text_lower
        ),
        "Підпис / підтвердження": (
            "signature" in text_lower
            or "signed" in text_lower
            or "signatory" in text_lower
        ),
    }

    total_checks = len(checks)
    found = [name for name, ok in checks.items() if ok]
    missing = [name for name, ok in checks.items() if not ok]

    result["found_elements"] = found
    result["structure_score"] = round((len(found) / total_checks) * 100)

    # Missing elements
    result["missing_elements"] = [f"Не виявлено: {item}" for item in missing]

    # Risks
    if "penalty" in text_lower:
        result["risks"].append("Виявлено пункт про штраф / penalty clause")

    if "automatic renewal" in text_lower:
        result["risks"].append("Виявлено автоматичне продовження договору")

    if "exclusive jurisdiction" in text_lower:
        result["risks"].append("Виявлено спеціальну / обмежену юрисдикцію спорів")

    if "non-refundable" in text_lower:
        result["risks"].append("Виявлено умову non-refundable")

    # Questions
    for item in missing:
        result["questions"].append(f"Уточнити: {item}")

    # Notes
    result["notes"].append(f"Покриття структури: {result['structure_score']}%")
    result["notes"].append(f"Знайдено елементів: {len(found)} із {total_checks}")

    # Simplified explanation
    simplified_preview = text.strip()[:500]
    result["simplified_text"] = simplified_preview if simplified_preview else "Текст відсутній."

    # Summary
    if result["structure_score"] >= 80:
        structure_status = "структура виглядає сильною"
    elif result["structure_score"] >= 60:
        structure_status = "структура виглядає базово достатньою"
    elif result["structure_score"] >= 40:
        structure_status = "структура виглядає слабкою"
    else:
        structure_status = "структура виглядає дуже неповною"

    result["summary"] = (
        f"Базовий аналіз завершено. Покриття структури: "
        f"{result['structure_score']}%. Загалом {structure_status}."
    )

    return result


if __name__ == "__main__":
    test_text = (
        "Service agreement between Company A and Company B. "
        "Payment 5000 USD. Penalty for delay."
    )
    analysis = run_core(test_text, mode="document")
    print(analysis)
