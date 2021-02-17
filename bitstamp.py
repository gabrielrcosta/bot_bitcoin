import ssl
import json

import websocket


def comprar():
    pass


def vender():
    pass


def on_open(ws):
    print("Abriu a conexão")
    json_subscribe = """
{
    "event": "bts:subscribe",
    "data": {
        "channel": "live_trades_btceur"
    }
}
"""
    ws.send(json_subscribe)


def on_error(ws, error):
    print("Error")


def on_close(ws):
    print("Fechou a conexão")


def on_message(ws, message):
    mensagem = json.loads(message)
    price = mensagem['data']['price']
    print(price)

    if price > 40000.0:
        vender()
    elif price < 38800.0:
        comprar()
    else:
        print("Aguardar.")


if __name__ == "__main__":
    ws = websocket.WebSocketApp("wss://ws.bitstamp.net.",
                                on_open=on_open,
                                on_close=on_close,
                                on_message=on_message,
                                on_error=on_error)
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
