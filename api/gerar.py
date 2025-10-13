import json
import os
from typing import Any

import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

_GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
_GEMINI_URL_TEMPLATE = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "{model}:generateContent?key={api_key}"
)


def _error_response(status_code: int, message: str):
    response = jsonify({"error": message})
    response.status_code = status_code
    return response


def _extract_text(gemini_payload: dict) -> str:
    try:
        candidates = gemini_payload["candidates"]
        content_parts = candidates[0]["content"]["parts"]
        text = content_parts[0]["text"]
    except (KeyError, IndexError, TypeError):  # pragma: no cover - defensive
        raise ValueError("Resposta inesperada da API Gemini.")

    if not text:
        raise ValueError("Resposta vazia da API Gemini.")

    return text


def _extract_json_fragment(text_response: str) -> Any:
    decoder = json.JSONDecoder()
    stripped = text_response.strip()

    for index, char in enumerate(stripped):
        if char in "[{":
            try:
                fragment, _ = decoder.raw_decode(stripped[index:])
                return fragment
            except json.JSONDecodeError:
                continue

    raise ValueError("Resposta não contém JSON válido.")


@app.route("/api/gerar", methods=["POST"])
def gerar():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return _error_response(500, "Chave da API do Gemini não configurada no servidor.")

    data = request.get_json(silent=True)
    if not data:
        return _error_response(400, "Nenhum dado recebido.")

    prompt = (data.get("prompt") or "").strip()
    is_json_mode = bool(data.get("isJsonMode"))

    if not prompt:
        return _error_response(400, "Prompt não fornecido.")

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": 8192},
    }

    url = _GEMINI_URL_TEMPLATE.format(model=_GEMINI_MODEL, api_key=api_key)

    try:
        response = requests.post(url, json=payload, timeout=(5, 30))
    except requests.RequestException as exc:
        return _error_response(502, f"Erro de conexão com API Gemini: {exc}")

    if not response.ok:
        try:
            error_payload = response.json()
            error_message = error_payload.get("error", {}).get("message")
        except ValueError:
            error_message = response.text or response.reason

        return _error_response(
            response.status_code,
            f"Erro da API Gemini: {error_message or response.status_code}",
        )

    try:
        gemini_response = response.json()
    except ValueError:
        return _error_response(502, "Resposta inválida da API Gemini.")

    try:
        text_part = _extract_text(gemini_response)
    except ValueError as exc:
        return _error_response(502, str(exc))

    if is_json_mode:
        try:
            parsed_content = _extract_json_fragment(text_part)
        except ValueError as exc:
            return _error_response(502, str(exc))

        return jsonify(parsed_content)

    return jsonify({"text": text_part})


@app.route("/api/gerar", methods=["OPTIONS"])
def gerar_options():
    response = jsonify({})
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
