import pandas as pd

def load_csv(file_path):
    """Load a CSV file into a DataFrame."""
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        return pd.DataFrame()

def save_csv(dataframe, file_path):
    """Save a DataFrame to a CSV file."""
    dataframe.to_csv(file_path, index=False)