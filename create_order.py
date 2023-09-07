import ccxt
import time
import asyncio
import hmac
import hashlib
import aiohttp

okx = ccxt.okx({
    'enboleRateLimit': False,
    'apiKey': '43a9b1aa-b840-45c5-86e5-a221988a922d',
    'secret': 'B8C400F21BA6999F02A7CFDF9F80C7F3',
    'password': 'CODDICODDICODi1!'
})

def create_okx_market_order(symbol, amount, side):
    try:
        type = 'market'
        order = okx.create_order(symbol, type, side, amount)
        print(order)
        return order['info']['ordId']
    except Exception as e:
        print('Order failed', e)
        return 0
    # if side == 'buy':
    #     return order['info']['executedQty']
    # if side == 'sell':
    #     return order['info']['cummulativeQuoteQty']


def create_okx_limit_order(symbol, price, amount, side):
    type = 'limit'
    order = okx.create_order(symbol, type, side, amount, price)
    return order['info']['ordId']


def create_okx_FOKorder(symbol, side, price, amount):
    print('Данные получены: ',symbol, price, amount, side)
    
    type = 'limit'
    order = okx.create_order(symbol, type, side, amount, price, {'timeInForce': 'FOK'})
    print(order)

    # if order['status'] == 'FILLED':
    #     if side == 'buy':
    #         return order['info']['executedQty']
    #     if side == 'sell':
    #         return order['info']['cummulativeQuoteQty']
    # else:
    #     return 'CANCEL'




def start_load(data):
    while True:
        if data:
            symbol = ''
            price_symbol = ''
            for i in data.keys():
                if i[-4:] == 'USDT':
                    symbol = i
                    price_symbol = data[i]['ask']
                    break
                else:
                    continue
            amount = 15 / float(price_symbol)
            price = float(price_symbol) - float(price_symbol) * 0.7 / 100
            order = okx.create_order(symbol, 'limit', 'buy', amount, price, {'timeInForce': 'FOK'})
            if order['info']['status'] == 'FILLED':
                print('Начальный ордер исполнен')
                break
            else:
                break



start_program = time.time()

def time_start():
    seconds = time.time() - start_program 
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60

    return f"{hours} часов, {minutes} минут, {remaining_seconds} секунд"

async def place_orders_async(orders):
    api_key = '43a9b1aa-b840-45c5-86e5-a221988a922d'
    api_secret = 'B8C400F21BA6999F02A7CFDF9F80C7F3'
    
    base_url = "https://www.okx.com/api/v5/sprd/order"
    headers = {
        "X-MBX-APIKEY": api_key
    }

    async def place_order(session, order):
        # await asyncio.sleep(0.04)
        try:
            query_string = "&".join([f"{key}={order[key]}" for key in order])
            signature = hmac.new(api_secret.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256).hexdigest()
            order["signature"] = signature
            order['timestamp'] == int((time.time() - 0.10) * 1000) 
            
      
            async with session.post(base_url, params=order, headers=headers) as response:
                response_json = await response.json()
                if response.status == 200:
                    # print(f"Order placed successfully: {response_json}")
                    pass
                else:
                    print(f"Error placing order: {response_json}")
        except Exception as e:
            print(f"Error placing order: {e}")

    async with aiohttp.ClientSession() as session:
        tasks = [place_order(session, order) for order in orders]
        await asyncio.gather(*tasks)
        
orders_c = 0

def send_order(orders):
    global orders_c
    start = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(place_orders_async(orders))
    orders_c += 1
    end_time = time.time() - start
    end_time = float("{:.4f}".format(end_time))
    print(f'Время выполнения: {end_time}mc   Шаг ордера: {orders_c}   Время работы: {time_start()}')

