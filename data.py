import pandas as pd
import asyncio
import arcticdb as adb
import os
from threading import Lock
import logging

# Setup basic configuration for logging
logging.basicConfig(level=logging.INFO)

class DataManagerConfig:
    ARCTIC_CONNECTION_STRING = "lmdb:///path/to/lildata?map_size=2GB"

class DataManager:
    _instance = None  # Singleton instance
    _lock = Lock()  # Lock for thread-safe operations

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataManager, cls).__new__(cls)
            cls._instance.ac = adb.Arctic(DataManagerConfig.ARCTIC_CONNECTION_STRING)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):  # Prevent reinitialization
            self.initialized = True
            self.lib = None
            self.shared_df = pd.DataFrame()  # Initialize the shared DataFrame
            self.data_df = pd.DataFrame()  # Initialize as an empty DataFrame
            self.instrument_names = []  # Initialize as an empty list
            self.data_fields = []  # Initialize as an empty list

    async def ensure_library_exists(self, library_name):
        existing_libraries = await asyncio.get_running_loop().run_in_executor(None, self.ac.list_libraries)
        if library_name not in existing_libraries:
            await asyncio.get_running_loop().run_in_executor(None, self.ac.create_library, library_name)
        self.lib = self.ac[library_name]
        logging.info(f"Library {library_name} accessed or created.")

    async def write_data_in_arctic(self, library_name, key, dataframe):
        """Store data in the specified Arctic library under the given key."""
        try:
            library = self.ac[library_name]  # Access the specific library
            if not dataframe.empty:
                await asyncio.get_running_loop().run_in_executor(None, library.write, key, dataframe)
                logging.info(f"Data stored under key {key} in library {library_name}.")
            else:
                logging.warning(f"No data to store under key {key} in library {library_name}.")
        except Exception as e:
            logging.error(f"Error storing data under key {key} in library {library_name}: {e}")
            raise

    async def read_data_from_arctic(self, library_name, key):
            """Read data from the specified Arctic library using the given key."""
            try:
                library = self.ac[library_name]  # Access the specific library
                data = await asyncio.get_running_loop().run_in_executor(None, library.read, key)
                logging.info(f"Data retrieved under key {key} from library {library_name}.")
                return data
            except Exception as e:
                logging.error(f"Error reading data under key {key} from library {library_name}: {e}")
                return pd.DataFrame()  # Return an empty DataFrame in case of error







    def update_shared_df(self, new_data):
        with self._lock:
            asyncio.run(self.store_data_in_arctic('data_df', new_data))
            print(new_data)
            logging.info("Shared DataFrame updated and stored in ArcticDB.")

    def get_shared_df(self):
        with self._lock:
            return asyncio.run(self.read_data_from_arctic('data_df'))


    async def setup_riskuser_library(self):
        """Ensure the 'riskuser' library is ready and structured for 'user.risk' data."""
        await self.ensure_library_exists('riskuser')
        # Additional setup can be done here if needed, such as configuring indexes or metadata

    async def store_user_risk_data(self, data):
        """Store 'user.risk' data into the 'riskuser' library."""
        df = pd.DataFrame([data])  # Assuming 'data' is a dictionary
        df.index = pd.date_range(pd.Timestamp.now(), periods=1)  # Set index if needed
        await self.store_data_in_arctic('riskuser', 'user_risk', df)  # Corrected to pass three arguments
        print("User risk data stored.")


    async def read_user_risk_data(self):
        """Read 'user.risk' data from the 'riskuser' library."""
        versioned_item = await self.read_data_from_arctic('riskuser', 'user_risk')
        if versioned_item and hasattr(versioned_item, 'data'):
            data_df = versioned_item.data  # Access the DataFrame from the VersionedItem
            print("Retrieved user risk data:")
            print(data_df)  # Print the DataFrame directly
            print(f"Data version: {versioned_item.version}")  # Optionally print the version
        else:
            print("No data found or invalid data format.")


    async def initialize_array_with_data(self):
        logging.info("Initializing data arrays...")
        await self.ensure_library_exists('lildata')
        await self.ensure_library_exists('instrument_names')
        logging.info("Data array ready to receive data from WebSocket feed.")

    async def store_instrument_data(self, data):
        df = pd.DataFrame([data])
        df.index = pd.date_range(pd.Timestamp.now(), periods=1)
        await asyncio.get_running_loop().run_in_executor(None, self.lib.write, 'instrument_data', df)
        logging.info("Instrument data stored in ArcticDB.")

