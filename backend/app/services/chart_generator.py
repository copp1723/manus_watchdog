"""
Chart generation utilities for Watchdog AI.

This module handles generating charts from analysis data.
"""
import os
import logging
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from typing import Dict, Any, List, Optional
import uuid

from app.core.config import settings

# Configure matplotlib to use Agg backend (non-interactive)
matplotlib.use('Agg')

# Configure logging
logger = logging.getLogger("watchdog.chart_generator")

def generate_chart(chart_data: Dict[str, Any], filename: str, chart_type: str = "bar") -> str:
    """
    Generate a chart from the provided data.
    
    Args:
        chart_data: Dictionary containing chart data (labels and datasets)
        filename: Filename for the chart image
        chart_type: Type of chart to generate (bar, line, pie)
        
    Returns:
        URL path to the generated chart
    """
    logger.info(f"Generating {chart_type} chart: {filename}")
    
    # Create figure and axis
    plt.figure(figsize=(10, 6))
    
    # Get chart data
    labels = chart_data.get("labels", [])
    datasets = chart_data.get("datasets", [])
    
    if not labels or not datasets:
        logger.warning("Chart data is empty")
        return ""
    
    # Generate chart based on type
    if chart_type == "bar":
        generate_bar_chart(labels, datasets)
    elif chart_type == "line":
        generate_line_chart(labels, datasets)
    elif chart_type == "pie":
        generate_pie_chart(labels, datasets)
    else:
        # Default to bar chart
        generate_bar_chart(labels, datasets)
    
    # Add title and labels
    plt.title(get_chart_title(chart_type, datasets), fontsize=14)
    plt.xlabel("Categories", fontsize=12)
    plt.ylabel("Values", fontsize=12)
    
    # Add grid
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save chart
    chart_path = os.path.join(settings.CHARTS_DIR, filename)
    plt.savefig(chart_path, dpi=100, bbox_inches='tight')
    plt.close()
    
    # Return URL path to chart
    return f"/static/charts/{filename}"

def generate_bar_chart(labels: List[str], datasets: List[Dict[str, Any]]) -> None:
    """
    Generate a bar chart.
    
    Args:
        labels: List of category labels
        datasets: List of datasets containing values
    """
    # Set up bar positions
    num_datasets = len(datasets)
    bar_width = 0.8 / num_datasets
    
    # Generate bars for each dataset
    for i, dataset in enumerate(datasets):
        data = dataset.get("data", [])
        label = dataset.get("label", f"Dataset {i+1}")
        
        # Calculate bar positions
        index = np.arange(len(labels))
        offset = (i - num_datasets / 2 + 0.5) * bar_width
        
        # Create bars
        plt.bar(index + offset, data, bar_width, label=label)
    
    # Set x-axis labels
    plt.xticks(range(len(labels)), labels, rotation=45, ha='right')
    
    # Add legend if multiple datasets
    if num_datasets > 1:
        plt.legend()

def generate_line_chart(labels: List[str], datasets: List[Dict[str, Any]]) -> None:
    """
    Generate a line chart.
    
    Args:
        labels: List of category labels
        datasets: List of datasets containing values
    """
    # Generate lines for each dataset
    for i, dataset in enumerate(datasets):
        data = dataset.get("data", [])
        label = dataset.get("label", f"Dataset {i+1}")
        
        # Create line
        plt.plot(range(len(labels)), data, marker='o', label=label)
    
    # Set x-axis labels
    plt.xticks(range(len(labels)), labels, rotation=45, ha='right')
    
    # Add legend if multiple datasets
    if len(datasets) > 1:
        plt.legend()

def generate_pie_chart(labels: List[str], datasets: List[Dict[str, Any]]) -> None:
    """
    Generate a pie chart.
    
    Args:
        labels: List of category labels
        datasets: List of datasets containing values
    """
    # Use the first dataset for pie chart
    if datasets:
        data = datasets[0].get("data", [])
        
        # Create pie chart
        plt.pie(data, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle

def get_chart_title(chart_type: str, datasets: List[Dict[str, Any]]) -> str:
    """
    Generate a title for the chart.
    
    Args:
        chart_type: Type of chart
        datasets: List of datasets
        
    Returns:
        Chart title
    """
    # Get dataset labels
    dataset_labels = [dataset.get("label", "Data") for dataset in datasets]
    
    # Generate title based on chart type and datasets
    if chart_type == "bar":
        if len(dataset_labels) == 1:
            return f"{dataset_labels[0]} by Category"
        else:
            return "Category Comparison"
    elif chart_type == "line":
        if len(dataset_labels) == 1:
            return f"{dataset_labels[0]} Trend"
        else:
            return "Trend Comparison"
    elif chart_type == "pie":
        return f"{dataset_labels[0]} Distribution"
    else:
        return "Data Visualization"
