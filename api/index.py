from flask import Flask, request

app = Flask(__name__)


def analyze_text(text: str):
    lowered = text.lower()

    number_tokens = []
    current_number = ""
    for ch in text:
        if ch.isdigit():
            current_number += ch
        else:
            if current_number:
                number_tokens.append(current_number)
                current_number = ""
    if current_number:
        number_tokens.append(current_number)

    time_words = [
        "today", "yesterday", "tomorrow", "last night", "this morning",
        "сьогодні", "вчора", "завтра", "вночі", "ранком", "зранку"
    ]

    source_hints = [
        "according to", "source", "reported by", "reuters", "bbc", "cnn",
        "за даними", "за словами", "джерело", "повідомляє", "згідно з"
    ]

    evidence_hints = [
        "photo", "video", "document", "evidence", "proof", "confirmed",
        "фото", "відео", "документ", "доказ", "підтверджено"
    ]

    context_hints = [
        "because", "after", "before", "during", "in the region", "at the time",
        "тому що", "після", "до", "під час", "у районі", "на той момент"
    ]

    action_verbs = [
        "destroyed", "attacked", "captured", "killed", "declared", "announced",
        "confirmed", "reported", "detected", "verified",
        "знищив", "знищили", "атакував", "атакували", "заявив", "заявили",
        "оголосив", "оголосили", "підтвердив", "підтвердили", "виявив", "виявили"
    ]

    found_time_words = [w for w in time_words if w in lowered]
    found_action_verbs = [w for w in action_verbs if w in lowered]

    has_source = any(hint in lowered for hint in source_hints)
    has_evidence = any(hint in lowered for hint in evidence_hints)
    has_context = any(hint in lowered for hint in context_hints)
    has_date = any(token.isdigit() and len(token) == 4 for token in number_tokens) or len(found_time_words) > 0
    has_claim = len(found_action_verbs) > 0 or len(number_tokens) > 0

    structure = {
        "source": "present" if has_source else "missing",
        "date": "present" if has_date else "missing",
        "context": "present" if has_context else "missing",
        "evidence": "present" if has_evidence else "missing",
        "claim": "present" if has_claim else "missing",
    }

    present_count = sum(1 for v in structure.values() if v == "present")
    coverage = round((present_count / 5) * 100)

    missing = [k for k, v in structure.items() if v == "missing"]
    critical_unknowns = [x for x in missing if x in ["source", "evidence"]]

    if coverage >= 80 and len(critical_unknowns) == 0:
        reliability = "HIGH"
    elif coverage >= 50:
        reliability = "MEDIUM"
    else:
        reliability = "LOW"

    if coverage < 30:
        maturity = "Level 1"
    elif coverage < 50:
        maturity = "Level 2"
    elif coverage < 70:
        maturity = "Level 3"
    elif coverage < 90:
        maturity = "Level 4"
    else:
        maturity = "Level 5"

    reasons = []
    if not has_source:
        reasons.append("Source missing")
    if not has_evidence:
        reasons.append("Evidence missing")
    if not has_context:
        reasons.append("Context weak or missing")
    if not has_date:
        reasons.append("Date or time reference missing")
    if not has_claim:
        reasons.append("Clear claim not detected")

    return {
        "text_length": len(text),
        "numbers": number_tokens,
        "time_words": found_time_words,
        "action_verbs": found_action_verbs,
        "structure": structure,
        "coverage": coverage,
        "missing": missing,
        "critical_unknowns": critical_unknowns,
        "reliability": reliability,
        "maturity": maturity,
        "reasons": reasons,
    }


