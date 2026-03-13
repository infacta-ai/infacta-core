from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>Infacta</h1>
    <p>Structure-based information verification</p>

    <form action="/analyze" method="post">
        <textarea name="text" rows="10" cols="80"></textarea><br><br>
        <button type="submit">Analyze</button>
    </form>
    """

@app.route("/analyze", methods=["POST"])
def analyze():
    text = request.form["text"]

    result = f"""
    <h2>Analysis result</h2>
    <p>Text length: {len(text)} characters</p>

    <a href="/">Back</a>
    """

    return result
