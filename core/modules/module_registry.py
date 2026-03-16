from core.modules.preprocessing import preprocess_text
from core.modules.structure_scan import scan_structure
from core.modules.risk_scan import scan_risks
from core.modules.questions_generator import generate_questions

ACTIVE_MODULES = [
    preprocess_text,
    scan_structure,
    scan_risks,
    generate_questions,
]
