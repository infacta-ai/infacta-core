def detect_contract_type(text: str) -> str:
    text_lower = text.lower()

    if (
        "іпотек" in text_lower
        or "mortgage" in text_lower
        or "іпотекодав" in text_lower
        or "іпотекодерж" in text_lower
    ):
        return "mortgage"

    if (
        "оренда" in text_lower
        or "lease" in text_lower
        or "орендодав" in text_lower
        or "орендар" in text_lower
    ):
        return "lease"

    if (
        "employment" in text_lower
        or "трудов" in text_lower
        or "працівник" in text_lower
        or "роботодавець" in text_lower
    ):
        return "employment"

    if (
        "nda" in text_lower
        or "non-disclosure" in text_lower
        or "confidentiality" in text_lower
        or "конфіденці" in text_lower
    ):
        return "nda"

    if (
        "subscription" in text_lower
        or "saas" in text_lower
        or "auto renewal" in text_lower
        or "renewal" in text_lower
    ):
        return "subscription"

    return "generic"
