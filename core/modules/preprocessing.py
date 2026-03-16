from core.utils.text_cleaner import clean_text


def preprocess_text(state: dict) -> dict:
    raw_text = state.get("text", "")
    state["processed_text"] = clean_text(raw_text)
    return state
