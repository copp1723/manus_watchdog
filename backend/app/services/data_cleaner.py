"""
Data cleaning utilities for Watchdog AI.

This module handles cleaning and normalizing CSV data for analysis.
"""
import pandas as pd
import numpy as np
import re
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger("watchdog.data_cleaner")

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and normalize a DataFrame for analysis.
    
    Args:
        df: DataFrame to clean
        
    Returns:
        Cleaned DataFrame
    """
    logger.info(f"Cleaning DataFrame with {len(df)} rows and {len(df.columns)} columns")
    
    # Create a copy to avoid modifying the original
    cleaned_df = df.copy()
    
    # Normalize column names
    cleaned_df = normalize_column_names(cleaned_df)
    
    # Clean monetary values
    monetary_columns = identify_monetary_columns(cleaned_df)
    for column in monetary_columns:
        cleaned_df[column] = clean_monetary_values(cleaned_df[column])
    
    # Clean date columns
    date_columns = identify_date_columns(cleaned_df)
    for column in date_columns:
        cleaned_df[column] = clean_dates(cleaned_df[column])
    
    # Handle missing values
    cleaned_df = handle_missing_values(cleaned_df)
    
    logger.info(f"Cleaning complete. DataFrame has {len(cleaned_df)} rows and {len(cleaned_df.columns)} columns")
    
    return cleaned_df

def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize column names to snake_case.
    
    Args:
        df: DataFrame to process
        
    Returns:
        DataFrame with normalized column names
    """
    # Create a copy to avoid modifying the original
    result = df.copy()
    
    # Function to convert to snake_case
    def to_snake_case(name):
        # Replace spaces and special characters with underscores
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1)
        # Replace multiple spaces/special chars with a single underscore
        s3 = re.sub(r'[^a-zA-Z0-9]', '_', s2)
        # Convert to lowercase and remove leading/trailing underscores
        return re.sub(r'_+', '_', s3).lower().strip('_')
    
    # Apply the function to all column names
    result.columns = [to_snake_case(col) for col in result.columns]
    
    return result

def identify_monetary_columns(df: pd.DataFrame) -> List[str]:
    """
    Identify columns that likely contain monetary values.
    
    Args:
        df: DataFrame to analyze
        
    Returns:
        List of column names that likely contain monetary values
    """
    monetary_columns = []
    
    # Common monetary column name patterns
    monetary_patterns = [
        'price', 'cost', 'revenue', 'sale', 'profit', 'expense', 'gross', 'income',
        'budget', 'payment', 'fee', 'charge', 'amount', 'total'
    ]
    
    # Check each column
    for column in df.columns:
        # Check if column name contains monetary pattern
        if any(pattern in column.lower() for pattern in monetary_patterns):
            monetary_columns.append(column)
            continue
        
        # Check if column contains values with dollar signs or commas
        if df[column].dtype == 'object':
            sample = df[column].dropna().astype(str).head(100)
            if sample.str.contains(r'^\$|\$|\,').any():
                monetary_columns.append(column)
                continue
    
    return monetary_columns

def clean_monetary_values(series: pd.Series) -> pd.Series:
    """
    Clean monetary values by removing currency symbols and commas.
    
    Args:
        series: Series to clean
        
    Returns:
        Cleaned series as float values
    """
    logger.debug(f"Cleaning monetary values for column: {series.name}")
    logger.debug(f"Original data type: {series.dtype}")
    logger.debug(f"Sample original values: {series.head()}")
    
    # Convert to string first to handle mixed types
    str_series = series.astype(str)
    
    # Function to clean individual values
    def clean_value(value):
        if pd.isna(value):
            return np.nan
        
        # Remove currency symbols, commas, and whitespace
        cleaned = re.sub(r'[$,\s]', '', str(value))
        
        # Handle empty strings
        if not cleaned:
            return np.nan
        
        try:
            return float(cleaned)
        except ValueError:
            logger.warning(f"Could not convert value to float: {value}")
            return np.nan
    
    # Apply the cleaning function
    result = str_series.apply(clean_value)
    logger.debug(f"Cleaned data type: {result.dtype}")
    logger.debug(f"Sample cleaned values: {result.head()}")
    logger.debug(f"Count of non-null values: {result.count()}")
    logger.debug(f"Count of zero values: {(result == 0).sum()}")
    return result

def identify_date_columns(df: pd.DataFrame) -> List[str]:
    """
    Identify columns that likely contain date values.
    
    Args:
        df: DataFrame to analyze
        
    Returns:
        List of column names that likely contain date values
    """
    date_columns = []
    
    # Common date column name patterns
    date_patterns = [
        'date', 'day', 'month', 'year', 'time', 'created', 'updated',
        'timestamp', 'sold', 'purchased', 'closed'
    ]
    
    # Check each column
    for column in df.columns:
        # Check if column name contains date pattern
        if any(pattern in column.lower() for pattern in date_patterns):
            date_columns.append(column)
            continue
        
        # Check if column can be converted to datetime
        if df[column].dtype == 'object':
            sample = df[column].dropna().head(10)
            try:
                pd.to_datetime(sample)
                date_columns.append(column)
            except:
                pass
    
    return date_columns

def clean_dates(series: pd.Series) -> pd.Series:
    """
    Clean date values by converting to datetime.
    
    Args:
        series: Series to clean
        
    Returns:
        Cleaned series as datetime values
    """
    try:
        # Try to convert to datetime with automatic format detection
        return pd.to_datetime(series, errors='coerce')
    except:
        # If conversion fails, return the original series
        return series

def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handle missing values in the DataFrame.
    
    Args:
        df: DataFrame to process
        
    Returns:
        DataFrame with handled missing values
    """
    logger.debug("Handling missing values")
    logger.debug(f"Original DataFrame shape: {df.shape}")
    logger.debug("Missing value counts by column:")
    for col in df.columns:
        missing = df[col].isna().sum()
        if missing > 0:
            logger.debug(f"{col}: {missing} missing values")
    
    # Create a copy to avoid modifying the original
    result = df.copy()
    
    # For numeric columns, replace NaN with 0
    numeric_columns = result.select_dtypes(include=['number']).columns
    logger.debug(f"Numeric columns: {numeric_columns.tolist()}")
    result[numeric_columns] = result[numeric_columns].fillna(0)
    
    # For string columns, replace NaN with empty string
    string_columns = result.select_dtypes(include=['object']).columns
    logger.debug(f"String columns: {string_columns.tolist()}")
    result[string_columns] = result[string_columns].fillna('')
    
    logger.debug("Missing values after handling:")
    for col in result.columns:
        missing = result[col].isna().sum()
        if missing > 0:
            logger.debug(f"{col}: {missing} missing values")
    
    return result
