import asyncio
from event_bus import EventBus
from sharedstate import send_order_through_websocket  # Assuming this function exists

class OMS:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.event_bus.subscribe('NEW_ORDER', self.handle_new_order)

    async def handle_new_order(self, order_data):
        order_instructions = order_data['instructions']
        instruments = order_data['instruments']
        spot_order = {'type': order_instructions[0], 'instrument': instruments[0], 'quantity': 1}
        futures_order = {'type': order_instructions[1], 'instrument': instruments[1], 'quantity': 1}
        await send_order_through_websocket(spot_order)
        await send_order_through_websocket(futures_order)

    def start(self):
        asyncio.get_event_loop().run_forever()