import config
from urllib.parse import urlencode
import hmac
import hashlib
import base64
from datetime import datetime
import websockets
import asyncio
import orjson
import gzip

class HtxWSClient:
    def __init__(self, api_key=None, api_secret=None):
        # Use HTX_API_KEY and HTX_SECRET_KEY from config.py
        self.api_key = api_key or config.HTX_API_KEY
        self.api_secret = api_secret or config.HTX_SECRET_KEY
        if not self.api_key or not self.api_secret:
            raise ValueError("API key or secret is not set. Please check your configuration.")

    def generate_signature(self, method, host, path, params):
        sorted_params = sorted(params.items())
        encoded_params = urlencode(sorted_params)
        pre_signed_text = f"{method}\n{host}\n{path}\n{encoded_params}"
        hmac_key = self.api_secret.encode('utf-8')
        message = pre_signed_text.encode('utf-8')
        signature = hmac.new(hmac_key, message, digestmod=hashlib.sha256).digest()
        return base64.b64encode(signature).decode('utf-8')

    def create_websocket_request(self):
        method = "GET"
        host = "api.huobi.pro"
        path = "/ws/v2"
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        params = {
            "AccessKeyId": self.api_key,
            "SignatureMethod": "HmacSHA256",
            "SignatureVersion": "2",
            "Timestamp": timestamp
        }
        signature = self.generate_signature(method, host, path, params)
        if signature:
            websocket_request = {
                "action": "req",
                "ch": "auth",
                "params": {
                    "authType": "api",
                    "accessKey": self.api_key,
                    "signatureMethod": "HmacSHA256",
                    "signatureVersion": "2.1",
                    "timestamp": timestamp,
                    "signature": signature
                }
            }
            return websocket_request
        return None



    async def connect(self, symbol):
        method = "GET"
        host = "api.huobi.pro"
        path = f"/ws/v2/market/{symbol}/bbo"  # Correctly format the path with the symbol
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        params = {
            "AccessKeyId": self.api_key,
            "SignatureMethod": "HmacSHA256",
            "SignatureVersion": "2",
            "Timestamp": timestamp
        }
        signature = self.generate_signature(method, host, path, params)
        url = f"wss://{host}{path}?{urlencode(params)}&Signature={signature}"
        self.websocket = await websockets.connect(url)
        return self.websocket

    async def send_websocket_request(self, request):
        json_request = orjson.dumps(request).decode('utf-8')  # Convert dictionary to JSON string using json
        await self.websocket.send(json_request)
        print("WebSocket request sent:", json_request.decode('utf-8'))  # Decode for printing if necessary

        # Wait for the response
        response = await self.websocket.recv()
        try:
            # Attempt to parse the response if it's expected to be JSON
            response_data = orjson.loads(response)
            print("Received response:", response_data)
            return response_data
        except orjson.JSONDecodeError:
            # Handle cases where the response is not JSON
            print("Received non-JSON response:", response)
            return response

    async def receive_messages(self):
        try:
            while True:
                message = await self.websocket.recv()
                try:
                    # Attempt to decompress the data assuming it's gzip-compressed
                    decompressed_message = gzip.decompress(message)
                    # Use orjson to deserialize the bytes into a Python object
                    message_data = orjson.loads(decompressed_message)
                    print("Received decompressed and parsed message:", message_data)
                except OSError:
                    # If decompression fails, assume the data is not compressed
                    try:
                        message_data = orjson.loads(message)
                        print("Received message:", message_data)
                    except orjson.JSONDecodeError:
                        # If it's not JSON, print the raw message
                        print("Received non-JSON message:", message)
        except websockets.exceptions.ConnectionClosed:
            print("WebSocket connection closed")


async def main():
    client = HtxWSClient()
    websocket_request = client.create_websocket_request()
    
    if websocket_request:
        await client.send_websocket_request(websocket_request)
        await client.receive_messages()
    else:
        print("Failed to create WebSocket request.")

if __name__ == '__main__':
    asyncio.run(main())

