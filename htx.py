import asyncio
import websockets
import gzip
import json
import datetime
import config
import requests
import hashlib
import hmac
import base64  # Import requests to handle HTTP POST

async def connect_to_htx():
    uri = config.HTX_WS_URL
    async with websockets.connect(uri) as websocket:
        # Authenticate
        await authenticate(websocket)

        # Continuously receive and handle messages
        while True:
            message = await websocket.recv()
            decompressed_message = gzip.decompress(message)
            data = json.loads(decompressed_message)
            print(data)

            if 'ping' in data:
                await send_message(websocket, 'pong', data['ping'])

async def authenticate(websocket):
    api_key = config.HTX_API_KEY
    secret_key = config.HTX_SECRET_KEY
    timestamp = datetime.datetime.utcnow().isoformat(timespec='seconds')
    
    # Prepare the string to sign
    method = "GET"  # Adjust if necessary based on the API's requirements
    endpoint = "/ws/v2"  # Example endpoint; adjust as necessary
    params_to_sign = f"accessKeyId={api_key}&signatureMethod=HmacSHA256&signatureVersion=2.1&timestamp={timestamp}"
    string_to_sign = f"{method}\n{endpoint}\n{params_to_sign}"
    
    # Generate the signature
    signature = hmac.new(secret_key.encode(), string_to_sign.encode(), hashlib.sha256).digest()
    signature_b64 = base64.b64encode(signature).decode()

    # Authentication data formatted according to the WebSocket API requirements
    auth_data = {
        "action": "req",
        "ch": "auth",
        "params": {
            "authType": "api",
            "accessKey": api_key,
            "signatureMethod": "HmacSHA256",
            "signatureVersion": "2.1",
            "timestamp": timestamp,
            "signature": signature_b64
        }
    }
    
    # Send authentication request
    await websocket.send(json.dumps(auth_data))
    response = await websocket.recv()

    # Decompress the response if it's gzip-compressed
    try:
        decompressed_response = gzip.decompress(response)
    except OSError:
        # If decompression fails, assume the response is not compressed
        decompressed_response = response

    # Convert bytes to string if necessary
    if isinstance(decompressed_response, bytes):
        decompressed_response = decompressed_response.decode('utf-8')

    response_data = json.loads(decompressed_response)
    return response_data.get("status") == "ok"

async def send_message(websocket, message_type, data):
    if message_type == 'pong':
        pong_data = {
            "op": "pong",
            "ts": data  # Send back the same value received in ping
        }
        await websocket.send(json.dumps(pong_data))
        print(f"Sent pong with ts: {data}")
    elif message_type == 'auth':
        await websocket.send(json.dumps(data))
    else:
        # Assuming RESTful POST for other types of messages
        url = f"{config.HTX_API_URL}/{message_type}"  # Construct URL for RESTful API
        response = requests.post(url, json=data)
        print(f"Sent {message_type} via POST with response: {response.status_code}")

if __name__ == '__main__':
    asyncio.run(connect_to_htx())