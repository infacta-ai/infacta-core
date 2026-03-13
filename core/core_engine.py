def analyze_document(text):

    result = {}

    # simple structure check
    result["has_date"] = "date" in text.lower()
    result["has_number"] = any(char.isdigit() for char in text)

    # basic evaluation
    if result["has_date"] and result["has_number"]:
        result["risk_level"] = "low"
    else:
        result["risk_level"] = "medium"

    return result


if __name__ == "__main__":

    test_text = "Test document dated 12.03.2026 order 123"

    analysis = analyze_document(test_text)

    print("Infacta Core Analysis")
    print(analysis)
