def detect_contract_type(text: str) -> str:
    text_lower = text.lower()

    if any(word in text_lower for word in ["mortgage", "іпотека", "іпотечн"]):
        return "mortgage"

    if any(word in text_lower for word in ["lease", "rent", "оренда", "оренд"]):
        return "lease"

    if any(word in text_lower for word in ["employment", "employee", "роботодав", "працівник", "трудов"]):
        return "employment"

    if any(word in text_lower for word in ["nda", "non-disclosure", "confidentiality", "конфіденцій"]):
        return "nda"

    if any(word in text_lower for word in ["subscription", "saas", "monthly plan", "підписка"]):
        return "subscription"

    return "generic"
