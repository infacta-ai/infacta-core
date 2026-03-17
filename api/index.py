import json
import traceback

from core.analyzer import analyze_text


def _json_response(status_code, payload):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json; charset=utf-8",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        },
        "body": json.dumps(payload, ensure_ascii=False),
    }


def _extract_body(event):
    if not event:
        return {}

    body = event.get("body")

    if body is None:
        return {}

    if isinstance(body, dict):
        return body

    if isinstance(body, str):
        body = body.strip()
        if not body:
            return {}
        try:
            return json.loads(body)
        except Exception:
            return {"text": body}

    return {}


def handler(event, context):
    try:
        method = (event or {}).get("httpMethod", "GET")

        if method == "OPTIONS":
            return _json_response(200, {"ok": True})

        if method == "GET":
            return _json_response(
                200,
                {
                    "ok": True,
                    "message": "Infacta API працює",
                    "mode": "contract_analysis",
                },
            )

        if method != "POST":
            return _json_response(
                405,
                {
                    "ok": False,
                    "error": "Method not allowed. Use POST.",
                },
            )

        data = _extract_body(event)

        text = data.get("text", "")
        mode = data.get("mode", "contract_analysis")
        language = data.get("language", "uk")

        result = analyze_text(
            text=text,
            mode=mode,
            language=language,
        )

        return _json_response(
            200,
            {
                "ok": True,
                "result": result,
            },
        )

    except Exception as e:
        return _json_response(
            500,
            {
                "ok": False,
                "error": "Internal server error",
                "details": str(e),
                "trace": traceback.format_exc(),
            },
        )
