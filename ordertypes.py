class OrderTypes:
    @staticmethod
    def market_order(quantity, price):
        return {"type": "market", "quantity": quantity, "price": price}

    @staticmethod
    def limit_order(quantity, price):
        return {"type": "limit", "quantity": quantity, "price": price}

    @staticmethod
    def stop_order(quantity, price, stop_price):
        return {"type": "stop", "quantity": quantity, "price": price, "stop_price": stop_price}

    # Add more order types as needed