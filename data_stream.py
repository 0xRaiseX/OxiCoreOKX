import requests
import json
import time
import websockets
import asyncio
from okx_function import load_tickers, generate_signature

data = {}
tickers = load_tickers()

def connect_websocket_symbols():
    global tickers
    iteration = 0
    connect = 180

    args = []
    subscription_data = {
                    "op": "subscribe",
                    "args": args
                }
    
    for i in tickers:
        if iteration != connect:
            args.append({'channel': 'bbo-tbt', 'instId': i})
            tickers.remove(i)
            iteration += 1
    
    return subscription_data



async def websocket_connect():
    uri = "wss://ws.okx.com:8443/ws/v5/public"
    async with websockets.connect(uri) as websocket:
        subscription_data = connect_websocket_symbols()

        while True:
            try:
                await websocket.send(json.dumps(subscription_data))
           
                while True:
                    
                    responce = await websocket.recv()
                    data_json = json.loads(responce)
                
                    try:
                        data[data_json['arg']['instId']] = {
                            'bid': data_json['data'][0]['bids'][0][0], 
                            'ask': data_json['data'][0]['asks'][0][0],
                            'askVolume': data_json['data'][0]['asks'][0][1], 
                            'bidVolume': data_json['data'][0]['bids'][0][1]
                        }
                            
                    except (KeyError, IndexError):
                        print(data_json)
                        continue
            
            except (websockets.ConnectionClosed, websockets.exceptions.InvalidStatusCode, TimeoutError) as e:
                await asyncio.sleep(5)
                print('Websocket 1. Conection closed. Reconnecting...', e)
                continue

    
async def websocket_connect2():
    await asyncio.sleep(5)
    uri = "wss://ws.okx.com:8443/ws/v5/public"
    async with websockets.connect(uri) as websocket:
        subscription_data = connect_websocket_symbols()

        while True:
            try:
                await websocket.send(json.dumps(subscription_data))
           
                while True:
                    
                    responce = await websocket.recv()
                    data_json = json.loads(responce)
                
                    try:
                        data[data_json['arg']['instId']] = {
                            'bid': data_json['data'][0]['bids'][0][0], 
                            'ask': data_json['data'][0]['asks'][0][0],
                            'askVolume': data_json['data'][0]['asks'][0][1], 
                            'bidVolume': data_json['data'][0]['bids'][0][1]
                        }
                            
                    except (KeyError, IndexError):
                        print(data_json)
                        continue
            
            except (websockets.ConnectionClosed, websockets.exceptions.InvalidStatusCode, TimeoutError) as e:
                await asyncio.sleep(5)
                print('Websocket 2. Conection closed. Reconnecting...', e)
                continue

async def websocket_connect3():
    await asyncio.sleep(10)
    uri = "wss://ws.okx.com:8443/ws/v5/public"
    async with websockets.connect(uri) as websocket:
        args = []
        for i in tickers:
            args.append({'channel': 'bbo-tbt', 'instId': i})
        
        subscription_data = {
                    "op": "subscribe",
                    "args": args
                }

        while True:
            try:
                await websocket.send(json.dumps(subscription_data))
           
                while True:
                    
                    responce = await websocket.recv()
                    data_json = json.loads(responce)
                
                    try:
                        data[data_json['arg']['instId']] = {
                            'bid': data_json['data'][0]['bids'][0][0], 
                            'ask': data_json['data'][0]['asks'][0][0],
                            'askVolume': data_json['data'][0]['asks'][0][1], 
                            'bidVolume': data_json['data'][0]['bids'][0][1]
                        }
                            
                    except (KeyError, IndexError):
                        print(data_json)
                        continue
            
            except (websockets.ConnectionClosed, websockets.exceptions.InvalidStatusCode, TimeoutError) as e:
                await asyncio.sleep(5)
                print('Websocket 3. Conection closed. Reconnecting...', e)
                continue


