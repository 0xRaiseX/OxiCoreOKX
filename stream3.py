import requests
import time
import json
# from create_order import create_binance_FOKorder, create_binance_market_order

def get_symbols_websocket_connect():
    params = {'instType': 'SPOT'}
    res = requests.get('https://www.okx.com/api/v5/public/instruments', params=params)
    
    symbols = json.loads(res.text)
 
    symbols_list = []
    for symbol in symbols['data']:
        for symbol2 in symbols['data']:
            if symbol2['quoteCcy'] != 'USDT' and symbol['quoteCcy'] != 'USDT':
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
    print('Stream 3 запущен')
    while True:
        data = queue.get()
        errors = 0
        start = time.time()

        for iteration in symbols:

            symbol = iteration[0]
            symbol2 = iteration[1]
            try:
                
                pair1 = settings[symbol]
                pair2 = settings[symbol2]

                symbol_price = data[symbol]['ask']
                symbol2_price = data[symbol2]['bid']

                try:
                    pair3 = pair1['symbol1'] + '-USDT'
                    pair3_price = data[pair3]['ask']
                    symbol3_price = float(symbol_price) * float(pair3_price)

                except KeyError:
        
                    pair3 = 'USDT-' + pair1['symbol1']
                    pair3_price = data[pair3]['bid']
                    symbol3_price = float(symbol_price) / float(pair3_price)

                try:

                    pair4 = pair2['symbol1'] + '-USDT'
                    pair4_price = data[pair4]['bid']
                    symbol4_price = float(symbol2_price) * float(pair4_price)

                except KeyError:

                    pair4 = 'USDT-' + pair2['symbol1']
                    pair4_price = data[pair4]['ask']
                    symbol4_price = float(symbol2_price) / float(pair4_price)

                end = 100 - symbol3_price / symbol4_price * 100
                # print(end, symbol, symbol2)
                if end > 0.4:
                    # print('Stream 3: ', end, symbol, symbol2)
                    continue

                    amount = 15 / float(pair3_price)
                    symbol3_step_amount = create_binance_FOKorder(pair3, pair3_price, amount, 'buy')

                    if symbol3_step_amount == 'CANCEL':
                        continue
                    amount_symbol = amount / float(symbol_price)
                    symbol_step2_amount = create_binance_FOKorder(symbol, symbol_price, amount_symbol, 'buy')

                    if symbol_step2_amount == 'CANCEL':
                        create_binance_market_order(pair3, amount, 'sell')
                        print('Stream 3  Step 2. Стоп по цене')
                        continue

                    symbol2_step3_amount = create_binance_FOKorder(symbol2, symbol2_price, symbol_step2_amount, 'sell')

                    if symbol2_step3_amount == 'CANCEL':
                        create_binance_market_order(symbol, amount_symbol, 'sell')
                        create_binance_market_order(pair3, amount, 'sell')
                        print('Stream 3  Step 3. Стоп по цене')
                        continue

                    symbol4_step4_amount = create_binance_FOKorder(pair4, pair4_price, symbol2_step3_amount, 'sell')
                    if symbol4_step4_amount == 'CANCEL':
                        create_binance_market_order(pair4, symbol2_step3_amount, 'sell')
                        print('Stream 3  Step 4. Стоп по цене')
                        continue
                    print('Stream 3  Все ордера исполнены')
            except KeyError:
                errors += 1
                continue 

    
        end = time.time() - start
        # print('Stream 3  Итераций: ',iter)
        # print('Stream 3  Время: ',end)

def monitoring(queue):
    while True:

        time.sleep(1)
        try:
            data = queue.get()
            print(data['BTC-USDT']['ask'])
            print(data['BTC-USDT']['bid'])
       
        except KeyError:
            continue
                        
def start_stream_3(queue):
    symbols_webscoket_exchange(queue)

