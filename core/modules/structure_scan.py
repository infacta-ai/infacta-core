def scan_structure(state: dict) -> dict:
    text = state.get("processed_text", "")
    text_lower = text.lower()

    structure = {
        "parties": False,
        "payment_terms": False,
        "duration": False,
        "liability": False,
        "termination": False,
        "date": False,
        "signature": False,
    }

    if (
        "сторони" in text_lower
        or "parties" in text_lower
        or "company" in text_lower
        or "agreement between" in text_lower
        or "contract between" in text_lower
    ):
        structure["parties"] = True

    if (
        "оплата" in text_lower
        or "payment" in text_lower
        or "usd" in text_lower
        or "eur" in text_lower
        or "uah" in text_lower
        or "$" in text
        or "price" in text_lower
        or "cost" in text_lower
    ):
        structure["payment_terms"] = True

    if (
        "строк" in text_lower
        or "term" in text_lower
        or "duration" in text_lower
        or "period" in text_lower
        or "deadline" in text_lower
        or "until" in text_lower
    ):
        structure["duration"] = True

    if (
        "відповідальність" in text_lower
        or "liability" in text_lower
        or "penalty" in text_lower
        or "штраф" in text_lower
        or "fine" in text_lower
    ):
        structure["liability"] = True

    if (
        "розірвання" in text_lower
        or "termination" in text_lower
        or "terminate" in text_lower
        or "cancel" in text_lower
    ):
        structure["termination"] = True

    if any(ch.isdigit() for ch in text):
        structure["date"] = True

    if (
        "підпис" in text_lower
        or "signature" in text_lower
        or "signed" in text_lower
        or "signatory" in text_lower
    ):
        structure["signature"] = True

    found_elements = [key for key, value in structure.items() if value]
    missing_elements = [key for key, value in structure.items() if not value]

    total = len(structure)
    score = round((len(found_elements) / total) * 100) if total else 0

    state["structure"] = structure
    state["found_elements"] = found_elements
    state["missing_elements_raw"] = missing_elements
    state["structure_score"] = score

    return state
