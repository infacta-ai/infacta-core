from core.modules.preprocessing import preprocess_text
from core.modules.structure_scan import run_structure_scan
from core.modules.risk_scanner import run_risk_scan
from core.modules.questions_generator import generate_questions


def preprocessing_module(state: dict) -> dict:
    state["processed_text"] = preprocess_text(state["text"])
    return state


def structure_module(state: dict) -> dict:
    state["structure_data"] = run_structure_scan(
        state["processed_text"],
        mode=state.get("mode", "document")
    )
    return state


def risk_module(state: dict) -> dict:
    state["risks"] = run_risk_scan(state["processed_text"])
    return state


def questions_module(state: dict) -> dict:
    state["questions"] = generate_questions(
        state["structure_data"]["missing_elements"]
    )
    return state


ACTIVE_MODULES = [
    preprocessing_module,
    structure_module,
    risk_module,
    questions_module,
]
