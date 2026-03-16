def scan_risks(state: dict) -> dict:
    text = state.get("processed_text", "")
    text_lower = text.lower()

    risks = []

    if "штраф" in text_lower or "penalty" in text_lower:
        risks.append("Виявлено пункт про штраф")

    if "односторон" in text_lower or "unilateral" in text_lower:
        risks.append("Виявлено можливі односторонні зобов’язання")

    if "без відповідальності" in text_lower or "no liability" in text_lower:
        risks.append("Виявлено можливе обмеження відповідальності")

    if (
        "автоматичне продовження" in text_lower
        or "automatic renewal" in text_lower
        or "auto renewal" in text_lower
    ):
        risks.append("Виявлено автоматичне продовження договору")

    if "non-refundable" in text_lower:
        risks.append("Виявлено умову без повернення коштів")

    if "exclusive jurisdiction" in text_lower:
        risks.append("Виявлено обмежену або спеціальну юрисдикцію спорів")

    state["risks"] = risks
    return state
