import requests
import time
import json
# from create_order import create_binance_FOKorder, create_binance_market_order, cancel_binance_order, create_binance_FOKorder_FOK
from create_order import create_okx_FOKorder, create_okx_limit_order, create_okx_market_order, send_order

def get_symbols_websocket_connect():
    params = {'instType': 'SPOT'}
    res = requests.get('https://www.okx.com/api/v5/public/instruments', params=params)
    
    symbols = json.loads(res.text)
 
    symbols_list = []
    for symbol in symbols['data']:
        for symbol2 in symbols['data']:
            if symbol2['quoteCcy'] == 'USDT':
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
    print('Stream 2 запущен')
    symbols_tag = {}

    while True:
        data = queue.get()
        errors = 0
        iter = 0
        start = time.time()
        for iteration in symbols:

            symbol = iteration[0]
            symbol2 = iteration[1]
            try:
                
                pair2 = settings[symbol]
                
                symbol_price = data[symbol]['ask']
                symbol2_price = data[symbol2]['bid']

                try:

                    pair3 = pair2['symbol1'] + '-USDT'
                    pair3_price = data[pair3]['ask']
                    symbol3_price = float(symbol_price) * float(pair3_price)

                except KeyError:

                    pair3 = 'USDT-' + pair2['symbol1']
                    pair3_price = data[pair3]['bid']
                    symbol3_price = float(symbol_price) / float(pair3_price)
            
                end = 100 - symbol3_price / float(symbol2_price) * 100
                # print(end, symbol, symbol2)
                if end > 0.3:
                    print('Stream 2: ',end, symbol, symbol2)
                    continue
                    # pair3_amount = 3.20 / float(pair3_price)
                    # pair3_side = ''
                    # if pair3[-4:] == 'USDT':
                    #     pair3_side = 'buy'
                    # else:
                    #     pair3_side = 'sell'
                    #     pair3_amount = 3.20

                    # symbol3_step_amount = create_okx_FOKorder(pair3, pair3_price, pair3_amount, pair3_side)

                    # #############
                    # if symbol3_step_amount == 'CANCEL':
                    #     continue

                    # symbol_amount = float(symbol3_step_amount) / float(symbol_price) 
                    # symbol_step2_amount = create_binance_FOKorder(symbol, symbol_price, symbol_amount, 'buy')
                    
         

                    # if flag == 0:
                    #     if pair3_side == 'buy':
                    #         create_binance_market_order(pair3, pair3_amount, 'sell')
                    #     else:
                    #         create_binance_market_order(pair3, pair3_amount, 'buy')
                    #     print('Stream 2  Step 2. Стоп по цене')
                    #     queue.get()
                    #     continue     

                    
                    # symbol2_step3_amount = create_binance_FOKorder(symbol2, symbol2_price, symbol_amount_N['quantity'], 'sell')

                    
                    # if flag == 0:
                    #     create_binance_market_order(symbol2, symbol_amount_N['quantity'], 'sell')
                    #     print('Stream 2  Step 3. Стоп по цене')
                    #     queue.get()
                    #     continue
                    
                
                    # print('Stream 2  Все ордера выполнены')
                    # queue.get()
                    pair3_side = ''

                    if pair3[-4:] == 'USDT':
                        pair3_side = 'buy'
                        pair3_amount = 3.20 / float(pair3_price)
                        # step = step_size[pair3]
                        # pair3_amount = round_to_step(float(pair3_amount), float(step))
                    else:
                        pair3_side = 'sell'
                        pair3_amount = 3.20  
                  
                    if pair3_side == 'buy':
                        amount_step2 = float(pair3_amount) / float(symbol_price)
                        # step = step_size[symbol]
                        
                        # amount_step2 = round_to_step(float(amount_step2), float(step))

                    else:
                        pair3_amount_sell = float(pair3_amount) * float(pair3_price)

                        amount_step2 = float(pair3_amount_sell) / float(symbol_price)
                        # step = step_size[symbol]

                        # amount_step2 = round_to_step(float(amount_step2), float(step))
                
                    timestamp = int(time.time() * 1000)

                    new_data_orders = [

                        {'symbol': pair3, 'side': pair3_side, 'quantity': pair3_amount, 'price': pair3_price, 'type': 'LIMIT', 'timeInForce': 'FOK', 'timestamp': timestamp},
                        {'symbol': symbol, 'side': 'buy', 'quantity': amount_step2, 'price': symbol_price, 'type': 'LIMIT', 'timeInForce': 'FOK', 'timestamp': timestamp},
                        {'symbol': symbol2, 'side': 'sell', 'quantity': amount_step2, 'price': symbol2_price, 'type': 'LIMIT', 'timeInForce': 'FOK', 'timestamp': timestamp}

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
        # print('Ошибок2: ',errors)
        # print('Stream 2  Итераций: ',iter)
        # print('Stream 2  Время: ',end)

def mo(queue):
    while True:
        try:
            data = queue.get()
            print(data['BTC-USDT']['ask'])
            print(data['BTC-USDT']['ask'])
            time.sleep(15)
        except Exception:
            continue
                        
def start_stream_2(queue):
   
    symbols_webscoket_exchange(queue)




