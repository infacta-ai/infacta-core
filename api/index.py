from flask import Flask, request
from core.analyzer import analyze_document

app = Flask(__name__)


@app.route("/")
def home():
    return """
    <h1>Infacta</h1>
    <p>Structure-based information verification</p>

    <form action="/analyze" method="post">
        <textarea name="text" rows="12" cols="90"></textarea><br><br>
        <button type="submit">Analyze</button>
    </form>
    """


@app.route("/analyze", methods=["POST"])
def analyze():

    text = request.form["text"]

    result = analyze_document(text)

    dates = "<br>".join(result["dates"]) if result["dates"] else "Not found"
    numbers = "<br>".join(result["numbers"]) if result["numbers"] else "Not found"
    unit = "Yes" if result["unit_detected"] else "No"

    return f"""
    <h1>Infacta analysis result</h1>

    <p><b>Text length:</b> {result["length"]}</p>

    <p><b>Dates found:</b><br>{dates}</p>

    <p><b>Numbers found:</b><br>{numbers}</p>

    <p><b>Unit keywords detected:</b> {unit}</p>

    <br>
    <a href="/">Back</a>
    """
