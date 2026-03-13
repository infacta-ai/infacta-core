from flask import Flask, request
from core.analyzer import analyze_document

app = Flask(__name__)


def detect_risk(result):
    score = 0

    if not result["dates"]:
        score += 1

    if not result["numbers"]:
        score += 1

    if not result["unit_detected"]:
        score += 1

    if score == 0:
        return "LOW", "#d4edda", "#155724"
    elif score == 1:
        return "MEDIUM", "#fff3cd", "#856404"
    else:
        return "HIGH", "#f8d7da", "#721c24"


@app.route("/")
def home():
    return """
    <html>
    <head>
        <title>Infacta</title>
    </head>
    <body style="font-family: Arial, sans-serif; max-width: 900px; margin: 40px auto; padding: 20px;">
        <h1 style="margin-bottom: 8px;">Infacta</h1>
        <p style="color: #555; margin-top: 0;">Structure-based information verification</p>

        <div style="background: #f5f5f5; padding: 14px; border-radius: 10px; margin-bottom: 20px;">
            <b>Visible analysis:</b><br>
            1. Checking structure<br>
            2. Detecting dates<br>
            3. Detecting numbers<br>
            4. Detecting unit keywords<br>
            5. Building result
        </div>

        <form action="/analyze" method="post">
            <textarea name="text" rows="14" style="width: 100%; padding: 12px; border-radius: 10px; border: 1px solid #ccc;"></textarea>
            <br><br>
            <button type="submit" style="padding: 10px 20px; border: none; border-radius: 8px; background: black; color: white; cursor: pointer;">
                Analyze
            </button>
        </form>
    </body>
    </html>
    """


@app.route("/analyze", methods=["POST"])
def analyze():
    text = request.form["text"]
    result = analyze_document(text)

    risk_label, bg_color, text_color = detect_risk(result)

    dates = "<br>".join(result["dates"]) if result["dates"] else "Not found"
    numbers = "<br>".join(result["numbers"]) if result["numbers"] else "Not found"
    unit = "Yes" if result["unit_detected"] else "No"

    unknowns = []
    if not result["dates"]:
        unknowns.append("No dates detected")
    if not result["numbers"]:
        unknowns.append("No document numbers detected")
    if not result["unit_detected"]:
        unknowns.append("No unit keywords detected")

    unknowns_html = "<br>".join(unknowns) if unknowns else "No major unknowns detected"

    return f"""
    <html>
    <head>
        <title>Infacta analysis result</title>
    </head>
    <body style="font-family: Arial, sans-serif; max-width: 900px; margin: 40px auto; padding: 20px;">
        <h1 style="margin-bottom: 8px;">Infacta analysis result</h1>
        <p style="color: #555; margin-top: 0;">Document verification module</p>

        <div style="background:{bg_color}; color:{text_color}; padding:16px; border-radius:10px; margin-bottom:20px;">
            <b>Risk level: {risk_label}</b>
        </div>

        <div style="background:#f8f9fa; padding:16px; border-radius:10px; margin-bottom:20px;">
            <b>Visible analysis completed:</b><br>
            ✔ Structure checked<br>
            ✔ Dates checked<br>
            ✔ Numbers checked<br>
            ✔ Unit keywords checked
        </div>

        <div style="background:#ffffff; border:1px solid #ddd; padding:16px; border-radius:10px; margin-bottom:20px;">
            <p><b>Text length:</b> {result["length"]}</p>
            <p><b>Dates found:</b><br>{dates}</p>
            <p><b>Numbers found:</b><br>{numbers}</p>
            <p><b>Unit keywords detected:</b> {unit}</p>
        </div>

        <div style="background:#eef2ff; padding:16px; border-radius:10px; margin-bottom:20px;">
            <b>Map of Unknowns:</b><br>
            {unknowns_html}
        </div>

        <a href="/" style="text-decoration:none; color:black;">← Back</a>
    </body>
    </html>
    """
