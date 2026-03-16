from flask import Flask, request, render_template_string

try:
    from core.analyzer import analyze
except ImportError:
    import os
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from core.analyzer import analyze

app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<html lang="uk">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Інфакта</title>
    <style>
        :root {
            --bg: #f7f8fb;
            --card: #ffffff;
            --border: #e5e7eb;
            --text: #1f2937;
            --muted: #6b7280;
            --primary: #4f46e5;
            --primary-hover: #4338ca;
            --secondary-bg: #eef2ff;
            --secondary-border: #c7d2fe;
            --hint-bg: #ecfeff;
            --hint-border: #a5f3fc;
        }

        * {
            box-sizing: border-box;
        }

        html {
            scroll-behavior: smooth;
        }

        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: var(--bg);
            color: var(--text);
        }

        .container {
            max-width: 980px;
            margin: 18px auto 36px auto;
            padding: 12px;
        }

        .card {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 18px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04);
            margin-bottom: 16px;
        }

        .hero {
            padding: 16px 18px;
        }

        h1 {
            margin: 0 0 4px 0;
            font-size: 28px;
            line-height: 1.1;
            color: var(--primary);
        }

        .subtitle {
            margin: 0 0 12px 0;
            color: var(--muted);
            font-size: 15px;
        }

        .modes {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin-bottom: 12px;
        }

        .mode {
            background: var(--secondary-bg);
            color: #3730a3;
            border: 1px solid var(--secondary-border);
            padding: 7px 11px;
            border-radius: 999px;
            font-size: 13px;
            font-weight: 700;
        }

        .focus-box {
            background: #fafafa;
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 12px 14px;
            font-size: 14px;
            line-height: 1.45;
        }

        .focus-box strong {
            display: block;
            margin-bottom: 6px;
        }

        label {
            display: block;
            font-size: 19px;
            font-weight: 700;
            margin-bottom: 8px;
        }

        textarea {
            width: 100%;
            min-height: 170px;
            padding: 14px;
            border-radius: 12px;
            border: 1px solid #d1d5db;
            font-size: 15px;
            line-height: 1.5;
            resize: vertical;
            background: #fff;
        }

        .hint {
            margin-top: 8px;
            color: var(--muted);
            font-size: 13px;
        }

        .action-row {
            margin-top: 14px;
            display: flex;
            align-items: center;
            gap: 12px;
            flex-wrap: wrap;
        }

        button {
            border: none;
            border-radius: 12px;
            padding: 12px 18px;
            font-size: 15px;
            font-weight: 700;
            cursor: pointer;
        }

        .primary {
            background: var(--primary);
            color: white;
        }

        .primary:hover {
            background: var(--primary-hover);
        }

        .secondary {
            background: var(--secondary-bg);
            color: #3730a3;
            border: 1px solid var(--secondary-border);
        }

        .secondary:hover {
            background: #e0e7ff;
        }

        .cta-note {
            color: var(--muted);
            font-size: 13px;
        }

        .result-hint {
            background: var(--hint-bg);
            border: 1px solid var(--hint-border);
            border-radius: 12px;
            padding: 12px 14px;
            margin-bottom: 14px;
            font-size: 15px;
            font-weight: 700;
        }

        h2 {
            margin: 0 0 14px 0;
            font-size: 24px;
        }

        h3 {
            margin: 0 0 8px 0;
            font-size: 18px;
            color: #374151;
        }

        .block {
            margin-bottom: 16px;
        }

        .plain-box {
            background: #f9fafb;
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 14px;
            white-space: pre-wrap;
            line-height: 1.55;
        }

        ul {
            margin: 0;
            padding-left: 20px;
        }

        li {
            margin-bottom: 7px;
            line-height: 1.45;
        }

        .empty {
            color: var(--muted);
            font-style: italic;
        }

        .top-anchor {
            position: relative;
            top: -10px;
        }

        @media (max-width: 768px) {
            .container {
                margin-top: 10px;
                padding: 10px;
            }

            .card {
                padding: 14px;
            }

            h1 {
                font-size: 24px;
            }

            textarea {
                min-height: 140px;
            }

            .action-row {
                align-items: stretch;
            }

            button {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="card hero">
            <h1>Інфакта</h1>
            <p class="subtitle">Аналіз документів і договорів на основі структури</p>

            <div class="modes">
                <div class="mode">Check Document</div>
                <div class="mode">Check Contract</div>
                <div class="mode">Check Information</div>
            </div>

            <div class="focus-box">
                <strong>Поточний фокус Core 0.11:</strong>
                1. Сканування структури<br>
                2. Виявлення відсутніх елементів<br>
                3. Пошук базових ризиків<br>
                4. Генерація уточнюючих питань<br>
                5. Спрощене пояснення тексту
            </div>
        </div>

        <div class="card" id="analyze-form">
            <form method="post" id="analysisForm" onsubmit="beforeAnalyze()">
                <label for="text">Вставте текст документа або договору</label>
                <textarea id="text" name="text" placeholder="Вставте тут текст для аналізу...">{{ text }}</textarea>

                <div class="hint">
                    На цьому етапі система працює як document/contract-first MVP.
                </div>

                <div class="action-row">
                    <button type="submit" class="primary">Аналізувати</button>
                    <button type="button" class="secondary" onclick="resetAnalysis()">Новий аналіз</button>
                    <div class="cta-note">Головна дія доступна одразу на першому екрані.</div>
                </div>
            </form>
        </div>

        {% if analysis %}
        <div class="top-anchor" id="result-anchor"></div>

        <div class="result-hint">
            Результат готовий ↓ Прокрутіть нижче або перегляньте блок результату нижче на цій сторінці.
        </div>

        <div class="card" id="result-block">
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

    <script>
        function resetAnalysis() {
            const textArea = document.getElementById("text");
            if (textArea) {
                textArea.value = "";
            }

            const resultBlock = document.getElementById("result-block");
            if (resultBlock) {
                resultBlock.remove();
            }

            const resultHint = document.querySelector(".result-hint");
            if (resultHint) {
                resultHint.remove();
            }

            const resultAnchor = document.getElementById("result-anchor");
            if (resultAnchor) {
                resultAnchor.remove();
            }

            window.scrollTo({ top: 0, behavior: "smooth" });
        }

        function beforeAnalyze() {
            const resultBlock = document.getElementById("result-block");
            if (resultBlock) {
                resultBlock.remove();
            }

            const resultHint = document.querySelector(".result-hint");
            if (resultHint) {
                resultHint.remove();
            }

            const resultAnchor = document.getElementById("result-anchor");
            if (resultAnchor) {
                resultAnchor.remove();
            }
        }

        window.addEventListener("load", function () {
            const resultBlock = document.getElementById("result-anchor");
            if (resultBlock) {
                resultBlock.scrollIntoView({ behavior: "smooth", block: "start" });
            }
        });
    </script>
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
            analysis = analyze(text, mode="document")

    return render_template_string(
        HTML_TEMPLATE,
        text=text,
        analysis=analysis
    )


@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok", "service": "infacta-core"}


if __name__ == "__main__":
    app.run(debug=True)
