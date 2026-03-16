def generate_questions(structure: dict, risks: list) -> list:

    questions = []

    if not structure.get("parties"):
        questions.append("Who are the legal parties of the agreement?")

    if not structure.get("payment_terms"):
        questions.append("What are the payment terms?")

    if not structure.get("duration"):
        questions.append("What is the duration of the contract?")

    if not structure.get("liability"):
        questions.append("What liability clauses exist?")

    if not structure.get("termination"):
        questions.append("How can the contract be terminated?")

    if risks:
        questions.append("Are the detected risk clauses acceptable?")

    return questions
