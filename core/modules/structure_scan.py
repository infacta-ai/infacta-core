from core.frames.contract_frame_v1 import CONTRACT_FRAME_V1
from core.contract_types.type_detector import detect_contract_type


def _check_keywords(text: str, keywords: list) -> bool:
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in keywords)


def scan_structure(state: dict) -> dict:
    text = state.get("processed_text", "")
    text_lower = text.lower()

    contract_type = detect_contract_type(text)
    frame = CONTRACT_FRAME_V1["generic"]

    structure = {}

    for field, keywords in frame.items():
        if field == "date":
            structure[field] = any(ch.isdigit() for ch in text)
        else:
            structure[field] = _check_keywords(text, keywords)

    found_elements = [key for key, value in structure.items() if value]
    missing_elements = [key for key, value in structure.items() if not value]

    total = len(structure)
    score = round((len(found_elements) / total) * 100) if total else 0

    state["contract_type"] = contract_type
    state["structure"] = structure
    state["found_elements"] = found_elements
    state["missing_elements_raw"] = missing_elements
    state["structure_score"] = score

    return state
