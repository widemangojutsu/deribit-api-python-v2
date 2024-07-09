import asyncio
import logging
from data import DataManager
from event_bus import EventBus

class CashCarry:
    def __init__(self, event_bus: EventBus):
        self.data_manager = DataManager()
        self.event_bus = event_bus
        self.currency = "BTC"  # Example currency, adjust as needed
        self.kinds = ["future", "spot"]

    async def fetch_and_store_instruments(self):
        for kind in self.kinds:
            await self._fetch_and_store_instrument_data(kind)

    async def _fetch_and_store_instrument_data(self, kind):
        try:
            # Publish a request to fetch instrument data
            request_params = {
                "currency": self.currency,
                "kind": kind
            }
            self.event_bus.publish('FETCH_INSTRUMENTS', request_params)

            # Listen for the response (assuming the event bus has a way to handle responses)
            response = await self._wait_for_response('INSTRUMENTS_DATA')
            if response:
                await self._store_instruments_data(kind, response)
        except Exception as e:
            logging.error(f"Error fetching or storing instrument data for {kind}: {e}")

    async def _wait_for_response(self, event_name):
        # Placeholder for waiting for a response from the event bus
        # Implement the actual logic to wait for and retrieve the response
        await asyncio.sleep(1)  # Simulate waiting for response
        return {"data": "example_data"}  # Replace with actual response data

    async def _store_instruments_data(self, kind, data):
        try:
            # Store the data in the lildata database under get_instruments folder
            await self.data_manager.store_data_in_arctic('get_instruments', f'{self.currency}_{kind}', data)
            logging.info(f"Instrument data for {kind} stored successfully.")
        except Exception as e:
            logging.error(f"Error storing instrument data for {kind}: {e}")

# Usage example
if __name__ == "__main__":
    event_bus = EventBus()  # Assuming EventBus is already implemented
    cash_carry = CashCarry(event_bus)
    asyncio.run(cash_carry.fetch_and_store_instruments())