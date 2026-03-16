from core.module_registry import ACTIVE_MODULES
from core.result.result_builder import build_result


def run_core(text, mode="document"):
    state = {
        "text": text,
        "mode": mode,
        "processed_text": text,
        "structure_data": {},
        "risks": [],
        "questions": [],
    }

    for module in ACTIVE_MODULES:
        state = module(state)

    return build_result(
        text=state["processed_text"],
        structure_data=state["structure_data"],
        risks=state["risks"],
        questions=state["questions"],
    )


if __name__ == "__main__":
    test_text = (
        "Service agreement between Company A and Company B. "
        "Payment 5000 USD. Penalty for delay."
    )
    analysis = run_core(test_text, mode="document")
    print(analysis)
