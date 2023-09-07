### STREAM ПАРА 1 /USDT

import requests
import time
import json
from create_order import send_order

def get_symbols_websocket_connect():
    params = {'instType': 'SPOT'}
    res = requests.get('https://www.okx.com/api/v5/public/instruments', params=params)
    
    symbols = json.loads(res.text)
 
    symbols_list = []
    for symbol in symbols['data']:
        for symbol2 in symbols['data']:
            if symbol['quoteCcy'] == 'USDT':
                if symbol['baseCcy'] == symbol2['baseCcy']:
                    if symbol['quoteCcy'] != symbol2['quoteCcy']:
                        symbols_list.append([symbol['instId'], symbol2['instId']])
    return symbols_list


def settings_connect():
    params = {'instType': 'SPOT'}
    res = requests.get('https://www.okx.com/api/v5/public/instruments', params=params)
    symbols = json.loads(res.text)

    settings = {}
    for i in symbols['data']:
        settings[i['instId']] = {
            'symbol': i['baseCcy'],
            'symbol1': i['quoteCcy'],
        }  
   
    return settings


def symbols_webscoket_exchange(queue):
    symbols = get_symbols_websocket_connect()
    settings = settings_connect()
    print('Stream 1 запущен')
    while True:

        data = queue.get()
        # print(data)
        errors = 0
        iter = 0
        start = time.time()
        for iteration in symbols:

            symbol = iteration[0]
            symbol2 = iteration[1]
            try:
                # print(symbol, symbol2)
                pair2 = settings[symbol2]
                # print(pair2)
                symbol_price = data[symbol]['ask']
                # print(symbol_price)
                symbol2_price = data[symbol2]['bid']
                # print(symbol2_price)

                try:

                    pair3 = pair2['symbol1'] + '-USDT'
                    # print(pair3)
                    pair3_price = data[pair3]['bid']
                    # print(pair3_price)
                    symbol3_price = float(symbol2_price) * float(pair3_price)
                    # print(symbol3_price)

                except KeyError:

                    pair3 = 'USDT-' + pair2['symbol1']
                    pair3_price = data[pair3]['ask']
                    symbol3_price = float(symbol2_price) / float(pair3_price)

                end = 100 - float(symbol_price) / symbol3_price * 100
                # print(end, symbol, symbol2)
                if end > 0.3:
                    # print('Stream 1: ',end, symbol, symbol2)
                    # continue
                    # symbol1 = symbol
                    # symbol2 = symbol2
                    
                    # amount_symbol = 15 / float(symbol_price)
                    # symbol_step_amount = create_binance_FOKorder(symbol1, symbol_price, amount_symbol, 'buy')

                    # if symbol_step_amount == 'CANCEL':
                    #     continue

                    # symbol2_step2_amount = create_binance_FOKorder(symbol2, symbol2_price, symbol_step_amount, 'sell')
                    # if symbol2_step2_amount == 'CANCEL':
                    #     create_binance_market_order(symbol1, symbol_step_amount, 'sell')
                    #     print('Stream 1  Step 2. Стоп по цене')
                    #     continue
                    

                    # symbol3_step3_amount = create_binance_FOKorder(pair3, pair3_price, symbol2_step2_amount, 'sell')

                    # if symbol3_step3_amount == 'CANCEL':
                    #     create_binance_market_order(pair3, symbol2_step2_amount, 'sell')
                    #     print('Stream 1  Step 3. Стоп по цене')
                    #     continue
                    # print('Stream 1  Все оредра выполнены')
                    symbol_amount = 3.20 / float(symbol_price)
                    symbol_amount_pair3 = symbol_amount * float(pair3_price)

                    pair3_side = ''
                    pair3_amount = symbol_amount * float(pair3_price)
                   
                    timestamp = int(time.time() * 1000)

                    new_data_orders = [

                        {'symbol': symbol, 'side': 'buy', 'quantity': symbol_amount, 'price': symbol_price, 'type': 'LIMIT', 'timeInForce': 'FOK', 'timestamp': timestamp},
                        {'symbol': symbol2, 'side': 'sell', 'quantity': symbol_amount, 'price': symbol2_price, 'type': 'LIMIT', 'timeInForce': 'FOK', 'timestamp': timestamp},
                        {'symbol': pair3, 'side': pair3_side, 'quantity': pair3_amount, 'price': pair3_price, 'type': 'LIMIT', 'timeInForce': 'FOK', 'timestamp': timestamp}

                    ]

                   
                    print(new_data_orders)
                    send_order(new_data_orders)
                    # print_orders(symbol, symbol2, pair3, end)
                    print('Symbol', symbol_price, 'Symbol2', symbol2_price, 'Symbol3', pair3_price)
                    raise



                iter += 1

            except KeyError:
                errors += 1
                continue 

    
        end = time.time() - start
        # print('Stream 1  Итераций: ',iter)
        # print('Stream 1  Время: ',end)
        # print('Stream 1  Длинна данных: ', len(data.keys())) 


def start_stream_1(data):
    symbols_webscoket_exchange(data)

