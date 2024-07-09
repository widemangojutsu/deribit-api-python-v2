import csv
import orjson
import asyncio
import websockets
from concurrent.futures import ThreadPoolExecutor


def process_and_save_data(data_chunk, file_name):
    # Process data (e.g., parse JSON)
    data = orjson.loads(data_chunk)
    # Assuming data is a list of dictionaries
    with open(file_name, 'a', newline='') as file:
        writer = csv.writer(file)
        for item in data:
            writer.writerow([item['field1'], item['field2'], item['field3']])  # Adjust field names as needed




async def call_api(msg):
    async with websockets.connect('wss://www.deribit.com/ws/api/v2') as websocket:
        await websocket.send(orjson.dumps(msg))
        with ThreadPoolExecutor(max_workers=5) as executor:  # Adjust number of workers as needed
            while websocket.open:
                response = await websocket.recv()
                # Submit the processing and saving task to the thread pool
                executor.submit(process_and_save_data, response, 'output.csv')


msg = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "public/get_instruments",
    "params": {
        "currency": "BTC",
        "kind": "future",
        "expired": "true"  # Corrected parameter to request expired futures
    }
}

async def call_api(msg):
    async with websockets.connect('wss://www.deribit.com/ws/api/v2') as websocket:
        await websocket.send(orjson.dumps(msg))
        while websocket.open:
            response = await websocket.recv()
            print(response)  # Prints the response from the server

asyncio.run(call_api(msg))