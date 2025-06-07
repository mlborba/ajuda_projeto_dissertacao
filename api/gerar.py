import os
import json
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

# Inicializa a aplicação Flask
app = Flask(__name__)
CORS(app)  # Permite requisições de qualquer origem

@app.route('/api/gerar', methods=['POST'])
def handler():
    """
    Esta função é o nosso "servidor". Ela recebe os pedidos do frontend,
    contacta a API do Gemini e devolve a resposta.
    """
    # A Vercel executará esta função para todos os pedidos para /api/gerar.

    # Lê a chave da API da variável de ambiente configurada na Vercel.
    # Este é o segredo que nunca é exposto ao público.
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        return jsonify({"error": "Chave da API do Gemini não configurada no servidor."}), 500

    try:
        # Extrai os dados (prompt, isJsonMode) enviados pelo frontend.
        data = request.get_json()
        prompt = data.get("prompt")
        is_json_mode = data.get("isJsonMode", False)

        if not prompt:
            return jsonify({"error": "Prompt não fornecido."}), 400

        # Prepara o corpo do pedido para a API do Gemini.
        gemini_payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"maxOutputTokens": 8192},
        }
        
        gemini_api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

        # Faz a chamada para a API do Gemini a partir do servidor.
        gemini_response = requests.post(gemini_api_url, json=gemini_payload)
        
        # Lança um erro se a resposta não for bem-sucedida.
        gemini_response.raise_for_status()

        gemini_data = gemini_response.json()
        
        candidate = gemini_data.get("candidates", [{}])[0]
        text_part = candidate.get("content", {}).get("parts", [{}])[0].get("text")

        if not text_part:
            raise ValueError("A resposta da API do Gemini está vazia ou em formato inesperado.")

        # Se o frontend pediu uma resposta em JSON, processamo-la aqui.
        if is_json_mode:
            json_start_index = text_part.find('{')
            json_end_index = text_part.rfind('}')
            
            if json_start_index == -1 or json_end_index == -1:
                raise ValueError("Resposta da IA não continha um JSON válido.")

            json_string = text_part[json_start_index : json_end_index + 1]
            final_response = jsonify(json.loads(json_string))
        else:
            # Se foi pedido texto, devolvemos um objeto com a propriedade 'text'.
            final_response = jsonify({"text": text_part})
        
        # Envia a resposta bem-sucedida de volta para o frontend.
        return final_response

    except requests.exceptions.HTTPError as http_err:
        # Erro específico da chamada HTTP para a API Gemini
        print(f"HTTP error occurred: {http_err}")
        return jsonify({"error": f"Erro ao comunicar com a API do Gemini: {gemini_response.text}"}), 502
    except Exception as e:
        # Outros erros no nosso servidor.
        print(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 500

# Esta parte não é necessária para a Vercel, mas é útil para testes locais.
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)

