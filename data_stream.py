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
        secret_key = ''
        login = {
            "op": "login",
            "args": [
                {
                    "apiKey": "",
                    "passphrase": "",
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
