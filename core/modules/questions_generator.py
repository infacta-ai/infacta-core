QUESTION_MAP = {
    "parties": "Уточнити: хто є сторонами договору?",
    "payment_terms": "Уточнити: які умови оплати?",
    "duration": "Уточнити: який строк / термін дії договору?",
    "liability": "Уточнити: яка відповідальність сторін?",
    "termination": "Уточнити: як може бути розірваний договір?",
    "date": "Уточнити: яка дата документа або договору?",
    "signature": "Уточнити: чи є підпис / підтвердження сторін?",
}


def generate_questions(state: dict) -> dict:
    missing_elements = state.get("missing_elements_raw", [])
    risks = state.get("risks", [])

    questions = []

    for item in missing_elements:
        if item in QUESTION_MAP:
            questions.append(QUESTION_MAP[item])

    if risks:
        questions.append("Уточнити: чи прийнятні виявлені ризикові умови?")

    state["questions"] = questions
    return state
