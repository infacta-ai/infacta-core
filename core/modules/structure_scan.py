from core.frames.contract_frame_v1 import CONTRACT_FRAME_V1


def scan_structure(state: dict) -> dict:
    text = state.get("processed_text", "").lower()

    structure = {}
    found_elements = []
    missing_elements = []

    frame = CONTRACT_FRAME_V1.get("generic", {})

    for element, keywords in frame.items():

        found = False

        for keyword in keywords:
            if keyword.lower() in text:
                found = True
                break

        structure[element] = found

        if found:
            found_elements.append(element)
        else:
            missing_elements.append(element)

    total = len(frame)
    score = round((len(found_elements) / total) * 100) if total else 0

    state["structure"] = structure
    state["found_elements"] = found_elements
    state["missing_elements_raw"] = missing_elements
    state["structure_score"] = score

    return state
