# types of bitcoin futures


# deribit inverse contracts

#using btc position size (at time of entry):
# usdprofit = (exit price - entry price) * position size in bitcoin

#using usd position size:
# usdprofit = (exit price/entryprice - 1) * position size in usd

# caluculate btc profit/loss for deribit inverse futures
# using btc position size (at time of entry):
# btc profit = (exit price - entry price) / exit price * position size in bitcoin

# using usd position size:
# btc profit = (1 / entry price - 1 / exit price) * position size in usd
import time


class dbitcalculator:
    def __init__(self, entry_price, position_size_btc=None, position_size_usd=None):
        self.entry_price = entry_price
        self.position_size_btc = position_size_btc
        self.position_size_usd = position_size_usd

    def calculate_usd_profit(self, exit_price):
        if self.position_size_btc is not None:
            return (exit_price - self.entry_price) * self.position_size_btc
        elif self.position_size_usd is not None:
            return (exit_price / self.entry_price - 1) * self.position_size_usd
        else:
            raise ValueError("Position size not set")

    def calculate_btc_profit(self, exit_price):
        if self.position_size_btc is not None:
            return (exit_price - self.entry_price) / exit_price * self.position_size_btc
        elif self.position_size_usd is not None:
            return (1 / self.entry_price - 1 / exit_price) * self.position_size_usd
        else:
            raise ValueError("Position size not set")

    def set_position_size_btc(self, position_size_btc):
        self.position_size_btc = position_size_btc

    def set_position_size_usd(self, position_size_usd):
        self.position_size_usd = position_size_usd
        self.position_size_btc = position_size_usd / self.entry_price

# Example usage:
contract = DeribitContract(entry_price=8000, position_size_usd=5000)
exit_price = 10000
usd_profit = contract.calculate_usd_profit(exit_price)
btc_profit = contract.calculate_btc_profit(exit_price)

print(f"USD Profit: {usd_profit}")
print(f"BTC Profit: {btc_profit}")

# quanto better for bullish traders/speculators
# inverse futures better for bearish traders/hedgers
# quantto futures trade at premium to inverse futures

    def days_till_expire(self, expiration_date):
    

    def current_timestamp(self):
        return int(time.time() * 1000)

