import pandas as pd
import os

def load_data(filepath):
    """Load CSV data into a pandas DataFrame."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    df = pd.read_csv(filepath)
    return df

def check_missing_values(df):
    """Return a Series with count of missing values per column."""
    return df.isnull().sum()

def check_duplicates(df):
    """Return the number of duplicate rows."""
    return df.duplicated().sum()

def clean_data(df):
    """Clean the healthcare dataset.
    
    - Remove duplicates
    - Standardize text columns (strip, title case)
    - Convert date columns to datetime
    - Ensure Billing Amount is numeric
    """
    df_clean = df.copy()
    
    text_cols = ['Name', 'Gender', 'Blood Type', 'Medical Condition', 
                 'Doctor', 'Hospital', 'Insurance Provider', 
                 'Admission Type', 'Medication', 'Test Results']
    for col in text_cols:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].astype(str).str.strip().str.title()
    
    if 'Date of Admission' in df_clean.columns:
        df_clean['Date of Admission'] = pd.to_datetime(
            df_clean['Date of Admission'], format='%d-%m-%Y', errors='coerce'
        )
    if 'Discharge Date' in df_clean.columns:
        df_clean['Discharge Date'] = pd.to_datetime(
            df_clean['Discharge Date'], format='%d-%m-%Y', errors='coerce'
        )
    if 'Billing Amount' in df_clean.columns:
        df_clean['Billing Amount'] = pd.to_numeric(
            df_clean['Billing Amount'], errors='coerce'
        )
    
    df_clean = df_clean.drop_duplicates()
    return df_clean

def save_cleaned_data(df, output_path):
    """Save cleaned DataFrame to CSV."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    return output_path

def load_and_clean(input_path, output_path=None):
    """Load, clean, and optionally save data. Returns cleaned DataFrame."""
    df = load_data(input_path)
    df_clean = clean_data(df)
    if output_path:
        save_cleaned_data(df_clean, output_path)
    return df_clean
