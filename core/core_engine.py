from core.module_registry import ACTIVE_MODULES
from core.result.result_builder import build_result


def run_core(text: str, mode: str = "document") -> dict:
    state = {
        "text": text,
        "mode": mode,
        "processed_text": "",
        "structure": {},
        "found_elements": [],
        "missing_elements_raw": [],
        "structure_score": 0,
        "risks": [],
        "questions": [],
    }

    for module in ACTIVE_MODULES:
        state = module(state)

    return build_result(state)


if __name__ == "__main__":
    test_text = (
        "Service agreement between Company A and Company B. "
        "Payment 5000 USD. Penalty for delay."
    )
    print(run_core(test_text))
