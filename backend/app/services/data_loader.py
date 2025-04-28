"""
Data loading utilities for Watchdog AI.

This module handles loading and initial validation of CSV files.
"""
import pandas as pd
import logging
from typing import Dict, Any, List, Optional
import os

logger = logging.getLogger("watchdog.data_loader")

def load_csv_file(file_path: str) -> pd.DataFrame:
    """
    Load a CSV file and perform initial validation.
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        DataFrame containing the CSV data
        
    Raises:
        ValueError: If the file is empty or invalid
        FileNotFoundError: If the file doesn't exist
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    logger.info(f"Loading CSV file: {file_path}")
    
    try:
        # Try to infer the delimiter
        with open(file_path, 'r', encoding='utf-8') as f:
            sample = f.read(4096)
        
        # Count occurrences of common delimiters
        delimiters = [',', ';', '\t', '|']
        counts = {d: sample.count(d) for d in delimiters}
        delimiter = max(counts, key=counts.get)
        
        # Load the CSV with the inferred delimiter
        df = pd.read_csv(file_path, delimiter=delimiter)
        
        # Basic validation
        if df.empty:
            raise ValueError("The CSV file is empty")
        
        if len(df.columns) < 2:
            raise ValueError("The CSV file must have at least two columns")
        
        logger.info(f"Successfully loaded CSV with {len(df)} rows and {len(df.columns)} columns")
        
        return df
    
    except pd.errors.ParserError as e:
        logger.error(f"Error parsing CSV file: {e}")
        raise ValueError(f"Invalid CSV format: {str(e)}")
    
    except Exception as e:
        logger.error(f"Unexpected error loading CSV: {e}")
        raise

def get_column_types(df: pd.DataFrame) -> Dict[str, str]:
    """
    Determine the data type of each column in the DataFrame.
    
    Args:
        df: DataFrame to analyze
        
    Returns:
        Dictionary mapping column names to data types
    """
    column_types = {}
    
    for column in df.columns:
        # Check if column contains numeric values
        if pd.api.types.is_numeric_dtype(df[column]):
            # Check if it's an integer or float
            if df[column].dropna().apply(lambda x: x == int(x)).all():
                column_types[column] = "integer"
            else:
                column_types[column] = "float"
        
        # Check if column contains datetime values
        elif pd.api.types.is_datetime64_dtype(df[column]):
            column_types[column] = "datetime"
        
        # Check if column might be a date string
        elif df[column].dtype == 'object':
            # Sample non-null values
            sample = df[column].dropna().head(10)
            try:
                pd.to_datetime(sample)
                column_types[column] = "date_string"
            except:
                column_types[column] = "string"
        
        # Default to string
        else:
            column_types[column] = "string"
    
    return column_types

def get_column_statistics(df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
    """
    Calculate basic statistics for each column in the DataFrame.
    
    Args:
        df: DataFrame to analyze
        
    Returns:
        Dictionary mapping column names to statistics
    """
    stats = {}
    column_types = get_column_types(df)
    
    for column in df.columns:
        column_stats = {
            "type": column_types[column],
            "missing_count": df[column].isna().sum(),
            "missing_percentage": round(df[column].isna().mean() * 100, 2),
            "unique_count": df[column].nunique()
        }
        
        # Add type-specific statistics
        if column_types[column] in ["integer", "float"]:
            numeric_stats = {
                "min": df[column].min() if not df[column].empty else None,
                "max": df[column].max() if not df[column].empty else None,
                "mean": df[column].mean() if not df[column].empty else None,
                "median": df[column].median() if not df[column].empty else None,
                "std": df[column].std() if not df[column].empty else None
            }
            column_stats.update(numeric_stats)
        
        elif column_types[column] in ["date_string", "datetime"]:
            try:
                date_series = pd.to_datetime(df[column])
                date_stats = {
                    "min_date": date_series.min().strftime("%Y-%m-%d") if not date_series.empty else None,
                    "max_date": date_series.max().strftime("%Y-%m-%d") if not date_series.empty else None,
                    "date_range_days": (date_series.max() - date_series.min()).days if not date_series.empty else None
                }
                column_stats.update(date_stats)
            except:
                # If conversion fails, skip date-specific stats
                pass
        
        elif column_types[column] == "string":
            # Get top values for categorical columns
            value_counts = df[column].value_counts().head(5).to_dict()
            column_stats["top_values"] = value_counts
        
        stats[column] = column_stats
    
    return stats

def detect_dealership_data_format(df: pd.DataFrame) -> str:
    """
    Detect which format of dealership data is being used.
    
    Args:
        df: DataFrame to analyze
        
    Returns:
        String indicating the detected format: "simple", "detailed", or "unknown"
    """
    # Check column names to determine format
    columns = set(df.columns.str.lower())
    
    # Simple format indicators (from watchdog test data.csv)
    simple_indicators = {"lead_source", "listing_price", "sold_price", "profit", "sales_rep_name"}
    
    # Detailed format indicators (from ROI Calc - Sold Log.csv)
    detailed_indicators = {"globalcustomerid", "autoleadid", "soldstatus", "solddate", "leadsource"}
    
    # Check for matches
    simple_match = len(simple_indicators.intersection(columns)) / len(simple_indicators)
    detailed_match = len(detailed_indicators.intersection(columns)) / len(detailed_indicators)
    
    if simple_match > 0.6:
        return "simple"
    elif detailed_match > 0.6:
        return "detailed"
    else:
        return "unknown"
