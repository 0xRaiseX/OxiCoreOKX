import requests
import hmac
import base64
import hashlib

def load_tickers():
    api_url = 'https://www.okx.com/api/v5/public/instruments'
    params = {'instType': 'SPOT'}

    responce = requests.get(api_url, params=params)
    data = responce.json()

    symbols = [symbol_data['instId'] for symbol_data in data['data']]
    
    return symbols


def generate_signature(secret_key, timestamp, method, request_path):
    # Конкатенируйте все данные в одну строку
    data_to_sign = f"{timestamp}{method}{request_path}"

    # Преобразуйте секретный ключ в байты
    secret_key_bytes = bytes(secret_key, 'utf-8')

    # Выполните HMAC SHA256 шифрование
    signature = hmac.new(secret_key_bytes, data_to_sign.encode('utf-8'), hashlib.sha256).digest()

    # Преобразуйте результат в Base64 строку
    signature_base64 = base64.b64encode(signature).decode('utf-8')

    return signature_base64
