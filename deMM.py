import requests

# Base URL for DLN API
BASE_URL = "https://api.dln.trade/v1.0"

def get_quote(src_chain_id, src_token_in, src_token_in_amount, dst_chain_id, dst_token_out, prepend_expenses, affiliate_fee):
    """Get a trading quote from the DLN API."""
    url = f"{BASE_URL}/dln/order/quote"
    params = {
        "srcChainId": src_chain_id,
        "srcChainTokenIn": src_token_in,
        "srcChainTokenInAmount": src_token_in_amount,
        "dstChainId": dst_chain_id,
        "dstChainTokenOut": dst_token_out,
        "prependOperatingExpenses": prepend_expenses,
        "affiliateFeePercent": affiliate_fee
    }
    response = requests.get(url, params=params)
    return response.json()

def create_order_transaction(data):
    """Create an order on the DLN API."""
    url = f"{BASE_URL}/dln/order/create-tx"
    response = requests.get(url, params=data)
    return response.json()

def track_order_status(order_id):
    """Track the status of an order."""
    url = f"{BASE_URL}/api/Orders/{order_id}"
    response = requests.get(url)
    return response.json()

# Example usage
if __name__ == "__main__":
    # Example parameters for getting a quote
    quote = get_quote(
        src_chain_id=42161,
        src_token_in="0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
        src_token_in_amount="57",
        dst_chain_id=8453,
        dst_token_out="0x833589fcd6edb6e08f4c7c32d4f71b54bda02913",
        prepend_expenses=True,
        affiliate_fee=0.01
    )
    print("Quote:", quote)

    # Assuming you have the necessary data from the quote to create an order
    order_data = {
        "srcChainId": 42161,
        "srcChainTokenIn": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
        "srcChainTokenInAmount": "57",
        "dstChainId": 8453,
        "dstChainTokenOut": "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913",
        "dstChainTokenOutAmount": "57",
        "dstChainTokenOutRecipient": "0xeaae3d91c8c2090d54f47632a4333f62b685e085",
        "srcChainOrderAuthorityAddress": "0xeaae3d91c8c2090d54f47632a4333f62b685e085",
        "dstChainOrderAuthorityAddress": "0xeaae3d91c8c2090d54f47632a4333f62b685e085",
        "affiliateFeePercent": 0.01,
        "affiliateFeeRecipient": "0xeaae3d91c8c2090d54f47632a4333f62b685e085"
    }
    order = create_order_transaction(order_data)
    print("Order Transaction:", order)

    # Track the status of an order
    order_status = track_order_status("0x9ee6c3d0aa68a7504e619b02df7c71539d0ce10e27f593bf8604b62e51955a01")
    print("Order Status:", order_status)