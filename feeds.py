import csv

def get_ticker_info(instrument_name, interval):
    """Returns best bid ask price and amount, iv, funding for perps, greeks, funding 8h, rates"""
    return [f"ticker.{instrument_name}.{interval}"]

def get_dbit_index_price(index_name):
    """Returns DBIT index price"""
    return [f"deribit_price_statistics.{index_name}"]

def get_user_porfolio(currency):
    """Returns user portfolio information"""
    return [f"user.portfolio.{currency}"]

def quote_by_instrument(instrument_name):
    """Generates quote channel names dynamically based on the instrument name."""
    return [f"quote.{instrument_name}"]

def get_instrument_names_from_csv():
    """Reads the instrument names from the CSV file."""
    instrument_names = []
    try:
        with open('instrument_name.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                instrument_names.append(row['instrument_name'])
    except FileNotFoundError:
        print("CSV file not found. Ensure that 'instrument_name.csv' exists.")
    return instrument_names

def channel_generator(instrument_names):
    """Generates a list of all channel names for the feeds using the provided list of instrument names."""
    all_channels = []
    for name in instrument_names:
        # all_channels.extend(get_user_porfolio(currency='BTC'))
        # all_channels.extend(get_dbit_index_price(index_name='BTC_USD'))
        # Assuming a fixed interval for simplicity, modify as needed
        all_channels.extend(get_ticker_info(name, interval='raw'))  # Example interval '1m'
    return all_channels