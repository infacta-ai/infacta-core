from core.module_registry import ACTIVE_MODULES
from core.result.result_builder import build_result
from core.contract_types.type_detector import detect_contract_type


def run_core(text: str, mode: str = "document") -> dict:
    detected_type = detect_contract_type(text)

    state = {
        "text": text,
        "mode": mode,
        "contract_type": detected_type,
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
        "Типовий договір для передачі в іпотеку житлової або нежитлової нерухомості. "
        "Іпотекодавець — фізична особа."
    )
    print(run_core(test_text))
