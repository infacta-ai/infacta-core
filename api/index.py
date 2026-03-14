from flask import Flask, request, jsonify

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


HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Infacta</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f5f7fb;
            color: #1f2937;
            margin: 0;
            padding: 40px 20px;
        }
        .container {
            max-width: 950px;
            margin: 0 auto;
        }
        h1 {
            margin-bottom: 6px;
            font-size: 42px;
        }
        .subtitle {
            color: #6b7280;
            margin-bottom: 24px;
        }
        .card {
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.04);
        }
        .visible-box {
            background: #f9fafb;
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 20px;
            color: #374151;
        }
        textarea {
            width: 100%;
            min-height: 180px;
            border-radius: 12px;
            border: 1px solid #d1d5db;
            padding: 14px;
            font-size: 16px;
            box-sizing: border-box;
            resize: vertical;
        }
        button {
            margin-top: 14px;
            background: #2563eb;
            color: white;
            border: none;
            border-radius: 10px;
            padding: 12px 20px;
            font-size: 16px;
            cursor: pointer;
        }
        button:hover {
            background: #1d4ed8;
        }
        .grid {
            display: grid;
            gap: 16px;
        }
        .badge {
            display: inline-block;
            padding: 6px 12px;
            border-radius: 999px;
            color: white;
            font-weight: bold;
            font-size: 14px;
        }
        .high { background: #16a34a; }
        .medium { background: #d97706; }
        .low { background: #dc2626; }
        ul {
            margin: 8px 0 0 20px;
        }
        .muted {
            color: #6b7280;
        }
        .mono {
            font-family: Consolas, monospace;
        }
        .result-box {
            margin-top: 20px;
        }
        .small-title {
            margin-bottom: 10px;
            font-size: 20px;
        }
        .line {
            margin-bottom: 8px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Infacta</h1>
        <div class="subtitle">Information Analysis Platform</div>

        <div class="visible-box">
            <strong>Visible analysis:</strong><br>
            1. Checking structure<br>
            2. Detecting numbers and time references<br>
            3. Estimating coverage<br>
            4. Building Map of Unknowns<br>
            5. Estimating reliability and maturity
        </div>

        <div class="card">
            <div class="small-title">Check Information</div>
            <div class="muted">Paste a short claim, paragraph, or news fragment.</div>

            <textarea id="inputText">New drone system destroyed 20 tanks yesterday.</textarea>
            <br>
            <button onclick="runAnalysis()">Analyze</button>

            <div id="result" class="result-box"></div>
        </div>
    </div>

    <script>
        async function runAnalysis() {
            const text = document.getElementById("inputText").value;

            const response = await fetch("/analyze", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ text })
            });

            const data = await response.json();

            const reliabilityClass =
                data.reliability === "HIGH" ? "high" :
                data.reliability === "MEDIUM" ? "medium" : "low";

            document.getElementById("result").innerHTML = `
                <div class="card">
                    <div class="small-title">Analysis Result</div>
                    <div class="line"><strong>Reliability:</strong> <span class="badge ${reliabilityClass}">${data.reliability}</span></div>
                    <div class="line"><strong>Analysis Maturity:</strong> ${data.maturity}</div>
                    <div class="line"><strong>Structure Coverage:</strong> ${data.coverage}%</div>
                    <div class="line"><strong>Text length:</strong> ${data.text_length}</div>
                </div>

                <div class="card">
                    <div class="small-title">Detected Elements</div>
                    <div class="line"><strong>Numbers:</strong> ${data.numbers.length ? data.numbers.join(", ") : "None"}</div>
                    <div class="line"><strong>Time references:</strong> ${data.time_words.length ? data.time_words.join(", ") : "None"}</div>
                    <div class="line"><strong>Action verbs:</strong> ${data.action_verbs.length ? data.action_verbs.join(", ") : "None"}</div>
                </div>

                <div class="card">
                    <div class="small-title">Structure Check</div>
                    <ul>
                        <li>Source: ${data.structure.source}</li>
                        <li>Date: ${data.structure.date}</li>
                        <li>Context: ${data.structure.context}</li>
                        <li>Evidence: ${data.structure.evidence}</li>
                        <li>Claim: ${data.structure.claim}</li>
                    </ul>
                </div>

                <div class="card">
                    <div class="small-title">Map of Unknowns</div>
                    <div class="line"><strong>Missing:</strong> ${data.missing.length ? data.missing.join(", ") : "None"}</div>
                    <div class="line"><strong>Critical Unknowns:</strong> ${data.critical_unknowns.length ? data.critical_unknowns.join(", ") : "None"}</div>
                </div>

                <div class="card">
                    <div class="small-title">Reasons</div>
                    <ul>
                        ${data.reasons.length ? data.reasons.map(item => `<li>${item}</li>`).join("") : "<li>No major gaps detected</li>"}
                    </ul>
                </div>
            `;
        }
    </script>
</body>
</html>
"""


@app.route("/", methods=["GET"])
def home():
    return HTML_PAGE


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "No text provided"}), 400

    result = analyze_text(text)
    return jsonify(result)


# Vercel looks for `app`
