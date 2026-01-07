from http.server import BaseHTTPRequestHandler
import json
import requests
from urllib.parse import urlparse, parse_qs

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Parsear parámetros GET
            query = parse_qs(urlparse(self.path).query)
            symbol = query.get("symbol", ["ETHUSDT"])[0].upper()
            interval = query.get("interval", ["1h"])[0]
            limit = int(query.get("limit", ["500"])[0])

            # Construir URL Binance
            url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
            r = requests.get(url, timeout=10)

            # Validar respuesta
            if r.status_code != 200:
                raise ValueError(f"Binance API error: {r.text}")

            data = r.json()
            if not isinstance(data, list) or not all(isinstance(c, list) for c in data):
                raise ValueError(f"Unexpected Binance response: {data}")

            candles = [
                {
                    "open_time": c[0],
                    "open": float(c[1]),
                    "high": float(c[2]),
                    "low": float(c[3]),
                    "close": float(c[4]),
                    "volume": float(c[5]),
                    "close_time": c[6],
                }
                for c in data
            ]

            response = json.dumps(candles)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(response.encode())

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            error = {"error": str(e)}
            self.wfile.write(json.dumps(error).encode())

