import requests
import csv
from datetime import datetime, timedelta
import os
from yaml import load, Loader

# Load parameters from parameters.yaml
with open('parameters.yaml', 'r') as file:
    params = load(file, Loader=Loader)

currency = params['currency']

def should_fetch_new_data():
    """Determine if new data should be fetched based on the pulldate in the CSV."""
    if not os.path.exists('instrument_name.csv'):
        print("No instrument_name.csv file found. Fetching new data.")
        return True
    with open('instrument_name.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        try:
            last_row = next(reader)  # Assuming pulldate is in the first row
            last_pulldate = datetime.strptime(last_row['pulldate'], '%Y%m%d%H%M')
            if datetime.now() - last_pulldate > timedelta(hours=24):
                print("Data is older than 24 hours. Fetching new data.")
                return True
        except StopIteration:
            print("CSV file is empty. Fetching new data.")
            return True  # File is empty, fetch new data
    return False

def fetch_instruments():
    kinds = ["future", "spot"]  # List of kinds to fetch
    url = "https://deribit.com/api/v2/public/get_instruments"
    
    # Open the CSV file once and write headers
    with open('instrument_name.csv', 'w', newline='') as csvfile:
        fieldnames = [
            'kind', 'instrument_name', 'settlement_period', 'strike', 'option_type', 'pulldate',
            'contract_size', 'create_timestamp', 'expiration_timestamp', 'instrument_id', 'instrument_type',
            'maker_commission', 'min_trade_amount', 'taker_commission', 'tick_size'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for kind in kinds:
            params = {
                "currency": currency,
                "kind": kind  # Use the kind from the list
            }
            response = requests.get(url, params=params, headers={"Content-Type": "application/json"})
            data = response.json()

            # Proceed only if 'result' key exists
            if 'result' in data:
                pulldate = datetime.now().strftime('%Y%m%d%H%M')
                for instrument in data['result']:
                    writer.writerow({
                        'kind': kind,
                        'instrument_name': instrument['instrument_name'],
                        'settlement_period': instrument.get('settlement_period', 'N/A'),
                        'strike': instrument.get('strike', 'N/A'),
                        'option_type': instrument.get('option_type', 'N/A'),
                        'pulldate': pulldate,
                        'contract_size': instrument.get('contract_size', 'N/A'),
                        'create_timestamp': instrument.get('creation_timestamp', 'N/A'),
                        'expiration_timestamp': instrument.get('expiration_timestamp', 'N/A'),
                        'instrument_id': instrument.get('instrument_id', 'N/A'),
                        'instrument_type': instrument.get('instrument_type', 'N/A'),
                        'maker_commission': instrument.get('maker_commission', 'N/A'),
                        'min_trade_amount': instrument.get('min_trade_amount', 'N/A'),
                        'taker_commission': instrument.get('taker_commission', 'N/A'),
                        'tick_size': instrument.get('tick_size', 'N/A')
                    })
            else:
                print(f"Error or unexpected response structure for {kind}:", data)

def main():
    if should_fetch_new_data():
        fetch_instruments()
    else:
        print("Data is up-to-date. No need to fetch new instruments.")

if __name__ == "__main__":
    main()