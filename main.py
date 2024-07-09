import asyncio
from sharedstate import DbitWS, get_currency
from event_bus import EventBus
from data import DataManager

async def main():
    print("Starting feeds...")
    event_bus = EventBus()
    data_manager = DataManager()
    currency = get_currency()  # Fetch currency from sharedstate.py
    dbit_ws = DbitWS(currency, data_manager, event_bus)
    await dbit_ws.connect()

if __name__ == '__main__':
    asyncio.run(main())