def render_page(result_html="", text_value="New drone system destroyed 20 tanks yesterday."):
    return f"""
<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Інфакта</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background: #f5f7fb;
            color: #1f2937;
            margin: 0;
            padding: 40px 20px;
        }}
        .container {{
            max-width: 950px;
            margin: 0 auto;
        }}
        h1 {{
            margin-bottom: 6px;
            font-size: 42px;
        }}
        .subtitle {{
            color: #6b7280;
            margin-bottom: 24px;
        }}
        .card {{
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.04);
        }}
        .visible-box {{
            background: #f9fafb;
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 20px;
            color: #374151;
        }}
        textarea {{
            width: 100%;
            min-height: 180px;
            border-radius: 12px;
            border: 1px solid #d1d5db;
            padding: 14px;
            font-size: 16px;
            box-sizing: border-box;
            resize: vertical;
        }}
        button {{
            margin-top: 14px;
            background: #2563eb;
            color: white;
            border: none;
            border-radius: 10px;
            padding: 12px 20px;
            font-size: 16px;
            cursor: pointer;
        }}
        button:hover {{
            background: #1d4ed8;
        }}
        .badge {{
            display: inline-block;
            padding: 6px 12px;
            border-radius: 999px;
            color: white;
            font-weight: bold;
            font-size: 14px;
        }}
        .high {{ background: #16a34a; }}
        .medium {{ background: #d97706; }}
        .low {{ background: #dc2626; }}
        ul {{
            margin: 8px 0 0 20px;
        }}
        .line {{
            margin-bottom: 8px;
        }}
        .small-title {{
            margin-bottom: 10px;
            font-size: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Інфакта</h1>
        <div class="subtitle">Верифікація інформації на основі структури</div>

        <div class="visible-box">
            <strong>Видимий аналіз:</strong><br>
            1. Перевірка структури<br>
            2. Виявлення чисел і часових маркерів<br>
            3. Оцінка покриття структури<br>
            4. Побудова карти невідомого<br>
            5. Оцінка достовірності та зрілості аналізу
        </div>

        <div class="card">
            <div class="small-title">Перевірити інформацію</div>

            <form method="POST" action="/analyze">
                <textarea name="text">{text_value}</textarea>
                <br>
                <button type="submit">Аналізуй</button>
            </form>
        </div>

        {result_html}
    </div>
</body>
</html>
"""


@app.route("/", methods=["GET"])
def home():
    return render_page()


@app.route("/analyze", methods=["POST"])
def analyze():
    text = request.form.get("text", "").strip()

    if not text:
        return render_page(
            result_html="""
            <div class="card">
                <div class="small-title">Помилка</div>
                <div class="line"><strong>Текст не передано.</strong></div>
            </div>
            """,
            text_value=""
        )

    data = analyze_text(text)

    reliability_class = "low"
    if data["reliability"] == "HIGH":
        reliability_class = "high"
    elif data["reliability"] == "MEDIUM":
        reliability_class = "medium"

    result_html = f"""
    <div class="card">
        <div class="small-title">Результат аналізу</div>
        <div class="line"><strong>Достовірність:</strong> <span class="badge {reliability_class}">{data["reliability"]}</span></div>
        <div class="line"><strong>Рівень зрілості аналізу:</strong> {data["maturity"]}</div>
        <div class="line"><strong>Покриття структури:</strong> {data["coverage"]}%</div>
        <div class="line"><strong>Довжина тексту:</strong> {data["text_length"]}</div>
    </div>

    <div class="card">
        <div class="small-title">Виявлені елементи</div>
        <div class="line"><strong>Числа:</strong> {", ".join(data["numbers"]) if data["numbers"] else "Немає"}</div>
        <div class="line"><strong>Часові маркери:</strong> {", ".join(data["time_words"]) if data["time_words"] else "Немає"}</div>
        <div class="line"><strong>Дієслова дії:</strong> {", ".join(data["action_verbs"]) if data["action_verbs"] else "Немає"}</div>
    </div>

    <div class="card">
        <div class="small-title">Перевірка структури</div>
        <ul>
            <li>Джерело: {data["structure"]["source"]}</li>
            <li>Дата: {data["structure"]["date"]}</li>
            <li>Контекст: {data["structure"]["context"]}</li>
            <li>Докази: {data["structure"]["evidence"]}</li>
            <li>Твердження: {data["structure"]["claim"]}</li>
        </ul>
    </div>

    <div class="card">
        <div class="small-title">Карта невідомого</div>
        <div class="line"><strong>Відсутні елементи:</strong> {", ".join(data["missing"]) if data["missing"] else "Немає"}</div>
        <div class="line"><strong>Критичні прогалини:</strong> {", ".join(data["critical_unknowns"]) if data["critical_unknowns"] else "Немає"}</div>
    </div>

    <div class="card">
        <div class="small-title">Причини оцінки</div>
        <ul>
            {"".join(f"<li>{item}</li>" for item in data["reasons"])} 
        </ul>
    </div>
    """

    return render_page(result_html=result_html, text_value=text)


# Vercel looks for `app`
