def scan_risks(text: str) -> list:
    text_lower = text.lower()
    risks = []

    if "штраф" in text_lower or "penalty" in text_lower:
        risks.append("Document contains penalty clauses")

    if "односторон" in text_lower or "unilateral" in text_lower:
        risks.append("Possible unilateral obligations detected")

    if "без відповідальності" in text_lower or "no liability" in text_lower:
        risks.append("Possible liability limitation")

    if "автоматичне продовження" in text_lower or "auto renewal" in text_lower:
        risks.append("Automatic renewal clause detected")

    return risks
