from flask import Flask, request, render_template_string

try:
    from core.core_engine import run_core
except ImportError:
    import os
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from core.core_engine import run_core

app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<html lang="uk">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Інфакта</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f7f8fb;
            color: #1f2937;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 920px;
            margin: 40px auto;
            padding: 24px;
        }
        .card {
            background: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 14px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        }
        h1 {
            margin: 0 0 8px 0;
            font-size: 42px;
            color: #4f46e5;
        }
        .subtitle {
            margin: 0 0 18px 0;
            color: #6b7280;
            font-size: 16px;
        }
        .modes {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-bottom: 18px;
        }
        .mode {
            background: #eef2ff;
            color: #3730a3;
            border: 1px solid #c7d2fe;
            padding: 8px 12px;
            border-radius: 999px;
            font-size: 14px;
            font-weight: 600;
        }
        label {
            display: block;
            font-size: 18px;
            font-weight: 700;
            margin-bottom: 10px;
        }
        textarea {
            width: 100%;
            min-height: 220px;
            padding: 14px;
            border-radius: 10px;
            border: 1px solid #d1d5db;
            font-size: 15px;
            line-height: 1.5;
            resize: vertical;
            box-sizing: border-box;
        }
        button {
            margin-top: 14px;
            background: #4f46e5;
            color: white;
            border: none;
            border-radius: 10px;
            padding: 12px 18px;
            font-size: 15px;
            font-weight: 700;
            cursor: pointer;
        }
        button:hover {
            background: #4338ca;
        }
        h2 {
            margin-top: 0;
            font-size: 22px;
            color: #111827;
        }
        h3 {
            margin-bottom: 10px;
            color: #374151;
        }
        .block {
            margin-bottom: 18px;
        }
        .plain-box {
            background: #f9fafb;
            border: 1px solid #e5e7eb;
            border-radius: 10px;
            padding: 14px;
            white-space: pre-wrap;
            line-height: 1.55;
        }
        ul {
            margin: 0;
            padding-left: 20px;
        }
        li {
            margin-bottom: 8px;
            line-height: 1.45;
        }
        .empty {
            color: #6b7280;
            font-style: italic;
        }
        .hint {
            color: #6b7280;
            font-size: 14px;
            margin-top: 6px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <h1>Інфакта</h1>
            <p class="subtitle">Аналіз документів і договорів на основі структури</p>

            <div class="modes">
                <div class="mode">Check Document</div>
                <div class="mode">Check Contract</div>
                <div class="mode">Check Information</div>
            </div>

            <div class="plain-box">
<strong>Поточний фокус Core 0.11:</strong>
1. Сканування структури
2. Виявлення відсутніх елементів
3. Пошук базових ризиків
4. Генерація уточнюючих питань
5. Спрощене пояснення тексту
            </div>
        </div>

        <div class="card">
            <form method="post">
                <label for="text">Вставте текст документа або договору</label>
                <textarea id="text" name="text" placeholder="Вставте тут текст для аналізу...">{{ text }}</textarea>
                <div class="hint">На цьому етапі система працює як document/contract-first MVP.</div>
                <button type="submit">Аналізувати</button>
            </form>
        </div>

        {% if analysis %}
        <div class="card">
            <h2>Результат аналізу</h2>

            <div class="block">
                <h3>Короткий зміст</h3>
                <div class="plain-box">
                    {{ analysis.summary if analysis.summary else "Поки що короткий зміст не сформовано." }}
                </div>
            </div>

            <div class="block">
                <h3>Спрощене пояснення</h3>
                <div class="plain-box">
                    {{ analysis.simplified_text if analysis.simplified_text else "Поки що спрощене пояснення відсутнє." }}
                </div>
            </div>

            <div class="block">
                <h3>Ризики</h3>
                {% if analysis.risks %}
                    <ul>
                        {% for item in analysis.risks %}
                            <li>{{ item }}</li>
                        {% endfor %}
                    </ul>
                {% else %}
                    <div class="empty">Явних ризиків на базовому рівні не виявлено.</div>
                {% endif %}
            </div>

            <div class="block">
                <h3>Відсутні елементи</h3>
                {% if analysis.missing_elements %}
                    <ul>
                        {% for item in analysis.missing_elements %}
                            <li>{{ item }}</li>
                        {% endfor %}
                    </ul>
                {% else %}
                    <div class="empty">Критичних пропусків на базовому рівні не виявлено.</div>
                {% endif %}
            </div>

            <div class="block">
                <h3>Уточнюючі питання</h3>
                {% if analysis.questions %}
                    <ul>
                        {% for item in analysis.questions %}
                            <li>{{ item }}</li>
                        {% endfor %}
                    </ul>
                {% else %}
                    <div class="empty">Питання для уточнення поки що не сформовані.</div>
                {% endif %}
            </div>

            <div class="block">
                <h3>Нотатки</h3>
                {% if analysis.notes %}
                    <ul>
                        {% for item in analysis.notes %}
                            <li>{{ item }}</li>
                        {% endfor %}
                    </ul>
                {% else %}
                    <div class="empty">Додаткових нотаток немає.</div>
                {% endif %}
            </div>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():
    text = ""
    analysis = None

    if request.method == "POST":
        text = request.form.get("text", "").strip()

        if text:
            raw_result = run_core(text, mode="document")

            analysis = {
                "summary": raw_result.get("summary", ""),
                "simplified_text": raw_result.get("simplified_text", ""),
                "risks": raw_result.get("risks", []),
                "missing_elements": raw_result.get("missing_elements", []),
                "questions": raw_result.get("questions", []),
                "notes": raw_result.get("notes", []),
            }

    return render_template_string(
        HTML_TEMPLATE,
        text=text,
        analysis=analysis
    )


@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok", "service": "infacta-core"}


# Для локального запуску
if __name__ == "__main__":
    app.run(debug=True)
