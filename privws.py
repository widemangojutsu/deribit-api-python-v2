import asyncio
import websockets
import json

class PrivateWSClient:
    def __init__(self, url, shared_state, api_key, api_secret):
        self.url = url
        self.shared_state = shared_state
        self.api_key = api_key
        self.api_secret = api_secret

    async def connect_and_listen(self):
        async with websockets.connect(self.url) as websocket:
            await self.authenticate(websocket)
            await self.subscribe_to_channels(websocket)
            while True:
                message = await websocket.recv()
                await self.handle_ws_message(message)

    async def authenticate(self, websocket):
        # Send authentication request
        # This is a simplified example; use your actual authentication method
        await websocket.send(json.dumps({
            "jsonrpc": "2.0",
            "id": 2,
            "method": "private/auth",
            "params": {
                "client_id": self.api_key,
                "client_secret": self.api_secret
            }
        }))

    async def subscribe_to_channels(self, websocket):
        # Example: Subscribe to private channels after authentication
        await websocket.send(json.dumps({
            "jsonrpc": "2.0",
            "id": 3,
            "method": "private/subscribe",
            "params": {
                "channels": ["user.orders.BTC-26MAR21.raw"]
            }
        }))


    async def send_order(self, instrument_name, amount, order_type="market", label=""):
        buy_order_message = {
            "jsonrpc": "2.0",
            "id": 5275,  # Unique ID for the request
            "method": "private/buy",
            "params": {
                "instrument_name": instrument_name,
                "amount": amount,
                "type": order_type,
                "label": label
            }
        }
        await self.websocket.send(json.dumps(buy_order_message))



    async def handle_ws_message(self, message):
        # Process private messages and update SharedState
        data = json.loads(message)
        # Example: Update SharedState with order information
        if 'params' in data and 'data' in data['params']:
            self.shared_state.set("private_orders", data['params']['data'])