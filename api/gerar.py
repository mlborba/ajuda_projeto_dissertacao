from http.server import BaseHTTPRequestHandler
import json
import os
import urllib.request
import urllib.parse
import urllib.error

class handler(BaseHTTPRequestHandler ):
    def do_POST(self):
        try:
            # Headers CORS
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()

            # Verificar chave da API
            api_key = os.environ.get("GEMINI_API_KEY")
            if not api_key:
                response = {"error": "Chave da API do Gemini não configurada no servidor."}
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                return

            # Ler dados da requisição
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                response = {"error": "Nenhum dado recebido."}
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                return
                
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            prompt = data.get("prompt", "").strip()
            is_json_mode = data.get("isJsonMode", False)

            if not prompt:
                response = {"error": "Prompt não fornecido."}
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                return

            # Preparar dados para API do Gemini
            gemini_payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"maxOutputTokens": 8192},
            }
            
            # Fazer requisição para API do Gemini
            gemini_api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
            
            req = urllib.request.Request(
                gemini_api_url,
                data=json.dumps(gemini_payload ).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            
            try:
                with urllib.request.urlopen(req, timeout=30) as response_obj:
                    if response_obj.status != 200:
                        response = {"error": f"Erro da API Gemini: {response_obj.status}"}
                        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                        return
                        
                    gemini_response = json.loads(response_obj.read().decode('utf-8'))
            except urllib.error.HTTPError as e:
                response = {"error": f"Erro HTTP da API Gemini: {e.code}"}
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                return
            except urllib.error.URLError as e:
                response = {"error": f"Erro de conexão com API Gemini: {str(e)}"}
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                return
            
            # Processar resposta
            candidates = gemini_response.get("candidates", [])
            if not candidates:
                response = {"error": "Nenhuma resposta da API Gemini"}
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                return
                
            candidate = candidates[0]
            content = candidate.get("content", {})
            parts = content.get("parts", [])
            
            if not parts:
                response = {"error": "Resposta vazia da API Gemini"}
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                return
                
            text_part = parts[0].get("text", "")

            if not text_part:
                response = {"error": "Texto vazio na resposta da API Gemini"}
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                return

            # Retornar resultado
            if is_json_mode:
                json_start_index = text_part.find('{')
                json_end_index = text_part.rfind('}')
                
                if json_start_index == -1 or json_end_index == -1:
                    response = {"error": "Resposta não contém JSON válido"}
                    self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                    return

                json_string = text_part[json_start_index : json_end_index + 1]
                try:
                    result = json.loads(json_string)
                    self.wfile.write(json.dumps(result, ensure_ascii=False).encode('utf-8'))
                except json.JSONDecodeError:
                    response = {"error": "JSON inválido na resposta da IA"}
                    self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            else:
                response = {"text": text_part}
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))

        except Exception as e:
            # Em caso de erro, sempre retornar JSON válido
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {"error": f"Erro interno: {str(e)}"}
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def log_message(self, format, *args):
        # Suprimir logs para evitar problemas no Vercel
        pass

    

  
