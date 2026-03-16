from core.modules.preprocessing import preprocess_text
from core.modules.structure_scan import scan_structure
from core.modules.risk_scan import scan_risks
from core.modules.questions_generator import generate_questions
from core.result.result_builder import build_result


def run_core(text: str, mode: str = "document") -> dict:
    cleaned = preprocess_text(text)
    structure = scan_structure(cleaned)
    risks = scan_risks(cleaned)
    questions = generate_questions(structure, risks)

    return build_result(
        text=cleaned,
        structure=structure,
        risks=risks,
        questions=questions
    )
