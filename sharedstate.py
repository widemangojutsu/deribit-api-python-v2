import asyncio
import websockets
import orjson
import hmac
import hashlib
from datetime import datetime
import time
import config
from data import DataManager
from get_instruments import should_fetch_new_data, fetch_instruments
from feeds import channel_generator
import urllib.parse
import base64
from event_bus import EventBus
import pandas as pd
import yaml
from shared_option_df import initialize_shared_options_df, update_shared_options_df, get_shared_options_df
from cashcarry import CashCarry

with open('parameters.yaml', 'r') as file:
    params = yaml.safe_load(file)

currency = params['currency'] 

def get_currency():
    return params['currency']

# Initialize the shared DataFrame globally
data_df = pd.DataFrame()
# Set the option to display all columns (None means no limit)
pd.set_option('display.max_columns', None)

option_columns = [
    'options_session_upl', 'options_gamma', 'options_vega', 
    'projected_delta_total', 'options_vega_map', 'options_delta', 
    'options_theta', 'delta_total', 'delta_total_map', 
    'options_pl', 'options_value', 'options_gamma_map'
]

# Define the WebSocket connection globally
websocket = None

async def init_websocket():
    global websocket
    url = config.DERIBIT_URL  # Modify with your actual WebSocket URL
    websocket = await websockets.connect(url)
    return websocket

# Function to get the shared data DataFrame
def get_shared_data_df():
    global data_df
    return data_df

# Function to update the shared data DataFrame
def update_shared_data_df(new_data):
    global data_df
    data_df = pd.concat([data_df, new_data])

# Ensure WebSocket is initialized when the module is loaded
asyncio.get_event_loop().run_until_complete(init_websocket())

class MessageHandler:
    def __init__(self, client):
        self.client = client  # Reference to the WebSocket client to access its properties and methods

    async def handle_message(self, message):
        if 'result' in message and 'access_token' in message['result']:
            await self.handle_auth_response(message)
        elif 'result' in message and isinstance(message['result'], list):
            await self.handle_subscription_response(message)
        elif 'result' in message and isinstance(message['result'], str):
            await self.handle_heartbeat_response(message)
        elif 'method' in message and message['method'] == 'subscription':
            await self.handle_user_channel(message)
        else:
            print("Received an unrecognized message format:")
            print(message)

    async def handle_auth_response(self, message):
        self.client.access_token = message['result']['access_token']
        print("Authentication successful, access token saved.")

    async def handle_subscription_response(self, message):
        print("Subscription successful to channels:", message['result'])

    async def handle_heartbeat_response(self, message):
        print("Heartbeat response received:", message['result'])

    async def handle_user_channel(self, message):
        channel = message['params']['channel']
        data = message['params']['data']
        if channel == 'user.portfolio.btc':
            # Convert the data dictionary to a DataFrame row and append it to user_risk
            df_row = pd.DataFrame([data])
            self.client.user_risk = pd.concat([self.client.user_risk, df_row], ignore_index=True)
            # Print the updated User Risk DataFrame
            print("Updated User Risk DataFrame:")
            print(self.client.user_risk)

