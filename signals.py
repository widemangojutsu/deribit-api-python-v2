import pandas as pd

class SignalProcessor:
    def __init__(self, data_manager):
        self.data_manager = data_manager

    def calculate_sma(self, data, window):
        return data['price'].rolling(window=window).mean()

    def generate_signals(self):
        """
        Generate trading signals based on a simple moving average (SMA) crossover strategy.
        """
        df = self.data_data_manager.get_data()
        df['SMA_short'] = self.calculate_sma(df, 10)
        df['SMA_long'] = self.calculate_sma(df, 30)
        df['signal'] = (df['SMA_short'] > df['SMA_long']).astype(int).diff().fillna(0)
        return df[df['signal'] != 0]