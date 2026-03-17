from flask import Flask, request, jsonify
import traceback

from core.analyzer import analyze_text

app = Flask(__name__)


@app.route("/", methods=["GET"])
def root():
    return jsonify({
        "ok": True,
        "message": "Infacta API працює"
    })


@app.route("/api", methods=["GET"])
def api_root():
    return jsonify({
        "ok": True,
        "message": "Infacta API endpoint ready"
    })


@app.route("/api/analyze", methods=["POST"])
def api_analyze():
    try:
        data = request.get_json(silent=True) or {}

        text = data.get("text", "")
        mode = data.get("mode", "contract_analysis")
        language = data.get("language", "uk")

        result = analyze_text(
            text=text,
            mode=mode,
            language=language,
        )

        return jsonify({
            "ok": True,
            "result": result
        })

    except Exception as e:
        return jsonify({
            "ok": False,
            "error": "Internal server error",
            "details": str(e),
            "trace": traceback.format_exc()
        }), 500


@app.route("/api/analyze", methods=["OPTIONS"])
def api_analyze_options():
    response = jsonify({"ok": True})
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response
