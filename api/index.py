from flask import Flask, request, jsonify
import traceback

from core.analyzer import analyze_text

app = Flask(__name__)


def _extract_input_data():
    """
    Safe input extractor:
    1) tries JSON body
    2) tries form fields
    3) tries query params
    """
    data = request.get_json(silent=True)
    if isinstance(data, dict):
        return data

    if request.form:
        return request.form.to_dict()

    if request.args:
        return request.args.to_dict()

    return {}


def _run_analysis():
    data = _extract_input_data()

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


@app.route("/", methods=["GET"])
def root_get():
    return jsonify({
        "ok": True,
        "message": "Infacta API працює"
    })


@app.route("/", methods=["POST"])
def root_post():
    try:
        return _run_analysis()
    except Exception as e:
        return jsonify({
            "ok": False,
            "error": "Internal server error",
            "details": str(e),
            "trace": traceback.format_exc()
        }), 500


@app.route("/api", methods=["GET"])
def api_get():
    return jsonify({
        "ok": True,
        "message": "Infacta API endpoint ready"
    })


@app.route("/api", methods=["POST"])
def api_post():
    try:
        return _run_analysis()
    except Exception as e:
        return jsonify({
            "ok": False,
            "error": "Internal server error",
            "details": str(e),
            "trace": traceback.format_exc()
        }), 500


@app.route("/api/analyze", methods=["GET"])
def api_analyze_get():
    return jsonify({
        "ok": True,
        "message": "Use POST to analyze text, or send query params for testing."
    })


@app.route("/api/analyze", methods=["POST"])
def api_analyze_post():
    try:
        return _run_analysis()
    except Exception as e:
        return jsonify({
            "ok": False,
            "error": "Internal server error",
            "details": str(e),
            "trace": traceback.format_exc()
        }), 500


@app.route("/analyze", methods=["GET"])
def analyze_get():
    return jsonify({
        "ok": True,
        "message": "Analyze endpoint is ready."
    })


@app.route("/analyze", methods=["POST"])
def analyze_post():
    try:
        return _run_analysis()
    except Exception as e:
        return jsonify({
            "ok": False,
            "error": "Internal server error",
            "details": str(e),
            "trace": traceback.format_exc()
        }), 500


@app.route("/", methods=["OPTIONS"])
@app.route("/api", methods=["OPTIONS"])
@app.route("/api/analyze", methods=["OPTIONS"])
@app.route("/analyze", methods=["OPTIONS"])
def options_handler():
    response = jsonify({"ok": True})
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response
