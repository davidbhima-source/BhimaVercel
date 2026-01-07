from http.server import BaseHTTPRequestHandler
import json
import requests

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            # Parámetros
            symbol = "ETHUSDT"
            interval = "1h"
            limit = 500

            url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
            r = requests.get(url, timeout=10)
            data = r.json()

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
