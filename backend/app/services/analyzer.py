"""
Data analysis utilities for Watchdog AI.

This module handles analyzing dealership data to extract insights.
"""
import pandas as pd
import numpy as np
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger("watchdog.analyzer")

def analyze_data(df: pd.DataFrame, intent: str = "general_analysis") -> Dict[str, Any]:
    """
    Analyze data based on the specified intent.
    
    Args:
        df: DataFrame to analyze
        intent: Analysis intent (e.g., 'sales_analysis', 'profit_analysis')
        
    Returns:
        Dictionary containing analysis results
    """
    logger.info(f"Analyzing data with intent: {intent}")
    
    # Determine which analysis to run based on intent
    if intent == "sales_analysis":
        return analyze_sales(df)
    elif intent == "profit_analysis":
        return analyze_profit(df)
    elif intent == "rep_performance":
        return analyze_rep_performance(df)
    elif intent == "lead_source_analysis":
        return analyze_lead_sources(df)
    elif intent == "vehicle_analysis":
        return analyze_vehicles(df)
    else:
        # Default to general analysis
        return analyze_general(df)

def analyze_general(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Perform general analysis of the data.
    
    Args:
        df: DataFrame to analyze
        
    Returns:
        Dictionary containing analysis results
    """
    results = {
        "summary": {
            "total_records": len(df),
            "date_range": get_date_range(df),
            "total_sales": get_total_sales(df),
            "total_profit": get_total_profit(df),
            "average_profit": get_average_profit(df)
        },
        "top_metrics": []
    }
    
    # Add top sales rep
    top_rep = get_top_sales_rep(df)
    if top_rep:
        results["top_metrics"].append({
            "title": "Top Sales Rep",
            "value": top_rep["name"],
            "metric": f"${top_rep['total_profit']:,.2f}",
            "description": f"Top performing sales representative by profit"
        })
    
    # Add top lead source
    top_source = get_top_lead_source(df)
    if top_source:
        results["top_metrics"].append({
            "title": "Top Lead Source",
            "value": top_source["name"],
            "metric": f"${top_source['total_profit']:,.2f}",
            "description": f"Most profitable lead source"
        })
    
    # Add top vehicle
    top_vehicle = get_top_vehicle(df)
    if top_vehicle:
        results["top_metrics"].append({
            "title": "Top Vehicle",
            "value": top_vehicle["name"],
            "metric": f"${top_vehicle['total_profit']:,.2f}",
            "description": f"Most profitable vehicle model"
        })
    
    # Add chart data for profit by rep
    results["chart_data"] = get_profit_by_rep_chart_data(df)
    results["chart_type"] = "bar"
    
    return results

def analyze_sales(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze sales data.
    
    Args:
        df: DataFrame to analyze
        
    Returns:
        Dictionary containing analysis results
    """
    results = {
        "summary": {
            "total_sales": get_total_sales(df),
            "average_sale_price": get_average_sale_price(df),
            "highest_sale": get_highest_sale(df),
            "lowest_sale": get_lowest_sale(df)
        },
        "sales_by_rep": get_sales_by_rep(df),
        "sales_by_month": get_sales_by_month(df) if has_date_column(df) else None,
        "sales_by_vehicle_type": get_sales_by_vehicle_type(df)
    }
    
    # Add chart data
    results["chart_data"] = get_sales_by_rep_chart_data(df)
    results["chart_type"] = "bar"
    
    return results

def analyze_profit(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze profit data.
    
    Args:
        df: DataFrame to analyze
        
    Returns:
        Dictionary containing analysis results
    """
    results = {
        "summary": {
            "total_profit": get_total_profit(df),
            "average_profit": get_average_profit(df),
            "highest_profit_sale": get_highest_profit_sale(df),
            "profit_margin": get_profit_margin(df)
        },
        "profit_by_rep": get_profit_by_rep(df),
        "profit_by_lead_source": get_profit_by_lead_source(df),
        "profit_by_vehicle_type": get_profit_by_vehicle_type(df)
    }
    
    # Add chart data
    results["chart_data"] = get_profit_by_rep_chart_data(df)
    results["chart_type"] = "bar"
    
    return results

def analyze_rep_performance(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze sales representative performance.
    
    Args:
        df: DataFrame to analyze
        
    Returns:
        Dictionary containing analysis results
    """
    results = {
        "summary": {
            "total_reps": get_total_reps(df),
            "top_rep": get_top_sales_rep(df),
            "average_profit_per_rep": get_average_profit_per_rep(df)
        },
        "rep_leaderboard": get_rep_leaderboard(df),
        "rep_metrics": get_rep_metrics(df)
    }
    
    # Add chart data
    results["chart_data"] = get_rep_performance_chart_data(df)
    results["chart_type"] = "bar"
    
    return results

def analyze_lead_sources(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze lead source effectiveness.
    
    Args:
        df: DataFrame to analyze
        
    Returns:
        Dictionary containing analysis results
    """
    results = {
        "summary": {
            "total_sources": get_total_lead_sources(df),
            "top_source": get_top_lead_source(df),
            "average_profit_per_source": get_average_profit_per_source(df)
        },
        "source_metrics": get_lead_source_metrics(df),
        "source_roi": get_lead_source_roi(df)
    }
    
    # Add chart data
    results["chart_data"] = get_lead_source_chart_data(df)
    results["chart_type"] = "bar"
    
    return results

def analyze_vehicles(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze vehicle sales data.
    
    Args:
        df: DataFrame to analyze
        
    Returns:
        Dictionary containing analysis results
    """
    results = {
        "summary": {
            "total_vehicles": len(df),
            "top_make": get_top_vehicle_make(df),
            "top_model": get_top_vehicle_model(df),
            "average_days_to_sell": get_average_days_to_sell(df)
        },
        "vehicle_metrics": get_vehicle_metrics(df),
        "make_performance": get_make_performance(df),
        "model_performance": get_model_performance(df)
    }
    
    # Add chart data
    results["chart_data"] = get_vehicle_chart_data(df)
    results["chart_type"] = "bar"
    
    return results

# Helper functions for data extraction

def get_date_range(df: pd.DataFrame) -> Optional[Dict[str, str]]:
    """Get the date range of the data if date columns exist."""
    date_columns = [col for col in df.columns if 'date' in col.lower()]
    if not date_columns:
        return None
    
    # Use the first date column found
    date_col = date_columns[0]
    try:
        dates = pd.to_datetime(df[date_col], errors='coerce')
        min_date = dates.min()
        max_date = dates.max()
        if pd.isna(min_date) or pd.isna(max_date):
            return None
        return {
            "start": min_date.strftime("%Y-%m-%d"),
            "end": max_date.strftime("%Y-%m-%d"),
            "days": (max_date - min_date).days
        }
    except:
        return None

def get_total_sales(df: pd.DataFrame) -> float:
    """Get the total sales amount."""
    # Look for sold_price or similar columns
    price_cols = [col for col in df.columns if any(term in col.lower() for term in ['sold_price', 'selling_price', 'sale_price'])]
    if not price_cols:
        return 0.0
    
    # Use the first price column found
    price_col = price_cols[0]
    return df[price_col].sum()

def get_total_profit(df: pd.DataFrame) -> float:
    """Get the total profit amount."""
    # Look for profit or similar columns
    profit_cols = [col for col in df.columns if 'profit' in col.lower()]
    if not profit_cols:
        return 0.0
    
    # Use the first profit column found
    profit_col = profit_cols[0]
    return df[profit_col].sum()

def get_average_profit(df: pd.DataFrame) -> float:
    """Get the average profit per sale."""
    # Look for profit or similar columns
    profit_cols = [col for col in df.columns if 'profit' in col.lower()]
    if not profit_cols:
        return 0.0
    
    # Use the first profit column found
    profit_col = profit_cols[0]
    return df[profit_col].mean()

def get_top_sales_rep(df: pd.DataFrame) -> Optional[Dict[str, Any]]:
    """Get the top performing sales representative by profit."""
    # Look for sales rep and profit columns
    rep_cols = [col for col in df.columns if any(term in col.lower() for term in ['sales_rep', 'salesperson', 'rep_name'])]
    profit_cols = [col for col in df.columns if 'profit' in col.lower()]
    
    if not rep_cols or not profit_cols:
        return None
    
    # Use the first columns found
    rep_col = rep_cols[0]
    profit_col = profit_cols[0]
    
    # Group by sales rep and sum profit
    rep_profit = df.groupby(rep_col)[profit_col].sum().reset_index()
    
    # Get the top rep
    if len(rep_profit) == 0:
        return None
    
    top_rep = rep_profit.loc[rep_profit[profit_col].idxmax()]
    return {
        "name": top_rep[rep_col],
        "total_profit": float(top_rep[profit_col]),
        "sale_count": int(df[df[rep_col] == top_rep[rep_col]].shape[0])
    }

def get_top_lead_source(df: pd.DataFrame) -> Optional[Dict[str, Any]]:
    """Get the top performing lead source by profit."""
    # Look for lead source and profit columns
    source_cols = [col for col in df.columns if any(term in col.lower() for term in ['lead_source', 'source'])]
    profit_cols = [col for col in df.columns if 'profit' in col.lower()]
    
    if not source_cols or not profit_cols:
        return None
    
    # Use the first columns found
    source_col = source_cols[0]
    profit_col = profit_cols[0]
    
    # Group by lead source and sum profit
    source_profit = df.groupby(source_col)[profit_col].sum().reset_index()
    
    # Get the top source
    if len(source_profit) == 0:
        return None
    
    top_source = source_profit.loc[source_profit[profit_col].idxmax()]
    return {
        "name": top_source[source_col],
        "total_profit": float(top_source[profit_col]),
        "sale_count": int(df[df[source_col] == top_source[source_col]].shape[0])
    }

def get_top_vehicle(df: pd.DataFrame) -> Optional[Dict[str, Any]]:
    """Get the top performing vehicle by profit."""
    # Look for vehicle model and profit columns
    model_cols = [col for col in df.columns if any(term in col.lower() for term in ['model', 'vehicle_model'])]
    make_cols = [col for col in df.columns if any(term in col.lower() for term in ['make', 'vehicle_make'])]
    profit_cols = [col for col in df.columns if 'profit' in col.lower()]
    
    if not model_cols or not profit_cols:
        return None
    
    # Use the first columns found
    model_col = model_cols[0]
    profit_col = profit_cols[0]
    
    # Include make if available
    if make_cols:
        make_col = make_cols[0]
        df['full_vehicle'] = df[make_col] + ' ' + df[model_col]
        group_col = 'full_vehicle'
    else:
        group_col = model_col
    
    # Group by vehicle and sum profit
    vehicle_profit = df.groupby(group_col)[profit_col].sum().reset_index()
    
    # Get the top vehicle
    if len(vehicle_profit) == 0:
        return None
    
    top_vehicle = vehicle_profit.loc[vehicle_profit[profit_col].idxmax()]
    return {
        "name": top_vehicle[group_col],
        "total_profit": float(top_vehicle[profit_col]),
        "sale_count": int(df[df[group_col] == top_vehicle[group_col]].shape[0])
    }

def get_profit_by_rep_chart_data(df: pd.DataFrame) -> Dict[str, Any]:
    """Get chart data for profit by sales representative."""
    # Look for sales rep and profit columns
    rep_cols = [col for col in df.columns if any(term in col.lower() for term in ['sales_rep', 'salesperson', 'rep_name'])]
    profit_cols = [col for col in df.columns if 'profit' in col.lower()]
    
    if not rep_cols or not profit_cols:
        return {"labels": [], "datasets": [{"label": "Profit", "data": []}]}
    
    # Use the first columns found
    rep_col = rep_cols[0]
    profit_col = profit_cols[0]
    
    # Group by sales rep and sum profit
    rep_profit = df.groupby(rep_col)[profit_col].sum().reset_index()
    
    # Sort by profit descending
    rep_profit = rep_profit.sort_values(profit_col, ascending=False)
    
    # Limit to top 10 reps
    rep_profit = rep_profit.head(10)
    
    return {
        "labels": rep_profit[rep_col].tolist(),
        "datasets": [{
            "label": "Profit",
            "data": rep_profit[profit_col].tolist()
        }]
    }

def get_sales_by_rep(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Get sales metrics by sales representative."""
    # Look for sales rep, price, and profit columns
    rep_cols = [col for col in df.columns if any(term in col.lower() for term in ['sales_rep', 'salesperson', 'rep_name'])]
    price_cols = [col for col in df.columns if any(term in col.lower() for term in ['sold_price', 'selling_price', 'sale_price'])]
    profit_cols = [col for col in df.columns if 'profit' in col.lower()]
    
    if not rep_cols:
        return []
    
    # Use the first rep column found
    rep_col = rep_cols[0]
    
    # Group by sales rep
    result = []
    for rep, group in df.groupby(rep_col):
        rep_data = {
            "name": rep,
            "sale_count": len(group)
        }
        
        # Add price metrics if available
        if price_cols:
            price_col = price_cols[0]
            rep_data["total_sales"] = float(group[price_col].sum())
            rep_data["average_sale"] = float(group[price_col].mean())
        
        # Add profit metrics if available
        if profit_cols:
            profit_col = profit_cols[0]
            rep_data["total_profit"] = float(group[profit_col].sum())
            rep_data["average_profit"] = float(group[profit_col].mean())
        
        result.append(rep_data)
    
    # Sort by total profit or sales descending
    if profit_cols:
        result.sort(key=lambda x: x.get("total_profit", 0), reverse=True)
    elif price_cols:
        result.sort(key=lambda x: x.get("total_sales", 0), reverse=True)
    else:
        result.sort(key=lambda x: x["sale_count"], reverse=True)
    
    return result

def get_average_sale_price(df: pd.DataFrame) -> float:
    """Get the average sale price."""
    # Look for price columns
    price_cols = [col for col in df.columns if any(term in col.lower() for term in ['sold_price', 'selling_price', 'sale_price'])]
    if not price_cols:
        return 0.0
    
    # Use the first price column found
    price_col = price_cols[0]
    return df[price_col].mean()

def get_highest_sale(df: pd.DataFrame) -> Optional[Dict[str, Any]]:
    """Get the highest sale."""
    # Look for price columns
    price_cols = [col for col in df.columns if any(term in col.lower() for term in ['sold_price', 'selling_price', 'sale_price'])]
    if not price_cols:
        return None
    
    # Use the first price column found
    price_col = price_cols[0]
    
    # Get the row with the highest price
    if len(df) == 0:
        return None
    
    highest_idx = df[price_col].idxmax()
    highest_row = df.loc[highest_idx]
    
    result = {
        "price": float(highest_row[price_col])
    }
    
    # Add vehicle info if available
    vehicle_cols = ['vehicle', 'vehicle_make', 'vehicle_model', 'vehicle_year']
    for col in vehicle_cols:
        if col in df.columns:
            result[col] = highest_row[col]
    
    # Add sales rep if available
    rep_cols = [col for col in df.columns if any(term in col.lower() for term in ['sales_rep', 'salesperson', 'rep_name'])]
    if rep_cols:
        result["sales_rep"] = highest_row[rep_cols[0]]
    
    return result

def get_lowest_sale(df: pd.DataFrame) -> Optional[Dict[str, Any]]:
    """Get the lowest sale."""
    # Look for price columns
    price_cols = [col for col in df.columns if any(term in col.lower() for term in ['sold_price', 'selling_price', 'sale_price'])]
    if not price_cols:
        return None
    
    # Use the first price column found
    price_col = price_cols[0]
    
    # Get the row with the lowest price
    if len(df) == 0:
        return None
    
    lowest_idx = df[price_col].idxmin()
    lowest_row = df.loc[lowest_idx]
    
    result = {
        "price": float(lowest_row[price_col])
    }
    
    # Add vehicle info if available
    vehicle_cols = ['vehicle', 'vehicle_make', 'vehicle_model', 'vehicle_year']
    for col in vehicle_cols:
        if col in df.columns:
            result[col] = lowest_row[col]
    
    # Add sales rep if available
    rep_cols = [col for col in df.columns if any(term in col.lower() for term in ['sales_rep', 'salesperson', 'rep_name'])]
    if rep_cols:
        result["sales_rep"] = lowest_row[rep_cols[0]]
    
    return result

def has_date_column(df: pd.DataFrame) -> bool:
    """Check if the DataFrame has a date column."""
    date_columns = [col for col in df.columns if 'date' in col.lower()]
    return len(date_columns) > 0

def get_sales_by_month(df: pd.DataFrame) -> Optional[List[Dict[str, Any]]]:
    """Get sales metrics by month."""
    # Look for date and price columns
    date_columns = [col for col in df.columns if 'date' in col.lower()]
    price_cols = [col for col in df.columns if any(term in col.lower() for term in ['sold_price', 'selling_price', 'sale_price'])]
    
    if not date_columns or not price_cols:
        return None
    
    # Use the first columns found
    date_col = date_columns[0]
    price_col = price_cols[0]
    
    try:
        # Convert to datetime
        df['date'] = pd.to_datetime(df[date_col], errors='coerce')
        
        # Extract month and year
        df['month_year'] = df['date'].dt.strftime('%Y-%m')
        
        # Group by month and calculate metrics
        monthly_sales = df.groupby('month_year').agg({
            price_col: ['sum', 'mean', 'count']
        }).reset_index()
        
        # Flatten the column names
        monthly_sales.columns = ['month_year', 'total_sales', 'average_sale', 'sale_count']
        
        # Convert to list of dictionaries
        result = []
        for _, row in monthly_sales.iterrows():
            result.append({
                "month": row['month_year'],
                "total_sales": float(row['total_sales']),
                "average_sale": float(row['average_sale']),
                "sale_count": int(row['sale_count'])
            })
        
        # Sort by month
        result.sort(key=lambda x: x["month"])
        
        return result
    
    except:
        return None

def get_sales_by_vehicle_type(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Get sales metrics by vehicle type."""
    # Look for vehicle make/model and price columns
    make_cols = [col for col in df.columns if any(term in col.lower() for term in ['make', 'vehicle_make'])]
    model_cols = [col for col in df.columns if any(term in col.lower() for term in ['model', 'vehicle_model'])]
    price_cols = [col for col in df.columns if any(term in col.lower() for term in ['sold_price', 'selling_price', 'sale_price'])]
    
    if not price_cols:
        return []
    
    # Use the first price column found
    price_col = price_cols[0]
    
    # Group by make if available, otherwise use model if available
    if make_cols:
        group_col = make_cols[0]
    elif model_cols:
        group_col = model_cols[0]
    else:
        return []
    
    # Group by vehicle type
    result = []
    for vehicle_type, group in df.groupby(group_col):
        vehicle_data = {
            "type": vehicle_type,
            "sale_count": len(group),
            "total_sales": float(group[price_col].sum()),
            "average_sale": float(group[price_col].mean())
        }
        
        result.append(vehicle_data)
    
    # Sort by total sales descending
    result.sort(key=lambda x: x["total_sales"], reverse=True)
    
    return result

def get_sales_by_rep_chart_data(df: pd.DataFrame) -> Dict[str, Any]:
    """Get chart data for sales by sales representative."""
    # Look for sales rep and price columns
    rep_cols = [col for col in df.columns if any(term in col.lower() for term in ['sales_rep', 'salesperson', 'rep_name'])]
    price_cols = [col for col in df.columns if any(term in col.lower() for term in ['sold_price', 'selling_price', 'sale_price'])]
    
    if not rep_cols or not price_cols:
        return {"labels": [], "datasets": [{"label": "Sales", "data": []}]}
    
    # Use the first columns found
    rep_col = rep_cols[0]
    price_col = price_cols[0]
    
    # Group by sales rep and sum sales
    rep_sales = df.groupby(rep_col)[price_col].sum().reset_index()
    
    # Sort by sales descending
    rep_sales = rep_sales.sort_values(price_col, ascending=False)
    
    # Limit to top 10 reps
    rep_sales = rep_sales.head(10)
    
    return {
        "labels": rep_sales[rep_col].tolist(),
        "datasets": [{
            "label": "Sales",
            "data": rep_sales[price_col].tolist()
        }]
    }

def get_highest_profit_sale(df: pd.DataFrame) -> Optional[Dict[str, Any]]:
    """Get the sale with the highest profit."""
    # Look for profit columns
    profit_cols = [col for col in df.columns if 'profit' in col.lower()]
    if not profit_cols:
        return None
    
    # Use the first profit column found
    profit_col = profit_cols[0]
    
    # Get the row with the highest profit
    if len(df) == 0:
        return None
    
    highest_idx = df[profit_col].idxmax()
    highest_row = df.loc[highest_idx]
    
    result = {
        "profit": float(highest_row[profit_col])
    }
    
    # Add price if available
    price_cols = [col for col in df.columns if any(term in col.lower() for term in ['sold_price', 'selling_price', 'sale_price'])]
    if price_cols:
        result["price"] = float(highest_row[price_cols[0]])
    
    # Add vehicle info if available
    vehicle_cols = ['vehicle', 'vehicle_make', 'vehicle_model', 'vehicle_year']
    for col in vehicle_cols:
        if col in df.columns:
            result[col] = highest_row[col]
    
    # Add sales rep if available
    rep_cols = [col for col in df.columns if any(term in col.lower() for term in ['sales_rep', 'salesperson', 'rep_name'])]
    if rep_cols:
        result["sales_rep"] = highest_row[rep_cols[0]]
    
    return result

def get_profit_margin(df: pd.DataFrame) -> Optional[float]:
    """Get the overall profit margin."""
    # Look for profit and price columns
    profit_cols = [col for col in df.columns if 'profit' in col.lower()]
    price_cols = [col for col in df.columns if any(term in col.lower() for term in ['sold_price', 'selling_price', 'sale_price'])]
    
    if not profit_cols or not price_cols:
        return None
    
    # Use the first columns found
    profit_col = profit_cols[0]
    price_col = price_cols[0]
    
    # Calculate profit margin
    total_profit = df[profit_col].sum()
    total_sales = df[price_col].sum()
    
    if total_sales == 0:
        return 0.0
    
    return (total_profit / total_sales) * 100

def get_profit_by_rep(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Get profit metrics by sales representative."""
    # Look for sales rep and profit columns
    rep_cols = [col for col in df.columns if any(term in col.lower() for term in ['sales_rep', 'salesperson', 'rep_name'])]
    profit_cols = [col for col in df.columns if 'profit' in col.lower()]
    
    if not rep_cols or not profit_cols:
        return []
    
    # Use the first columns found
    rep_col = rep_cols[0]
    profit_col = profit_cols[0]
    
    # Group by sales rep
    result = []
    for rep, group in df.groupby(rep_col):
        rep_data = {
            "name": rep,
            "sale_count": len(group),
            "total_profit": float(group[profit_col].sum()),
            "average_profit": float(group[profit_col].mean())
        }
        
        result.append(rep_data)
    
    # Sort by total profit descending
    result.sort(key=lambda x: x["total_profit"], reverse=True)
    
    return result

def get_profit_by_lead_source(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Get profit metrics by lead source."""
    # Look for lead source and profit columns
    source_cols = [col for col in df.columns if any(term in col.lower() for term in ['lead_source', 'source'])]
    profit_cols = [col for col in df.columns if 'profit' in col.lower()]
    
    if not source_cols or not profit_cols:
        return []
    
    # Use the first columns found
    source_col = source_cols[0]
    profit_col = profit_cols[0]
    
    # Group by lead source
    result = []
    for source, group in df.groupby(source_col):
        source_data = {
            "name": source,
            "sale_count": len(group),
            "total_profit": float(group[profit_col].sum()),
            "average_profit": float(group[profit_col].mean())
        }
        
        result.append(source_data)
    
    # Sort by total profit descending
    result.sort(key=lambda x: x["total_profit"], reverse=True)
    
    return result

def get_profit_by_vehicle_type(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Get profit metrics by vehicle type."""
    # Look for vehicle make/model and profit columns
    make_cols = [col for col in df.columns if any(term in col.lower() for term in ['make', 'vehicle_make'])]
    model_cols = [col for col in df.columns if any(term in col.lower() for term in ['model', 'vehicle_model'])]
    profit_cols = [col for col in df.columns if 'profit' in col.lower()]
    
    if not profit_cols:
        return []
    
    # Use the first profit column found
    profit_col = profit_cols[0]
    
    # Group by make if available, otherwise use model if available
    if make_cols:
        group_col = make_cols[0]
    elif model_cols:
        group_col = model_cols[0]
    else:
        return []
    
    # Group by vehicle type
    result = []
    for vehicle_type, group in df.groupby(group_col):
        vehicle_data = {
            "type": vehicle_type,
            "sale_count": len(group),
            "total_profit": float(group[profit_col].sum()),
            "average_profit": float(group[profit_col].mean())
        }
        
        result.append(vehicle_data)
    
    # Sort by total profit descending
    result.sort(key=lambda x: x["total_profit"], reverse=True)
    
    return result

def get_total_reps(df: pd.DataFrame) -> int:
    """Get the total number of sales representatives."""
    # Look for sales rep columns
    rep_cols = [col for col in df.columns if any(term in col.lower() for term in ['sales_rep', 'salesperson', 'rep_name'])]
    if not rep_cols:
        return 0
    
    # Use the first rep column found
    rep_col = rep_cols[0]
    
    # Count unique reps
    return df[rep_col].nunique()

def get_average_profit_per_rep(df: pd.DataFrame) -> Optional[float]:
    """Get the average profit per sales representative."""
    # Look for sales rep and profit columns
    rep_cols = [col for col in df.columns if any(term in col.lower() for term in ['sales_rep', 'salesperson', 'rep_name'])]
    profit_cols = [col for col in df.columns if 'profit' in col.lower()]
    
    if not rep_cols or not profit_cols:
        return None
    
    # Use the first columns found
    rep_col = rep_cols[0]
    profit_col = profit_cols[0]
    
    # Group by sales rep and calculate average profit
    rep_profit = df.groupby(rep_col)[profit_col].sum().reset_index()
    
    if len(rep_profit) == 0:
        return 0.0
    
    return rep_profit[profit_col].mean()

def get_rep_leaderboard(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Get a leaderboard of sales representatives by profit."""
    # Look for sales rep and profit columns
    rep_cols = [col for col in df.columns if any(term in col.lower() for term in ['sales_rep', 'salesperson', 'rep_name'])]
    profit_cols = [col for col in df.columns if 'profit' in col.lower()]
    
    if not rep_cols or not profit_cols:
        return []
    
    # Use the first columns found
    rep_col = rep_cols[0]
    profit_col = profit_cols[0]
    
    # Group by sales rep and calculate metrics
    rep_metrics = df.groupby(rep_col).agg({
        profit_col: ['sum', 'mean', 'count']
    }).reset_index()
    
    # Flatten the column names
    rep_metrics.columns = ['name', 'total_profit', 'average_profit', 'sale_count']
    
    # Sort by total profit descending
    rep_metrics = rep_metrics.sort_values('total_profit', ascending=False)
    
    # Convert to list of dictionaries
    result = []
    for _, row in rep_metrics.iterrows():
        result.append({
            "name": row['name'],
            "total_profit": float(row['total_profit']),
            "average_profit": float(row['average_profit']),
            "sale_count": int(row['sale_count'])
        })
    
    return result

def get_rep_metrics(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Get detailed metrics for each sales representative."""
    # Look for sales rep, profit, and price columns
    rep_cols = [col for col in df.columns if any(term in col.lower() for term in ['sales_rep', 'salesperson', 'rep_name'])]
    profit_cols = [col for col in df.columns if 'profit' in col.lower()]
    price_cols = [col for col in df.columns if any(term in col.lower() for term in ['sold_price', 'selling_price', 'sale_price'])]
    
    if not rep_cols:
        return []
    
    # Use the first rep column found
    rep_col = rep_cols[0]
    
    # Group by sales rep
    result = []
    for rep, group in df.groupby(rep_col):
        rep_data = {
            "name": rep,
            "sale_count": len(group)
        }
        
        # Add profit metrics if available
        if profit_cols:
            profit_col = profit_cols[0]
            rep_data["total_profit"] = float(group[profit_col].sum())
            rep_data["average_profit"] = float(group[profit_col].mean())
            rep_data["highest_profit"] = float(group[profit_col].max())
        
        # Add price metrics if available
        if price_cols:
            price_col = price_cols[0]
            rep_data["total_sales"] = float(group[price_col].sum())
            rep_data["average_sale"] = float(group[price_col].mean())
            rep_data["highest_sale"] = float(group[price_col].max())
        
        # Add profit margin if both profit and price are available
        if profit_cols and price_cols:
            profit_col = profit_cols[0]
            price_col = price_cols[0]
            total_profit = group[profit_col].sum()
            total_sales = group[price_col].sum()
            if total_sales > 0:
                rep_data["profit_margin"] = (total_profit / total_sales) * 100
        
        result.append(rep_data)
    
    # Sort by total profit or sales descending
    if profit_cols:
        result.sort(key=lambda x: x.get("total_profit", 0), reverse=True)
    elif price_cols:
        result.sort(key=lambda x: x.get("total_sales", 0), reverse=True)
    else:
        result.sort(key=lambda x: x["sale_count"], reverse=True)
    
    return result

def get_rep_performance_chart_data(df: pd.DataFrame) -> Dict[str, Any]:
    """Get chart data for sales representative performance."""
    # Look for sales rep and profit columns
    rep_cols = [col for col in df.columns if any(term in col.lower() for term in ['sales_rep', 'salesperson', 'rep_name'])]
    profit_cols = [col for col in df.columns if 'profit' in col.lower()]
    
    if not rep_cols or not profit_cols:
        return {"labels": [], "datasets": [{"label": "Profit", "data": []}, {"label": "Sales Count", "data": []}]}
    
    # Use the first columns found
    rep_col = rep_cols[0]
    profit_col = profit_cols[0]
    
    # Group by sales rep and calculate metrics
    rep_metrics = df.groupby(rep_col).agg({
        profit_col: 'sum',
        rep_col: 'count'
    }).reset_index()
    
    # Rename columns
    rep_metrics.columns = ['name', 'total_profit', 'sale_count']
    
    # Sort by total profit descending
    rep_metrics = rep_metrics.sort_values('total_profit', ascending=False)
    
    # Limit to top 10 reps
    rep_metrics = rep_metrics.head(10)
    
    return {
        "labels": rep_metrics['name'].tolist(),
        "datasets": [
            {
                "label": "Profit",
                "data": rep_metrics['total_profit'].tolist()
            },
            {
                "label": "Sales Count",
                "data": rep_metrics['sale_count'].tolist()
            }
        ]
    }

def get_total_lead_sources(df: pd.DataFrame) -> int:
    """Get the total number of lead sources."""
    # Look for lead source columns
    source_cols = [col for col in df.columns if any(term in col.lower() for term in ['lead_source', 'source'])]
    if not source_cols:
        return 0
    
    # Use the first source column found
    source_col = source_cols[0]
    
    # Count unique sources
    return df[source_col].nunique()

def get_average_profit_per_source(df: pd.DataFrame) -> Optional[float]:
    """Get the average profit per lead source."""
    # Look for lead source and profit columns
    source_cols = [col for col in df.columns if any(term in col.lower() for term in ['lead_source', 'source'])]
    profit_cols = [col for col in df.columns if 'profit' in col.lower()]
    
    if not source_cols or not profit_cols:
        return None
    
    # Use the first columns found
    source_col = source_cols[0]
    profit_col = profit_cols[0]
    
    # Group by lead source and calculate average profit
    source_profit = df.groupby(source_col)[profit_col].sum().reset_index()
    
    if len(source_profit) == 0:
        return 0.0
    
    return source_profit[profit_col].mean()

def get_lead_source_metrics(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Get detailed metrics for each lead source."""
    # Look for lead source, profit, and price columns
    source_cols = [col for col in df.columns if any(term in col.lower() for term in ['lead_source', 'source'])]
    profit_cols = [col for col in df.columns if 'profit' in col.lower()]
    price_cols = [col for col in df.columns if any(term in col.lower() for term in ['sold_price', 'selling_price', 'sale_price'])]
    expense_cols = [col for col in df.columns if any(term in col.lower() for term in ['expense', 'cost'])]
    
    if not source_cols:
        return []
    
    # Use the first source column found
    source_col = source_cols[0]
    
    # Group by lead source
    result = []
    for source, group in df.groupby(source_col):
        source_data = {
            "name": source,
            "sale_count": len(group)
        }
        
        # Add profit metrics if available
        if profit_cols:
            profit_col = profit_cols[0]
            source_data["total_profit"] = float(group[profit_col].sum())
            source_data["average_profit"] = float(group[profit_col].mean())
        
        # Add price metrics if available
        if price_cols:
            price_col = price_cols[0]
            source_data["total_sales"] = float(group[price_col].sum())
            source_data["average_sale"] = float(group[price_col].mean())
        
        # Add expense metrics if available
        if expense_cols:
            expense_col = expense_cols[0]
            source_data["total_expense"] = float(group[expense_col].sum())
            source_data["average_expense"] = float(group[expense_col].mean())
        
        # Add ROI if both profit and expense are available
        if profit_cols and expense_cols:
            profit_col = profit_cols[0]
            expense_col = expense_cols[0]
            total_profit = group[profit_col].sum()
            total_expense = group[expense_col].sum()
            if total_expense > 0:
                source_data["roi"] = (total_profit / total_expense) * 100
        
        result.append(source_data)
    
    # Sort by total profit or sales descending
    if profit_cols:
        result.sort(key=lambda x: x.get("total_profit", 0), reverse=True)
    elif price_cols:
        result.sort(key=lambda x: x.get("total_sales", 0), reverse=True)
    else:
        result.sort(key=lambda x: x["sale_count"], reverse=True)
    
    return result

def get_lead_source_roi(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Get ROI metrics for each lead source."""
    # Look for lead source, profit, and expense columns
    source_cols = [col for col in df.columns if any(term in col.lower() for term in ['lead_source', 'source'])]
    profit_cols = [col for col in df.columns if 'profit' in col.lower()]
    expense_cols = [col for col in df.columns if any(term in col.lower() for term in ['expense', 'cost'])]
    
    if not source_cols or not profit_cols or not expense_cols:
        return []
    
    # Use the first columns found
    source_col = source_cols[0]
    profit_col = profit_cols[0]
    expense_col = expense_cols[0]
    
    # Group by lead source and calculate metrics
    source_metrics = df.groupby(source_col).agg({
        profit_col: 'sum',
        expense_col: 'sum',
        source_col: 'count'
    }).reset_index()
    
    # Rename columns
    source_metrics.columns = ['name', 'total_profit', 'total_expense', 'sale_count']
    
    # Calculate ROI
    source_metrics['roi'] = source_metrics.apply(
        lambda row: (row['total_profit'] / row['total_expense']) * 100 if row['total_expense'] > 0 else 0,
        axis=1
    )
    
    # Sort by ROI descending
    source_metrics = source_metrics.sort_values('roi', ascending=False)
    
    # Convert to list of dictionaries
    result = []
    for _, row in source_metrics.iterrows():
        result.append({
            "name": row['name'],
            "total_profit": float(row['total_profit']),
            "total_expense": float(row['total_expense']),
            "sale_count": int(row['sale_count']),
            "roi": float(row['roi'])
        })
    
    return result

def get_lead_source_chart_data(df: pd.DataFrame) -> Dict[str, Any]:
    """Get chart data for lead source performance."""
    # Look for lead source, profit, and expense columns
    source_cols = [col for col in df.columns if any(term in col.lower() for term in ['lead_source', 'source'])]
    profit_cols = [col for col in df.columns if 'profit' in col.lower()]
    expense_cols = [col for col in df.columns if any(term in col.lower() for term in ['expense', 'cost'])]
    
    if not source_cols or not profit_cols:
        return {"labels": [], "datasets": [{"label": "Profit", "data": []}]}
    
    # Use the first columns found
    source_col = source_cols[0]
    profit_col = profit_cols[0]
    
    # Group by lead source and calculate profit
    source_profit = df.groupby(source_col)[profit_col].sum().reset_index()
    
    # Sort by profit descending
    source_profit = source_profit.sort_values(profit_col, ascending=False)
    
    # Limit to top 10 sources
    source_profit = source_profit.head(10)
    
    # If expense data is available, add ROI dataset
    if expense_cols:
        expense_col = expense_cols[0]
        source_expense = df.groupby(source_col)[expense_col].sum().reset_index()
        
        # Merge profit and expense data
        source_data = pd.merge(source_profit, source_expense, on=source_col)
        
        # Calculate ROI
        source_data['roi'] = source_data.apply(
            lambda row: (row[profit_col] / row[expense_col]) * 100 if row[expense_col] > 0 else 0,
            axis=1
        )
        
        return {
            "labels": source_data[source_col].tolist(),
            "datasets": [
                {
                    "label": "Profit",
                    "data": source_data[profit_col].tolist()
                },
                {
                    "label": "ROI (%)",
                    "data": source_data['roi'].tolist()
                }
            ]
        }
    
    # If expense data is not available, just return profit data
    return {
        "labels": source_profit[source_col].tolist(),
        "datasets": [{
            "label": "Profit",
            "data": source_profit[profit_col].tolist()
        }]
    }

def get_top_vehicle_make(df: pd.DataFrame) -> Optional[Dict[str, Any]]:
    """Get the top performing vehicle make by profit."""
    # Look for vehicle make and profit columns
    make_cols = [col for col in df.columns if any(term in col.lower() for term in ['make', 'vehicle_make'])]
    profit_cols = [col for col in df.columns if 'profit' in col.lower()]
    
    if not make_cols or not profit_cols:
        return None
    
    # Use the first columns found
    make_col = make_cols[0]
    profit_col = profit_cols[0]
    
    # Group by make and sum profit
    make_profit = df.groupby(make_col)[profit_col].sum().reset_index()
    
    # Get the top make
    if len(make_profit) == 0:
        return None
    
    top_make = make_profit.loc[make_profit[profit_col].idxmax()]
    return {
        "name": top_make[make_col],
        "total_profit": float(top_make[profit_col]),
        "sale_count": int(df[df[make_col] == top_make[make_col]].shape[0])
    }

def get_top_vehicle_model(df: pd.DataFrame) -> Optional[Dict[str, Any]]:
    """Get the top performing vehicle model by profit."""
    # Look for vehicle model and profit columns
    model_cols = [col for col in df.columns if any(term in col.lower() for term in ['model', 'vehicle_model'])]
    profit_cols = [col for col in df.columns if 'profit' in col.lower()]
    
    if not model_cols or not profit_cols:
        return None
    
    # Use the first columns found
    model_col = model_cols[0]
    profit_col = profit_cols[0]
    
    # Group by model and sum profit
    model_profit = df.groupby(model_col)[profit_col].sum().reset_index()
    
    # Get the top model
    if len(model_profit) == 0:
        return None
    
    top_model = model_profit.loc[model_profit[profit_col].idxmax()]
    return {
        "name": top_model[model_col],
        "total_profit": float(top_model[profit_col]),
        "sale_count": int(df[df[model_col] == top_model[model_col]].shape[0])
    }

def get_average_days_to_sell(df: pd.DataFrame) -> Optional[float]:
    """Get the average days to sell a vehicle."""
    # Look for days to close/sell columns
    days_cols = [col for col in df.columns if any(term in col.lower() for term in ['days_to_close', 'days_to_sell'])]
    if not days_cols:
        return None
    
    # Use the first days column found
    days_col = days_cols[0]
    
    # Calculate average
    return df[days_col].mean()

def get_vehicle_metrics(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Get detailed metrics for each vehicle type."""
    # Look for vehicle make/model, profit, and price columns
    make_cols = [col for col in df.columns if any(term in col.lower() for term in ['make', 'vehicle_make'])]
    model_cols = [col for col in df.columns if any(term in col.lower() for term in ['model', 'vehicle_model'])]
    profit_cols = [col for col in df.columns if 'profit' in col.lower()]
    price_cols = [col for col in df.columns if any(term in col.lower() for term in ['sold_price', 'selling_price', 'sale_price'])]
    days_cols = [col for col in df.columns if any(term in col.lower() for term in ['days_to_close', 'days_to_sell'])]
    
    # Determine grouping column
    if make_cols and model_cols:
        # If both make and model are available, combine them
        make_col = make_cols[0]
        model_col = model_cols[0]
        df['vehicle_type'] = df[make_col] + ' ' + df[model_col]
        group_col = 'vehicle_type'
    elif make_cols:
        group_col = make_cols[0]
    elif model_cols:
        group_col = model_cols[0]
    else:
        return []
    
    # Group by vehicle type
    result = []
    for vehicle_type, group in df.groupby(group_col):
        vehicle_data = {
            "type": vehicle_type,
            "sale_count": len(group)
        }
        
        # Add profit metrics if available
        if profit_cols:
            profit_col = profit_cols[0]
            vehicle_data["total_profit"] = float(group[profit_col].sum())
            vehicle_data["average_profit"] = float(group[profit_col].mean())
        
        # Add price metrics if available
        if price_cols:
            price_col = price_cols[0]
            vehicle_data["total_sales"] = float(group[price_col].sum())
            vehicle_data["average_sale"] = float(group[price_col].mean())
        
        # Add days to sell metrics if available
        if days_cols:
            days_col = days_cols[0]
            vehicle_data["average_days_to_sell"] = float(group[days_col].mean())
        
        result.append(vehicle_data)
    
    # Sort by total profit or sales descending
    if profit_cols:
        result.sort(key=lambda x: x.get("total_profit", 0), reverse=True)
    elif price_cols:
        result.sort(key=lambda x: x.get("total_sales", 0), reverse=True)
    else:
        result.sort(key=lambda x: x["sale_count"], reverse=True)
    
    return result

def get_make_performance(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Get performance metrics for each vehicle make."""
    # Look for vehicle make, profit, and price columns
    make_cols = [col for col in df.columns if any(term in col.lower() for term in ['make', 'vehicle_make'])]
    profit_cols = [col for col in df.columns if 'profit' in col.lower()]
    price_cols = [col for col in df.columns if any(term in col.lower() for term in ['sold_price', 'selling_price', 'sale_price'])]
    
    if not make_cols:
        return []
    
    # Use the first make column found
    make_col = make_cols[0]
    
    # Group by make
    result = []
    for make, group in df.groupby(make_col):
        make_data = {
            "make": make,
            "sale_count": len(group)
        }
        
        # Add profit metrics if available
        if profit_cols:
            profit_col = profit_cols[0]
            make_data["total_profit"] = float(group[profit_col].sum())
            make_data["average_profit"] = float(group[profit_col].mean())
        
        # Add price metrics if available
        if price_cols:
            price_col = price_cols[0]
            make_data["total_sales"] = float(group[price_col].sum())
            make_data["average_sale"] = float(group[price_col].mean())
        
        result.append(make_data)
    
    # Sort by total profit or sales descending
    if profit_cols:
        result.sort(key=lambda x: x.get("total_profit", 0), reverse=True)
    elif price_cols:
        result.sort(key=lambda x: x.get("total_sales", 0), reverse=True)
    else:
        result.sort(key=lambda x: x["sale_count"], reverse=True)
    
    return result

def get_model_performance(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Get performance metrics for each vehicle model."""
    # Look for vehicle model, profit, and price columns
    model_cols = [col for col in df.columns if any(term in col.lower() for term in ['model', 'vehicle_model'])]
    profit_cols = [col for col in df.columns if 'profit' in col.lower()]
    price_cols = [col for col in df.columns if any(term in col.lower() for term in ['sold_price', 'selling_price', 'sale_price'])]
    
    if not model_cols:
        return []
    
    # Use the first model column found
    model_col = model_cols[0]
    
    # Group by model
    result = []
    for model, group in df.groupby(model_col):
        model_data = {
            "model": model,
            "sale_count": len(group)
        }
        
        # Add profit metrics if available
        if profit_cols:
            profit_col = profit_cols[0]
            model_data["total_profit"] = float(group[profit_col].sum())
            model_data["average_profit"] = float(group[profit_col].mean())
        
        # Add price metrics if available
        if price_cols:
            price_col = price_cols[0]
            model_data["total_sales"] = float(group[price_col].sum())
            model_data["average_sale"] = float(group[price_col].mean())
        
        result.append(model_data)
    
    # Sort by total profit or sales descending
    if profit_cols:
        result.sort(key=lambda x: x.get("total_profit", 0), reverse=True)
    elif price_cols:
        result.sort(key=lambda x: x.get("total_sales", 0), reverse=True)
    else:
        result.sort(key=lambda x: x["sale_count"], reverse=True)
    
    return result

def get_vehicle_chart_data(df: pd.DataFrame) -> Dict[str, Any]:
    """Get chart data for vehicle performance."""
    # Look for vehicle make/model and profit columns
    make_cols = [col for col in df.columns if any(term in col.lower() for term in ['make', 'vehicle_make'])]
    model_cols = [col for col in df.columns if any(term in col.lower() for term in ['model', 'vehicle_model'])]
    profit_cols = [col for col in df.columns if 'profit' in col.lower()]
    
    # Determine grouping column
    if make_cols:
        group_col = make_cols[0]
    elif model_cols:
        group_col = model_cols[0]
    else:
        return {"labels": [], "datasets": [{"label": "Profit", "data": []}]}
    
    # Use the first profit column found if available
    if profit_cols:
        profit_col = profit_cols[0]
        
        # Group by vehicle type and sum profit
        vehicle_profit = df.groupby(group_col)[profit_col].sum().reset_index()
        
        # Sort by profit descending
        vehicle_profit = vehicle_profit.sort_values(profit_col, ascending=False)
        
        # Limit to top 10 vehicles
        vehicle_profit = vehicle_profit.head(10)
        
        return {
            "labels": vehicle_profit[group_col].tolist(),
            "datasets": [{
                "label": "Profit",
                "data": vehicle_profit[profit_col].tolist()
            }]
        }
    
    # If profit data is not available, use count
    vehicle_count = df[group_col].value_counts().reset_index()
    vehicle_count.columns = [group_col, 'count']
    
    # Sort by count descending
    vehicle_count = vehicle_count.sort_values('count', ascending=False)
    
    # Limit to top 10 vehicles
    vehicle_count = vehicle_count.head(10)
    
    return {
        "labels": vehicle_count[group_col].tolist(),
        "datasets": [{
            "label": "Sales Count",
            "data": vehicle_count['count'].tolist()
        }]
    }
