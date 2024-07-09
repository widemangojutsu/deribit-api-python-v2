class BuyTrade:
    def __init__(self, instrument_name: str, order_type: str = "limit", amount: float = None, contracts: int = None,
                 label: str = None, price: float = None, time_in_force: str = "good_til_cancelled", max_show: int = 0,
                 post_only: bool = False, reject_post_only: bool = False, reduce_only: bool = False,
                 trigger_price: float = None, trigger_offset: float = None, trigger: str = None, advanced: str = None,
                 mmp: bool = False, valid_until: int = None, linked_order_type: str = None,
                 trigger_fill_condition: str = "first_hit", otoco_config: list = None):
        """
        Initialize a BuyTrade object with all necessary parameters for the /private/buy endpoint.

        :param instrument_name: str - The name of the trading instrument.
        :param order_type: str - The type of order (e.g., limit, market, stop_limit).
        :param amount: float - The amount in USD units or underlying base currency coin.
        :param contracts: int - The order size in contract units.
        :param label: str - User-defined label for the order (maximum 64 characters).
        :param price: float - The order price in base currency.
        :param time_in_force: str - How long the order remains in effect.
        :param max_show: int - Maximum amount within an order to be shown to other customers.
        :param post_only: bool - If true, the order is considered post-only.
        :param reject_post_only: bool - If set to true, the order is put to the order book unmodified or rejected.
        :param reduce_only: bool - If true, the order is considered reduce-only.
        :param trigger_price: float - Trigger price for trigger orders only.
        :param trigger_offset: float - The maximum deviation from the price peak for trigger orders.
        :param trigger: str - Defines the trigger type (e.g., index_price, mark_price).
        :param advanced: str - Advanced option order type.
        :param mmp: bool - Order MMP flag, only for order_type 'limit'.
        :param valid_until: int - Timestamp until when the order is valid.
        :param linked_order_type: str - Type of the linked order.
        :param trigger_fill_condition: str - The fill condition of the linked order.
        :param otoco_config: list - List of trades to create or cancel when this order is filled.
        """
        self.instrument_name = instrument_name
        self.order_type = order_type
        self.amount = amount
        self.contracts = contracts
        self.label = label
        self.price = price
        self.time_in_force = time_in_force
        self.max_show = max_show
        self.post_only = post_only
        self.reject_post_only = reject_post_only
        self.reduce_only = reduce_only
        self.trigger_price = trigger_price
        self.trigger_offset = trigger_offset
        self.trigger = trigger
        self.advanced = advanced
        self.mmp = mmp
        self.valid_until = valid_until
        self.linked_order_type = linked_order_type
        self.trigger_fill_condition = trigger_fill_condition
        self.otoco_config = otoco_config

    async def create_order_payload(self):
        """
        Validate necessary parameters and create the payload for the API request asynchronously.

        :return: dict - The payload for the order.
        """
        if not self.instrument_name:
            raise ValueError("Instrument name is required")
        if self.amount is None and self.contracts is None:
            raise ValueError("Either amount or contracts must be provided")

        payload = {
            "instrument_name": self.instrument_name,
            "type": self.order_type,
            "label": self.label,
            "price": self.price,
            "time_in_force": self.time_in_force,
            "max_show": self.max_show,
            "post_only": self.post_only,
            "reject_post_only": self.reject_post_only,
            "reduce_only": self.reduce_only,
            "trigger_price": self.trigger_price,
            "trigger_offset": self.trigger_offset,
            "trigger": self.trigger,
            "advanced": self.advanced,
            "mmp": self.mmp,
            "valid_until": self.valid_until,
            "linked_order_type": self.linked_order_type,
            "trigger_fill_condition": self.trigger_fill_condition,
            "otoco_config": self.otoco_config
        }

        # Include amount or contracts based on what is provided
        if self.amount is not None:
            payload["amount"] = self.amount
        if self.contracts is not None:
            payload["contracts"] = self.contracts

        return payload

    async def submit_order(self):
        """
        Simulate the interaction with the trading API to submit the order asynchronously.

        :return: dict - The simulated API response.
        """
        payload = await self.create_order_payload()
        print("Submitting order with payload:", payload)
        # Simulate API response
        return {"status": "success", "data": payload}