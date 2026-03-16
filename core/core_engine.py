def run_core(text, mode="document"):

    result = {
        "summary": "",
        "simplified_text": "",
        "risks": [],
        "missing_elements": [],
        "questions": [],
        "notes": []
    }

    text_lower = text.lower()

    # simple structure scan
    has_date = any(char.isdigit() for char in text)
    has_parties = "agreement" in text_lower or "contract" in text_lower
    has_money = "$" in text or "usd" in text_lower or "eur" in text_lower

    # missing elements detection
    if not has_date:
        result["missing_elements"].append("No clear date detected")

    if not has_parties:
        result["missing_elements"].append("No parties defined")

    if not has_money:
        result["missing_elements"].append("No payment terms detected")

    # risk scan
    if "penalty" in text_lower:
        result["risks"].append("Penalty clause detected")

    if "automatic renewal" in text_lower:
        result["risks"].append("Automatic renewal clause")

    # questions generator
    for item in result["missing_elements"]:
        result["questions"].append(f"Clarify: {item}")

    # simplified explanation
    result["simplified_text"] = text[:300]

    result["summary"] = "Basic contract scan completed."

    return result
