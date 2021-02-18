import ssl
import json

import websocket
import bitstamp.client

import credenciais


def client():
    return bitstamp.client.Trading(username=credenciais.USERNAME,
                                   key=credenciais.KEY,
                                   secret=credenciais.SECRET)


def buy(amount):
    trading_client = client()
    trading_client.buy_market_order(amount)


def sell(amount):
    trading_client = client()
    trading_client.sell_market_order(amount)


def on_open(ws):
    print("Opening connection.")
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
    print("Error.")


def on_close(ws):
    print("Connection Closed.")


def on_message(ws, message):
    mensagem = json.loads(message)
    price = mensagem['data']['price']
    print(price)

    if price > 40000.0:
        sell()
    elif price < 38800.0:
        buy()
    else:
        print("Waiting for the right moment.")


if __name__ == "__main__":
    ws = websocket.WebSocketApp("wss://ws.bitstamp.net.",
                                on_open=on_open,
                                on_close=on_close,
                                on_message=on_message,
                                on_error=on_error)
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
