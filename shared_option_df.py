import pandas as pd

# Initialize the shared DataFrame for options globally
shared_options_df = pd.DataFrame()

def initialize_shared_options_df(data_df, option_columns):
    """Initialize the shared DataFrame with option columns from the main DataFrame."""
    global shared_options_df
    # Check if data_df is not empty and contains the required columns
    if not data_df.empty and all(col in data_df.columns for col in option_columns):
        shared_options_df = data_df[option_columns].copy()
    else:
        print("Data DataFrame is empty or missing required columns. No options data to initialize.")
        # Optionally, initialize with empty columns if needed
        shared_options_df = pd.DataFrame(columns=option_columns)

def update_shared_options_df(new_data):
    global shared_options_df
    # Assume new_data is a DataFrame with the same structure as options_df
    shared_options_df = pd.concat([shared_options_df, new_data])

def get_shared_options_df():
    """Get the shared options DataFrame."""
    global shared_options_df
    return shared_options_df