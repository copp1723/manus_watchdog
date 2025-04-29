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
    logger.debug("Identifying monetary columns")
    monetary_columns = []

    # Refined monetary column name patterns (more specific)
    monetary_patterns = [
        r'(^|_)price($|_)', r'(^|_)profit($|_)', r'(^|_)gross($|_)', r'(^|_)expense($|_)', r'(^|_)cost($|_)',
        r'(^|_)revenue($|_)', r'(^|_)sale($|_)', r'(^|_)amount($|_)', r'(^|_)total($|_)', r'(^|_)fee($|_)',
        r'(^|_)charge($|_)', r'(^|_)budget($|_)', r'(^|_)payment($|_)', r'(^|_)income($|_)'
    ]
    # Exclude columns with these patterns
    exclude_patterns = [r'name', r'rep', r'id', r'number']

    for column in df.columns:
        column_lower = column.lower()
        logger.debug(f"Checking column: {column}")

        # Skip if column is already numeric
        if pd.api.types.is_numeric_dtype(df[column]):
            logger.debug(f"Skipping {column} as it is already numeric")
            continue

        # Exclude columns with certain patterns
        if any(re.search(pat, column_lower) for pat in exclude_patterns):
            logger.debug(f"Skipping {column} due to exclusion pattern")
            continue

        # Check if column name matches monetary pattern
        if any(re.search(pat, column_lower) for pat in monetary_patterns):
            logger.debug(f"Adding {column} based on name pattern")
            monetary_columns.append(column)
            continue

        # Check if column contains values with dollar signs or commas
        if df[column].dtype == 'object':
            sample = df[column].dropna().astype(str).head(100)
            if sample.str.contains(r'\$|,').any():
                logger.debug(f"Adding {column} based on value format")
                monetary_columns.append(column)
                continue

    logger.debug(f"Identified monetary columns: {monetary_columns}")
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
    logger.debug(f"Sample original values:\n{series.head()}")
    
    # Convert to string and remove $ and , characters
    cleaned_series = series.astype(str).str.replace(r'[$,]', '', regex=True)
    logger.debug(f"Series after removing $ and , characters:\n{cleaned_series.head()}")
    
    # Convert to numeric values
    numeric_series = pd.to_numeric(cleaned_series, errors='coerce')
    logger.debug(f"Column '{series.name}' dtype after cleaning: {numeric_series.dtype}")
    logger.debug(f"Monetary values after cleaning attempt (Head):\n{numeric_series.head()}")
    
    # Log additional diagnostics
    logger.debug(f"Count of non-null values: {numeric_series.count()}")
    logger.debug(f"Count of zero values: {(numeric_series == 0).sum()}")
    logger.debug(f"Value distribution:\n{numeric_series.value_counts().head()}")
    
    return numeric_series

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
    Clean date values by converting to datetime, with special handling for certain columns.
    
    Args:
        series: Series to clean
        
    Returns:
        Cleaned series as datetime values, or original/numeric for special cases
    """
    col_name = series.name.lower() if series.name else ""
    logger.debug(f"Cleaning dates for column: {series.name}")
    logger.debug(f"Original data type: {series.dtype}")
    logger.debug(f"Sample original values:\n{series.head()}")

    # Special case: days_to_close should remain numeric
    if 'days_to_close' in col_name:
        logger.debug("Skipping date cleaning for days_to_close (should remain numeric)")
        return pd.to_numeric(series, errors='coerce')

    # Special case: vehicle_year should be parsed as year only
    if 'vehicle_year' in col_name:
        try:
            cleaned_series = pd.to_datetime(series, format='%Y', errors='coerce')
            logger.debug(f"Cleaned vehicle_year as datetime: {cleaned_series.head()}")
            return cleaned_series
        except Exception as e:
            logger.error(f"Error cleaning vehicle_year: {str(e)}")
            return series

    # Do not attempt to clean monetary columns as dates
    if 'sold_price' in col_name or 'price' in col_name:
        logger.debug("Skipping date cleaning for price columns")
        return series

    try:
        # Try to convert to datetime with automatic format detection
        cleaned_series = pd.to_datetime(series, errors='coerce')
        logger.debug(f"Cleaned data type: {cleaned_series.dtype}")
        logger.debug(f"Sample cleaned values:\n{cleaned_series.head()}")
        logger.debug(f"Count of non-null values: {cleaned_series.count()}")
        logger.debug(f"Value distribution:\n{cleaned_series.value_counts().head()}")
        return cleaned_series
    except Exception as e:
        logger.error(f"Error cleaning dates: {str(e)}")
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
