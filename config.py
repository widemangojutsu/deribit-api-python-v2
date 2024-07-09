from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access environment variables and set them as constants
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
DERIBIT_URL = os.getenv('DERIBIT_URL')
HTX_WS_URL = os.getenv('HUOBI_WS_URL')
HTX_API_KEY = os.getenv('HUOBI_ID')
HTX_SECRET_KEY = os.getenv('HUOBI_SECRET')
KRAKEN_ID = os.getenv('KRAKEN_ID')
KRAKEN_SECRET = os.getenv('KRAKEN_SECRET')
