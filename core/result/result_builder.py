FIELD_LABELS_UA = {
    "parties": "сторони договору",
    "payment_terms": "умови оплати",
    "duration": "строк / термін дії",
    "liability": "відповідальність сторін",
    "termination": "умови розірвання",
    "date": "дата документа або договору",
    "signature": "підпис / підтвердження сторін",
}

CONTRACT_TYPE_LABELS_UA = {
    "generic": "загальний договір",
    "mortgage": "іпотечний договір",
    "lease": "договір оренди",
    "employment": "трудовий договір",
    "nda": "договір про нерозголошення",
    "subscription": "договір підписки / сервісний договір",
    "service": "договір послуг",
}


def _label_field(field_key: str) -> str:
    return FIELD_LABELS_UA.get(field_key, field_key)


def _label_contract_type(contract_type: str) -> str:
    return CONTRACT_TYPE_LABELS_UA.get(contract_type, contract_type)


def build_result(state: dict) -> dict:
    processed_text = state.get("processed_text", "")
    structure_score = state.get("structure_score", 0)
    found_elements = state.get("found_elements", [])
    missing_elements_raw = state.get("missing_elements_raw", [])
    risks = state.get("risks", [])
    questions = state.get("questions", [])
    contract_type = state.get("contract_type", "generic")

    found_elements_ua = [_label_field(item) for item in found_elements]
    missing_elements_ua = [_label_field(item) for item in missing_elements_raw]

    missing_elements = [f"Не виявлено: {item}" for item in missing_elements_ua]

    contract_type_ua = _label_contract_type(contract_type)

    notes = [
        f"Тип договору: {contract_type_ua}",
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
        f"Базовий аналіз завершено. Тип: {contract_type_ua}. "
        f"Покриття структури: {structure_score}%. "
        f"Загалом {structure_status}."
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
        "found_elements": found_elements_ua,
        "contract_type": contract_type_ua,
    }
