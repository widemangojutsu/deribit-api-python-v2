import logging
from event_bus import EventBus

class OrderExecutor:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    def prepare_and_publish_order(self, signal):
        """Prepare order based on the signal and publish it to the event bus."""
        try:
            order = self._prepare_order(signal)
            self.event_bus.publish('NEW_ORDER', order)
            logging.info(f"Order published for signal {signal}")
        except Exception as e:
            logging.error(f"Failed to prepare or publish order for signal {signal}: {e}")
            raise

    def _prepare_order(self, signal):
        """Internal method to construct order parameters from a signal."""
        # Placeholder for order preparation logic
        order_params = {"type": "buy", "quantity": signal['quantity'], "price": signal['price']}
        return order_params

# Usage example
if __name__ == "__main__":
    event_bus = EventBus()  # Assuming EventBus is already implemented
    executor = Order,Executor(event_bus)
    signal = {"quantity": 100, "price": 50}  # Example signal
    executor.prepare_and_publish_order(signal)