class DbitWS:
    def __init__(self, currency, data_manager, event_bus):
        self.client_id = config.CLIENT_ID
        self.client_secret = config.CLIENT_SECRET
        self.url = config.DERIBIT_URL
        self.currency = currency
        self.data_manager = data_manager
        self.event_bus = event_bus
        self.websocket = None
        self.access_token = None
        self.subscribed_channels = set()
        self.event_bus.subscribe('FETCH_INSTRUMENTS', self.handle_fetch_instruments)

    async def connect(self):
        self.websocket = await websockets.connect(self.url)
        await self.authenticate()
        await self.subscribe_to_channels()
        self.event_bus.subscribe('SEND_ORDER', self.send_order)

    async def send_order_through_websocket(order):
        global websocket
        await websocket.send(order)

    async def send_order(self, order):
        await self.send_message(order)

    async def authenticate(self):
        timestamp, nonce, signature = self.generate_signature()
        auth_message = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "public/auth",
            "params": {
                "grant_type": "client_signature",
                "client_id": self.client_id,
                "timestamp": timestamp,
                "signature": signature,
                "nonce": nonce
            }
        }
        await self.send_message(auth_message)
        response = await self.receive_message()
        if 'result' in response and 'access_token' in response['result']:
            self.access_token = response['result']['access_token']
            print("Authentication successful, access token saved.")

    async def send_message(self, message):
        serialized_message = orjson.dumps(message).decode('utf-8')
        await self.websocket.send(serialized_message)

    async def receive_message(self):
        response = await self.websocket.recv()
        return orjson.loads(response)

    async def subscribe_to_channels(self):
        if self.access_token:
            subscribe_message = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "private/subscribe",
                "params": {
                    "channels": ["user.portfolio." + self.currency],
                    "access_token": self.access_token
                }
            }
            await self.send_message(subscribe_message)
            print(f"Subscribed to user portfolio channel for {self.currency}")

    def generate_signature(self):
        timestamp = int(time.time() * 1000)
        nonce = "nonce"
        data = ""
        message = f"{timestamp}\n{nonce}\n{data}"
        signature = hmac.new(self.client_secret.encode(), message.encode(), hashlib.sha256).hexdigest()
        return timestamp, nonce, signature

    async def send_heartbeat(self, interval=60):
        heartbeat_message = {
                        "jsonrpc": "2.0",
            "id": 9098,
            "method": "public/set_heartbeat",
            "params": {
                "interval": interval
            }
        }
        await self.send_message(heartbeat_message)
        print(f"Heartbeat set with interval {interval} seconds.")

    async def send_test_message(self):
        test_message = {
            "jsonrpc": "2.0",
            "id": 8212,
            "method": "public/test",
            "params": {}
        }
        await self.send_message(test_message)
        print("Test message sent.")

    async def handle_incoming_message(self):
        try:
            while self.websocket.open:
                response = await self.receive_message()
                await self.process_message(response)
        except websockets.exceptions.ConnectionClosed:
            print("WebSocket connection closed.")
        except Exception as e:
            print(f"An error occurred: {e}")

    async def process_message(self, message):
        await self.message_handler.handle_message(message)

    async def subscribe_to_data(msg):
        """
        Send a subscription message to the WebSocket and return the response.
        """
        global websocket
        if not websocket:
            await init_websocket()  # Ensure the WebSocket is initialized

        # Serialize the message for sending
        serialized_message = orjson.dumps(msg).decode('utf-8')
        await websocket.send(serialized_message)

        # Wait for the response
        response = await websocket.recv()
        return orjson.loads(response)

    async def receive_message(self):
        response = await self.websocket.recv()
        print(response)
        return orjson.loads(response)

    async def connect(self):
        self.websocket = await websockets.connect(self.url)
        await self.authenticate()
        try:
            await self.handle_incoming_message()
        finally:
            await self.websocket.close()

    async def subscribe_to_channels(self):
        # Existing subscriptions
        if self.channels:
            subscribe_message = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "public/subscribe",
                "params": {
                    "channels": self.channels
                }
            }
            await self.send_message(subscribe_message)
            self.subscribed_channels.update(self.channels)
            print(f"Subscribed to channels: {self.channels}")

    async def sub_to_priv(self, channels=None):
        if not channels:  # Default to a basic portfolio channel if none provided
            channels = [f"user.portfolio.{self.currency}",
                        f"user.changes.future.{self.currency}.raw",
                        f"user.changes.spot.{self.currency}.raw",
                        f"user.changes.option.{self.currency}.raw"]
        if self.access_token:  # Ensure you have an access token
            subscribe_message = {
                "jsonrpc": "2.0",
                "id": 111,
                "method": "private/subscribe",
                "params": {
                    "channels": channels,
                    "access_token": self.access_token
                }
            }
            await self.send_message(subscribe_message)
            self.subscribed_channels.update(channels)
            print(f"Subscribed to private channels: {channels}")
        else:
            print("Cannot subscribe to private channels: access token is missing.")

    async def handle_fetch_instruments(self, params):
        try:
            currency = params['currency']
            kind = params['kind']
            instruments = await self._fetch_instruments(currency, kind)
            self.event_bus.publish('INSTRUMENTS_DATA', instruments)
        except Exception as e:
            logging.error(f"Error fetching instruments: {e}")

    async def _fetch_instruments(self, currency, kind):
        request = {
            "jsonrpc": "2.0",
            "id": 42,
            "method": "public/get_instruments",
            "params": {
                "currency": currency,
                "kind": kind,
                "expired": False
            }
        }
        await self.send_message(request)
        response = await self.receive_message()
        return response

async def implement_strategy():
    event_bus = EventBus()
    strategy = CashCarry(event_bus)
    await strategy.fetch_and_store_instruments()

async def main():
    # Load parameters from YAML
    with open('parameters.yaml', 'r') as file:
        params = yaml.safe_load(file)
    currency = params['currency']
    event_bus = EventBus()
    data_manager = DataManager()
    dbit_ws = DbitWS(currency, data_manager, event_bus)
    await dbit_ws.connect()
    await implement_strategy()

if __name__ == '__main__':
    asyncio.run(main())