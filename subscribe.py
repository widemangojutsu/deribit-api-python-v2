def send_heartbeat(interval):
    '''
    Sends a heartbeat message to keep the WebSocket connection alive.
    @Deribit Parameters:
    - interval: The frequency in seconds at which the server should send heartbeat messages.
    '''
    return {
        "jsonrpc": "2.0",
        "id": 44,
        "method": "public/set_heartbeat",
        "params": {
            "interval": interval
        }
    }


def public_test():
    return {
        "jsonrpc": "2.0",
        "id": 44,
        "method": "public/test",
        "params": {}
    }


def subscribe(channels):
    '''
    Subscribes to one or more channels for receiving real-time updates.
    @Deribit Parameters:
    - channels: A list of channel names to subscribe to.
    '''
    return {
        "jsonrpc": "2.0",
        "id": 45,
        "method": "public/subscribe",
        "params": {
            "channels": channels
        }
    }

def unsubscribe(channels):
    '''
    Unsubscribes from one or more previously subscribed channels.
    @Deribit Parameters:
    - channels: A list of channel names to unsubscribe from.
    '''
    return {
        "jsonrpc": "2.0",
        "id": 46,
        "method": "public/unsubscribe",
        "params": {
            "channels": channels
        }
    }

def priv_subscribe(channels):
    '''
    Subscribes to one or more private channels for receiving user-specific updates.
    @Deribit Parameters:
    - channels: A list of private channel names to subscribe to.
    '''
    return {
        "jsonrpc": "2.0",
        "id": 47,
        "method": "private/subscribe",
        "params": {
            "channels": channels
        }
    }

def priv_unsubscribe(channels):
    '''
    Unsubscribes from one or more previously subscribed private channels.
    @Deribit Parameters:
    - channels: A list of private channel names to unsubscribe from.
    '''
    return {
        "jsonrpc": "2.0",
        "id": 48,
        "method": "private/unsubscribe",
        "params": {
            "channels": channels
        }
    }

# The following methods would follow a similar pattern, with descriptions tailored to each specific function.
# For example:

def get_contract_size(instrument_name):
    '''
    Retrieves the contract size for a specified instrument.
    @Deribit Parameters:
    - instrument_name: The name of the instrument to query the contract size for.
    '''
    return {
        "jsonrpc": "2.0",
        "id": 49,
        "method": "public/get_contract_size",
        "params": {
            "instrument_name": instrument_name
        }
    }

def get_funding_chart_data(instrument_name, length):
    '''
    Returns a list of dictionaries containing the funding chart data for the specified instrument.
    length accepts 8h, 24h, 1m for month
    '''

    return {
        "jsonrpc": "2.0",
        "id": 50,  # Example ID
        "method": "public/get_funding_chart_data",
        "params": {
            "instrument_name": instrument_name,
            "length": length
        }
    }

def get_future_instruments(currency, future, expired):
    '''
    Currency string BTC, ETH, USDC, USDT, EURR
    kind string future option spot future_combo option_combo
    expired true or false set to true if you want to get only expired instruments
    '''
    return {
        "jsonrpc": "2.0",
        "id": 51,  # Example ID
        "method": "public/get_instruments",
        "params": {
            "currency": currency,
            "kind": future,
            "expired": expired
        }
    }

def get_option_instruments(currency, option, expired):
    '''
    Currency string BTC, ETH, USDC, USDT, EURR
    kind string future option spot future_combo option_combo
    expired true or false set to true if you want to get only expired instruments
    '''
    return {
        "jsonrpc": "2.0",
        "id": 52,  # Example ID
        "method": "public/get_instruments",
        "params": {
            "currency": currency,
            "kind": option,
            "expired": expired
        }
    }

def get_spot_instruments(currency, spot, expired):
    '''
    Currency string BTC, ETH, USDC, USDT, EURR
    kind string future option spot future_combo option_combo
    expired true or false set to true if you want to get only expired instruments
    '''
    return {
        "jsonrpc": "2.0",
        "id": 53,  # Example ID
        "method": "public/get_instruments",
        "params": {
            "currency": currency,
            "kind": spot,
            "expired": expired
        }
    }

def get_instrument(instrument_name):
    '''Retrieves information about instrument'''
    return {
        "jsonrpc": "2.0",
        "id": 54,  # Example ID
        "method": "public/get_instrument",
        "params": {
            "instrument_name": instrument_name
        }
    }


def get_chart_data(instrument_name, length):
    '''
    instrument_name	true	string		Instrument name
    start_timestamp	true	integer		The earliest timestamp to return result from (milliseconds since the UNIX epoch)
    end_timestamp	true	integer		The most recent timestamp to return result from (milliseconds since the UNIX epoch)
    resolution	true		1, 3, 5, 10, 15, 30, 60, 120, 180, 360, 720, 1D	The resolution of the data to return
    '''
    return {
        "jsonrpc": "2.0",
        "id": 54,  # Example ID
        "method": "public/get_chart_data",
        "params": {
            "instrument_name": instrument_name,
            "length": length
        }
    }

def ticker(instrument_name):
    '''
    instrument_name	true	string		Instrument name
    '''
    return {
        "jsonrpc": "2.0",
        "id": 55,  # Example ID
        "method": "public/ticker",
        "params": {
            "instrument_name": instrument_name
        }
    }

def get_orderbook(instrument_name, depth):
    return {
        "jsonrpc": "2.0",
        "method": "public/subscribe",
        "params": {
            "channels": [f"book.{instrument_name}.none.{depth}.100ms"]
        }
    }


def get_orderbook_by_insturment_id(instrument_id, depth):
    '''
    instrument_id	true	integer		Instrument ID
    depth	true	integer		The number of price levels to include in the order book
    '''
    return {
        "jsonrpc": "2.0",
        "id": 56,  # Example ID
        "method": "public/get_orderbook_by_instrument_id",
        "params": {
            "instrument_id": instrument_id,
            "depth": depth
        }
    }

def get_book_summary_by_instrument(instrument_name):
    '''
    instrument_name	true	string		Instrument name
    '''
    return {
        "jsonrpc": "2.0",
        "id": 57,  # Example ID
        "method": "public/get_book_summary_by_instrument",
        "params": {
            "instrument_name": instrument_name
        }
    }