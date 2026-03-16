from core.modules.preprocessing import preprocess_text
from core.modules.structure_scan import scan_structure
from core.modules.risk_scan import scan_risks
from core.modules.questions_generator import generate_questions


def analyze_contract(text: str):

    cleaned = preprocess_text(text)

    structure = scan_structure(cleaned)

    risks = scan_risks(cleaned)

    questions = generate_questions(structure, risks)

    result = {
        "structure": structure,
        "risks": risks,
        "questions": questions
    }

    return result
