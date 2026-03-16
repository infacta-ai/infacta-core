def scan_structure(text: str) -> dict:
    text_lower = text.lower()

    elements = {
        "parties": False,
        "payment_terms": False,
        "duration": False,
        "liability": False,
        "termination": False
    }

    if "сторони" in text_lower or "parties" in text_lower:
        elements["parties"] = True

    if "оплата" in text_lower or "payment" in text_lower:
        elements["payment_terms"] = True

    if "строк" in text_lower or "term" in text_lower:
        elements["duration"] = True

    if "відповідальність" in text_lower or "liability" in text_lower:
        elements["liability"] = True

    if "розірвання" in text_lower or "termination" in text_lower:
        elements["termination"] = True

    return elements
