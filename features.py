import numpy as np
from numba import jit
import pandas as pd
import datetime



class Features:
    def __init__(self):
        pass
    @staticmethod
    @jit(nopython=True)
    def bid_ask_spread(asks, bids):
        """Calculate the bid-ask spread.

        Args:
            asks (np.array): Array of ask prices and quantities.
            bids (np.array): Array of bid prices and quantities.

        Returns:
            float: The bid-ask spread.
        """
        best_ask = asks[0][0]  # First element of the first ask
        best_bid = bids[0][0]  # First element of the first bid
        spread = best_ask - best_bid
        return spread

    
    @staticmethod
    @jit(nopython=True)
    def calculate_total_volume(asks, bids):
        """Calculate the total volume of asks and bids.

        Args:
            asks (np.array): Array of ask prices and quantities.
            bids (np.array): Array of bid prices and quantities.

        Returns:
            tuple: Total ask volume, Total bid volume
        """
        total_ask_volume = np.sum(asks[:, 1])  # Sum of all ask quantities
        total_bid_volume = np.sum(bids[:, 1])  # Sum of all bid quantities
        return total_ask_volume, total_bid_volume

    
    @staticmethod
    @jit(nopython=True)
    def midprice(asks, bids):
        """Calculate the midprice.

        Args:
            asks (np.array): Array of ask prices and quantities.
            bids (np.array): Array of bid prices and quantities.

        Returns:
            float: The midprice.
        """
        best_ask = asks[0][0]  # First element of the first ask
        best_bid = bids[0][0]  # First element of the first bid
        midprice = (best_ask + best_bid) / 2
        return midprice

    
    @staticmethod
    @jit(nopython=True)
    def weighted_midprice(asks, bids, imbal):
        """Calculate the weighted midprice.

        Args:
            asks (np.array): Array of ask prices and quantities.
            bids (np.array): Array of bid prices and quantities.

        Returns:
            float: The weighted midprice.
        """
        best_ask = asks[0][0]  # First element of the first ask
        best_bid = bids[0][0]  # First element of the first bid
        weighted_midprice = best_bid(1 - imbal) + best_ask(imbal)
        return weighted_midprice
    
    
    def calculate_imbalance(asks, bids):
        """Calculate the imbalance.

        Args:
            asks (np.array): Array of ask prices and quantities.
            bids (np.array): Array of bid prices and quantities.

        Returns:
            float: The imbalance.
        """
        best_askq = asks[0][1]  # First element of the first ask
        best_bidq = bids[0][1]  # First element of the first bid
        imbalance = best_bidq/(best_bidq+best_askq)
        return imbalance


    
    @staticmethod
    @jit(nopython=True)
    def micro_price(asks, bids):
        """
        Calculate the micro price based on the best ask and bid prices and quantities.
        """
        best_ask_price, best_ask_quantity = asks[0]
        best_bid_price, best_bid_quantity = bids[0]
        micro_price = (best_ask_price * best_bid_quantity + best_bid_price * best_ask_quantity) / (best_ask_quantity + best_bid_quantity)
        return micro_price


    def handle_btcspotdf(self, message):
        btc_futures_df = pd.DataFrame(message['result'])
        pd.set_option('display.max_columns', None)  # Adjust as needed
        pd.set_option('display.max_rows', 10)  # Adjust as needed
        pd.set_option('display.width', 1000)  # Adjust the width to fit your console
        print(btc_futures_df)

    def handle_btcfutdf(self, message):
        # Create the DataFrame from the message result
        btc_futures_df = pd.DataFrame(message['result'])
        
        # Select only the required columns
        required_columns = [
            'expiration_timestamp', 
            'settlement_period', 
            'creation_timestamp', 
            'is_active', 
            'instrument_name', 
            'maker_commission'  # Assuming the correct name is 'maker_commission'
        ]
        
        # Filter the DataFrame to include only the required columns
        filtered_df = btc_futures_df[required_columns]
        
        return filtered_df
    

    def get_current_timestamp(self):
        """Returns the current timestamp in milliseconds."""
        return int(datetime.now().timestamp() * 1000)


    
    def days_till_expiration(self, expiration_timestamp):
        """Calculates the days until expiration.
        
        Args:
            expiration_timestamp (int): The expiration timestamp in milliseconds.
            
        Returns:
            int: The number of days until expiration.
        """
        current_timestamp = self.get_current_timestamp()
        # Convert timestamps from milliseconds to seconds for datetime
        expiration_date = datetime.fromtimestamp(expiration_timestamp / 1000)
        current_date = datetime.fromtimestamp(current_timestamp / 1000)
        delta = expiration_date - current_date
        return delta.days

    
    @staticmethod
    @jit(nopython=True)
    def t(self, expiration_timestamp, create_timestamp):
        """Calculate time to expiration in years."""
        expiration_date = pd.to_datetime(expiration_timestamp)
        create_date = pd.to_datetime(create_timestamp)
        return (expiration_date - create_date).days / 365.25
    
    def extract_instrument_name(self, message):
        # Placeholder for extracting instrument_name from the message
        # The actual implementation depends on the message structure
        # For example:
        return message.get('result', {}).get('instrument_name')
    

    def get_trader_fair(instrument_price, usd_borrow_rate, btc_lending_rate):
        """
        Calculate the trader fair price based on borrow and lending rates.

        Args:
            instrument_price (float): The price of the instrument.
            usd_borrow_rate (float): The USD borrow rate.
            btc_lending_rate (float): The BTC lending rate.

        Returns:
            float: The trader fair price.
        """
        # Example calculation, adjust formula as needed
        trader_fair = instrument_price * (1 + usd_borrow_rate - btc_lending_rate)
        return trader_fair
    

    def pd_outright(futures_price, spot_price):
        """
        Calculate the outright percentage difference between futures and spot prices.

        Args:
            futures_price (float): The price of the futures instrument.
            spot_price (float): The spot price of the instrument.

        Returns:
            float: The outright percentage difference.
        """
        outright = (futures_price / spot_price) - 1
        return outright
    

    def pd_pa(rate, t):
        """
        Annualize a rate or percentage difference based on time to maturity.

        Args:
            rate (float): The rate or percentage difference to annualize.
            t (float): The time to maturity in years.

        Returns:
            float: The annualized rate or percentage difference.
        """
        if t == 0:  # Prevent division by zero
            return 0
        pa_rate = rate / t
        return pa_rate
    
    def basis(self, futures_price, spot_price):
        """
        Calculate the difference of a futures contract vs spot price.

        Args:
            futures_price (float): The price of the futures contract.
            spot_price (float): The price of the underlying asset.

        Returns:
            float: The basis of the futures contract.    
        """
        basis = futures_price - spot_price
        return basis
    
    def percent_basis_pa(self, futures_price, spot_price, t):
        """
        Calculate the percent basis of a futures contract vs spot price.

        Args:
            futures_price (float): The price of the futures contract.
            spot_price (float): The price of the underlying asset.
            t (float): The time to maturity in years.

        Returns:
            float: The percent basis of the futures contract per annum.
        """
        basis = self.basis(futures_price, spot_price)
        pa = self.pd_pa(basis, t)
        return pa
    



