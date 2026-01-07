import json
import requests

def handler(request):
    # Parámetros básicos
    symbol = "ETHUSDT"
    interval = "1h"
    limit = 1000  # puedes ajustar a 500, 1000, etc.

    # Endpoint oficial de Binance
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        # Transformamos el formato
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

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(candles)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