async def websocket_connect_data():
    # await asyncio.sleep(10)
    uri = "wss://ws.okx.com:8443/ws/v5/private"
    async with websockets.connect(uri) as websocket:

        subscription_data = {
            "op": "subscribe",
            "args": [
                {
                    "channel": "orders",
                    "sprdId": "BTC-USDT"
                }
            ]
        }
        secret_key = 'B8C400F21BA6999F02A7CFDF9F80C7F3'
        login = {
            "op": "login",
            "args": [
                {
                    "apiKey": "43a9b1aa-b840-45c5-86e5-a221988a922d",
                    "passphrase": "CODDICODDICODi1!",
                    "timestamp": str(int(time.time())),
                    "sign": generate_signature(secret_key, time.time(), 'GET', '/users/self/verify')
                }
            ]
        }

        while True:
            try:
                await websocket.send(json.dumps(login))
                await websocket.send(json.dumps(subscription_data))
              

                while True:
                    responce = await websocket.recv()
                    data_json = json.loads(responce)
                
                    try:
                        data[data_json['arg']['instId']] = {
                            'bid': data_json['data'][0]['bids'][0][0], 
                            'ask': data_json['data'][0]['asks'][0][0],
                            'askVolume': data_json['data'][0]['asks'][0][1], 
                            'bidVolume': data_json['data'][0]['bids'][0][1]
                        }
                        
                    except (KeyError, IndexError):
                        print(data_json)
                        continue
            
            except (websockets.ConnectionClosed, websockets.exceptions.InvalidStatusCode, TimeoutError) as e:
                await asyncio.sleep(5)
                print('Websocket Data. Conection closed. Reconnecting...', e)
                continue



async def add_queue(queue):
    await asyncio.sleep(5)
    while True:
        try:
            queue.put(data.copy(), block=False)
            await asyncio.sleep(0.001)
        except Exception:
            continue
    

async def main(queue):
    await asyncio.gather(websocket_connect(), websocket_connect2(), websocket_connect3(), add_queue(queue))

def start_process_data(queue):
    asyncio.run(main(queue))




# async def authenticate_and_subscribe(api_key, secret_key, passphrase):
#     # Устанавливаем URL для WebSocket и URL для REST API биржи OKX
#     ws_url = "wss://ws.okx.com:8443/ws/v5/private"
#     rest_api_url = "https://www.okx.com/api/v5/"

#     # Создаем WebSocket соединение
#     async with websockets.connect(ws_url) as websocket:
#         # Определяем параметры для аутентификации
#         timestamp = str(int(time.time()))
#         method = "GET"
#         request_path = "/users/self/verify"
#         string_to_sign = f"{timestamp}{method}{request_path}"

#         # Создаем подпись для аутентификации
#         signature = generate_signature(secret_key, string_to_sign)

#         # Формируем HTTP запрос для аутентификации
#         headers = {
#             "OK-ACCESS-KEY": api_key,
#             "OK-ACCESS-SIGN": signature,
#             "OK-ACCESS-TIMESTAMP": timestamp,
#             "OK-ACCESS-PASSPHRASE": passphrase
#         }
#         response = requests.get(rest_api_url + request_path, headers=headers)
#         print(response.text)
#         if response.status_code == 200:
#             print("Аутентификация прошла успешно")
#             # Подписываемся на канал данных о выставленных ордерах
#             await websocket.send(json.dumps({"op": "subscribe", "args": ["spot/order:BTC-USDT"]}))
#             async for message in websocket:
#                 print(f"Получено сообщение: {message}")
#         else:
#             print("Ошибка при аутентификации")

# # Функция для генерации подписи
# def generate_signature(secret_key, data):
#     secret_key_bytes = bytes(secret_key, 'utf-8')
#     signature = base64.b64encode(hmac.new(secret_key_bytes, data.encode('utf-8'), hashlib.sha256).digest()).decode('utf-8')
#     return signature

# api_key = "43a9b1aa-b840-45c5-86e5-a221988a922d"
# secret_key = "B8C400F21BA6999F02A7CFDF9F80C7F3"
# passphrase = "CODDICODDICODi1!"

# asyncio.get_event_loop().run_until_complete(authenticate_and_subscribe(api_key, secret_key, passphrase))
