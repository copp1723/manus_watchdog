"""
Insight engine for Watchdog AI.

This module generates insights and answers questions based on analysis results.
"""
import logging
from typing import Dict, Any, List, Optional
import re
import random

logger = logging.getLogger("watchdog.insight_engine")

def generate_insights(analysis_results: Dict[str, Any], intent: str) -> List[Dict[str, Any]]:
    """
    Generate insights based on analysis results.
    
    Args:
        analysis_results: Dictionary containing analysis results
        intent: Analysis intent
        
    Returns:
        List of insight items
    """
    logger.info(f"Generating insights for intent: {intent}")
    
    insights = []
    
    # Generate insights based on intent
    if intent == "sales_analysis":
        insights.extend(generate_sales_insights(analysis_results))
    elif intent == "profit_analysis":
        insights.extend(generate_profit_insights(analysis_results))
    elif intent == "rep_performance":
        insights.extend(generate_rep_insights(analysis_results))
    elif intent == "lead_source_analysis":
        insights.extend(generate_lead_source_insights(analysis_results))
    elif intent == "vehicle_analysis":
        insights.extend(generate_vehicle_insights(analysis_results))
    else:
        # General analysis
        insights.extend(generate_general_insights(analysis_results))
    
    return insights

def generate_general_insights(analysis_results: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Generate insights for general analysis.
    
    Args:
        analysis_results: Dictionary containing analysis results
        
    Returns:
        List of insight items
    """
    insights = []
    
    # Add summary insight
    summary = analysis_results.get("summary", {})
    if summary:
        total_sales = format_currency(summary.get("total_sales", 0))
        total_profit = format_currency(summary.get("total_profit", 0))
        average_profit = format_currency(summary.get("average_profit", 0))
        
        date_range = summary.get("date_range", {})
        date_text = ""
        if date_range:
            start = date_range.get("start", "")
            end = date_range.get("end", "")
            days = date_range.get("days", 0)
            if start and end:
                date_text = f" from {start} to {end} ({days} days)"
        
        insights.append({
            "title": "Sales Summary",
            "description": f"Your dealership generated {total_sales} in sales and {total_profit} in profit{date_text}.",
            "amount": total_profit,
            "percentage": None,
            "actionItems": [
                f"Average profit per sale is {average_profit}.",
                "Review the top performing areas below for more insights."
            ]
        })
    
    # Add top metrics insights
    top_metrics = analysis_results.get("top_metrics", [])
    for metric in top_metrics:
        title = metric.get("title", "")
        value = metric.get("value", "")
        metric_value = metric.get("metric", "")
        description = metric.get("description", "")
        
        insights.append({
            "title": title,
            "description": description,
            "employee": value,
            "employeeTitle": title.lower(),
            "amount": metric_value,
            "percentage": None,
            "actionItems": generate_action_items_for_metric(title, value, metric_value)
        })
    
    return insights

def generate_sales_insights(analysis_results: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Generate insights for sales analysis.
    
    Args:
        analysis_results: Dictionary containing analysis results
        
    Returns:
        List of insight items
    """
    insights = []
    
    # Add summary insight
    summary = analysis_results.get("summary", {})
    if summary:
        total_sales = format_currency(summary.get("total_sales", 0))
        average_sale = format_currency(summary.get("average_sale_price", 0))
        highest_sale = summary.get("highest_sale", {})
        
        highest_sale_price = format_currency(highest_sale.get("price", 0)) if highest_sale else ""
        highest_sale_vehicle = highest_sale.get("vehicle", "") if highest_sale else ""
        highest_sale_rep = highest_sale.get("sales_rep", "") if highest_sale else ""
        
        insights.append({
            "title": "Sales Performance",
            "description": f"Your dealership generated {total_sales} in total sales with an average sale price of {average_sale}.",
            "amount": total_sales,
            "percentage": None,
            "actionItems": [
                f"Your highest sale was {highest_sale_price}" + (f" for a {highest_sale_vehicle}" if highest_sale_vehicle else "") + (f" by {highest_sale_rep}" if highest_sale_rep else "") + ".",
                "Focus on high-value vehicles to increase average sale price."
            ]
        })
    
    # Add sales by rep insight
    sales_by_rep = analysis_results.get("sales_by_rep", [])
    if sales_by_rep and len(sales_by_rep) > 0:
        top_rep = sales_by_rep[0]
        rep_name = top_rep.get("name", "")
        rep_sales = format_currency(top_rep.get("total_sales", 0))
        rep_count = top_rep.get("sale_count", 0)
        
        insights.append({
            "title": "Top Sales Representative",
            "description": f"{rep_name} is your top performing sales representative by total sales.",
            "employee": rep_name,
            "employeeTitle": "top sales performer",
            "amount": rep_sales,
            "percentage": None,
            "actionItems": [
                f"Completed {rep_count} sales.",
                f"Study {rep_name}'s sales techniques for team training."
            ]
        })
    
    # Add sales by vehicle type insight
    sales_by_vehicle = analysis_results.get("sales_by_vehicle_type", [])
    if sales_by_vehicle and len(sales_by_vehicle) > 0:
        top_vehicle = sales_by_vehicle[0]
        vehicle_type = top_vehicle.get("type", "")
        vehicle_sales = format_currency(top_vehicle.get("total_sales", 0))
        vehicle_count = top_vehicle.get("sale_count", 0)
        
        insights.append({
            "title": "Top Selling Vehicle",
            "description": f"{vehicle_type} is your top selling vehicle by total sales.",
            "amount": vehicle_sales,
            "percentage": None,
            "actionItems": [
                f"Sold {vehicle_count} units.",
                f"Consider increasing inventory of {vehicle_type} models."
            ]
        })
    
    return insights

def generate_profit_insights(analysis_results: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Generate insights for profit analysis.
    
    Args:
        analysis_results: Dictionary containing analysis results
        
    Returns:
        List of insight items
    """
    insights = []
    
    # Add summary insight
    summary = analysis_results.get("summary", {})
    if summary:
        total_profit = format_currency(summary.get("total_profit", 0))
        average_profit = format_currency(summary.get("average_profit", 0))
        profit_margin = summary.get("profit_margin", 0)
        profit_margin_formatted = f"{profit_margin:.1f}%" if profit_margin is not None else ""
        
        highest_profit_sale = summary.get("highest_profit_sale", {})
        highest_profit = format_currency(highest_profit_sale.get("profit", 0)) if highest_profit_sale else ""
        highest_profit_vehicle = highest_profit_sale.get("vehicle", "") if highest_profit_sale else ""
        
        insights.append({
            "title": "Profit Performance",
            "description": f"Your dealership generated {total_profit} in total profit with an average profit of {average_profit} per sale.",
            "amount": total_profit,
            "percentage": profit_margin_formatted,
            "actionItems": [
                f"Your highest profit sale was {highest_profit}" + (f" for a {highest_profit_vehicle}" if highest_profit_vehicle else "") + ".",
                "Focus on high-margin vehicles to increase overall profitability."
            ]
        })
    
    # Add profit by rep insight
    profit_by_rep = analysis_results.get("profit_by_rep", [])
    if profit_by_rep and len(profit_by_rep) > 0:
        top_rep = profit_by_rep[0]
        rep_name = top_rep.get("name", "")
        rep_profit = format_currency(top_rep.get("total_profit", 0))
        rep_average = format_currency(top_rep.get("average_profit", 0))
        
        insights.append({
            "title": "Top Profit Generator",
            "description": f"{rep_name} is your top profit-generating sales representative.",
            "employee": rep_name,
            "employeeTitle": "top profit generator",
            "amount": rep_profit,
            "percentage": None,
            "actionItems": [
                f"Average profit per sale: {rep_average}.",
                f"Analyze {rep_name}'s negotiation strategies for team training."
            ]
        })
    
    # Add profit by lead source insight
    profit_by_source = analysis_results.get("profit_by_lead_source", [])
    if profit_by_source and len(profit_by_source) > 0:
        top_source = profit_by_source[0]
        source_name = top_source.get("name", "")
        source_profit = format_currency(top_source.get("total_profit", 0))
        source_average = format_currency(top_source.get("average_profit", 0))
        
        insights.append({
            "title": "Most Profitable Lead Source",
            "description": f"{source_name} is your most profitable lead source.",
            "amount": source_profit,
            "percentage": None,
            "actionItems": [
                f"Average profit per sale: {source_average}.",
                f"Consider increasing marketing investment in {source_name}."
            ]
        })
    
    return insights

def generate_rep_insights(analysis_results: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Generate insights for sales representative performance analysis.
    
    Args:
        analysis_results: Dictionary containing analysis results
        
    Returns:
        List of insight items
    """
    insights = []
    
    # Add summary insight
    summary = analysis_results.get("summary", {})
    if summary:
        total_reps = summary.get("total_reps", 0)
        average_profit = format_currency(summary.get("average_profit_per_rep", 0))
        
        top_rep = summary.get("top_rep", {})
        top_rep_name = top_rep.get("name", "") if top_rep else ""
        top_rep_profit = format_currency(top_rep.get("total_profit", 0)) if top_rep else ""
        
        insights.append({
            "title": "Sales Team Performance",
            "description": f"Your sales team consists of {total_reps} representatives with an average profit of {average_profit} per rep.",
            "amount": None,
            "percentage": None,
            "actionItems": [
                f"{top_rep_name} is your top performer with {top_rep_profit} in profit.",
                "Consider implementing a mentorship program with top performers."
            ]
        })
    
    # Add rep leaderboard insight
    rep_leaderboard = analysis_results.get("rep_leaderboard", [])
    if rep_leaderboard and len(rep_leaderboard) >= 3:
        top_reps = rep_leaderboard[:3]
        
        rep_names = [rep.get("name", "") for rep in top_reps]
        rep_profits = [format_currency(rep.get("total_profit", 0)) for rep in top_reps]
        
        insights.append({
            "title": "Sales Rep Leaderboard",
            "description": f"Your top 3 sales representatives by profit are:",
            "employee": rep_names[0],
            "employeeTitle": "top performer",
            "amount": rep_profits[0],
            "percentage": None,
            "actionItems": [
                f"2nd Place: {rep_names[1]} with {rep_profits[1]}",
                f"3rd Place: {rep_names[2]} with {rep_profits[2]}"
            ]
        })
    
    # Add rep metrics insight
    rep_metrics = analysis_results.get("rep_metrics", [])
    if rep_metrics and len(rep_metrics) > 0:
        # Find rep with highest average profit
        highest_avg_rep = max(rep_metrics, key=lambda x: x.get("average_profit", 0), default={})
        rep_name = highest_avg_rep.get("name", "")
        rep_average = format_currency(highest_avg_rep.get("average_profit", 0))
        rep_count = highest_avg_rep.get("sale_count", 0)
        
        insights.append({
            "title": "Highest Average Profit",
            "description": f"{rep_name} achieves the highest average profit per sale.",
            "employee": rep_name,
            "employeeTitle": "highest margin rep",
            "amount": rep_average,
            "percentage": None,
            "actionItems": [
                f"Completed {rep_count} sales.",
                f"Study {rep_name}'s negotiation techniques for training materials."
            ]
        })
    
    return insights

def generate_lead_source_insights(analysis_results: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Generate insights for lead source analysis.
    
    Args:
        analysis_results: Dictionary containing analysis results
        
    Returns:
        List of insight items
    """
    insights = []
    
    # Add summary insight
    summary = analysis_results.get("summary", {})
    if summary:
        total_sources = summary.get("total_sources", 0)
        average_profit = format_currency(summary.get("average_profit_per_source", 0))
        
        top_source = summary.get("top_source", {})
        top_source_name = top_source.get("name", "") if top_source else ""
        top_source_profit = format_currency(top_source.get("total_profit", 0)) if top_source else ""
        
        insights.append({
            "title": "Lead Source Performance",
            "description": f"Your dealership uses {total_sources} lead sources with an average profit of {average_profit} per source.",
            "amount": None,
            "percentage": None,
            "actionItems": [
                f"{top_source_name} is your top performing source with {top_source_profit} in profit.",
                "Consider reallocating marketing budget to top performing sources."
            ]
        })
    
    # Add source ROI insight
    source_roi = analysis_results.get("source_roi", [])
    if source_roi and len(source_roi) > 0:
        # Find source with highest ROI
        highest_roi_source = max(source_roi, key=lambda x: x.get("roi", 0), default={})
        source_name = highest_roi_source.get("name", "")
        source_roi_value = highest_roi_source.get("roi", 0)
        source_roi_formatted = f"{source_roi_value:.1f}%" if source_roi_value is not None else ""
        source_profit = format_currency(highest_roi_source.get("total_profit", 0))
        
        insights.append({
            "title": "Highest ROI Lead Source",
            "description": f"{source_name} provides the highest return on investment.",
            "amount": source_profit,
            "percentage": source_roi_formatted,
            "actionItems": [
                f"ROI: {source_roi_formatted}",
                f"Increase marketing investment in {source_name} for optimal returns."
            ]
        })
    
    # Add source metrics insight
    source_metrics = analysis_results.get("source_metrics", [])
    if source_metrics and len(source_metrics) > 0:
        # Find source with highest average profit
        highest_avg_source = max(source_metrics, key=lambda x: x.get("average_profit", 0), default={})
        source_name = highest_avg_source.get("name", "")
        source_average = format_currency(highest_avg_source.get("average_profit", 0))
        source_count = highest_avg_source.get("sale_count", 0)
        
        insights.append({
            "title": "Highest Quality Leads",
            "description": f"{source_name} provides leads with the highest average profit.",
            "amount": source_average,
            "percentage": None,
            "actionItems": [
                f"Generated {source_count} sales.",
                f"Focus on quality over quantity with {source_name} leads."
            ]
        })
    
    return insights

def generate_vehicle_insights(analysis_results: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Generate insights for vehicle analysis.
    
    Args:
        analysis_results: Dictionary containing analysis results
        
    Returns:
        List of insight items
    """
    insights = []
    
    # Add summary insight
    summary = analysis_results.get("summary", {})
    if summary:
        total_vehicles = summary.get("total_vehicles", 0)
        avg_days = summary.get("average_days_to_sell", 0)
        avg_days_formatted = f"{avg_days:.1f}" if avg_days is not None else ""
        
        top_make = summary.get("top_make", {})
        top_make_name = top_make.get("name", "") if top_make else ""
        top_make_profit = format_currency(top_make.get("total_profit", 0)) if top_make else ""
        
        top_model = summary.get("top_model", {})
        top_model_name = top_model.get("name", "") if top_model else ""
        
        insights.append({
            "title": "Vehicle Sales Performance",
            "description": f"Your dealership sold {total_vehicles} vehicles with an average time to sell of {avg_days_formatted} days.",
            "amount": None,
            "percentage": None,
            "actionItems": [
                f"{top_make_name} is your most profitable make with {top_make_profit} in profit.",
                f"{top_model_name} is your most profitable model."
            ]
        })
    
    # Add make performance insight
    make_performance = analysis_results.get("make_performance", [])
    if make_performance and len(make_performance) > 0:
        top_make = make_performance[0]
        make_name = top_make.get("make", "")
        make_profit = format_currency(top_make.get("total_profit", 0))
        make_count = top_make.get("sale_count", 0)
        
        insights.append({
            "title": "Top Performing Make",
            "description": f"{make_name} is your top performing vehicle make by profit.",
            "amount": make_profit,
            "percentage": None,
            "actionItems": [
                f"Sold {make_count} {make_name} vehicles.",
                f"Consider increasing {make_name} inventory allocation."
            ]
        })
    
    # Add model performance insight
    model_performance = analysis_results.get("model_performance", [])
    if model_performance and len(model_performance) > 0:
        top_model = model_performance[0]
        model_name = top_model.get("model", "")
        model_profit = format_currency(top_model.get("total_profit", 0))
        model_average = format_currency(top_model.get("average_profit", 0))
        
        insights.append({
            "title": "Top Performing Model",
            "description": f"{model_name} is your top performing vehicle model by profit.",
            "amount": model_profit,
            "percentage": None,
            "actionItems": [
                f"Average profit per sale: {model_average}.",
                f"Focus sales team training on {model_name} features and benefits."
            ]
        })
    
    # Add vehicle metrics insight
    vehicle_metrics = analysis_results.get("vehicle_metrics", [])
    if vehicle_metrics and len(vehicle_metrics) > 0:
        # Find vehicle with fastest sales
        fastest_selling = min(vehicle_metrics, key=lambda x: x.get("average_days_to_sell", float('inf')), default={})
        if "average_days_to_sell" in fastest_selling:
            vehicle_type = fastest_selling.get("type", "")
            days_to_sell = fastest_selling.get("average_days_to_sell", 0)
            days_formatted = f"{days_to_sell:.1f}" if days_to_sell is not None else ""
            
            insights.append({
                "title": "Fastest Selling Vehicle",
                "description": f"{vehicle_type} sells the fastest on your lot.",
                "amount": None,
                "percentage": None,
                "actionItems": [
                    f"Average days to sell: {days_formatted}",
                    f"Maintain optimal inventory levels of {vehicle_type} to maximize turnover."
                ]
            })
    
    return insights

def answer_question(df, question: str) -> Dict[str, Any]:
    """
    Answer a specific question about the data.
    
    Args:
        df: DataFrame containing the data
        question: Question to answer
        
    Returns:
        Dictionary containing the answer, insights, and chart data
    """
    logger.info(f"Answering question: {question}")
    
    # Normalize question
    normalized_question = question.lower().strip()
    
    # Determine intent based on question
    intent = determine_intent(normalized_question)
    
    # Analyze data based on intent
    from app.services.analyzer import analyze_data
    analysis_results = analyze_data(df, intent)
    
    # Generate insights
    insights = generate_insights(analysis_results, intent)
    
    # Generate answer text
    answer = generate_answer_text(normalized_question, analysis_results, intent)
    
    return {
        "answer": answer,
        "insights": insights,
        "chart_data": analysis_results.get("chart_data"),
        "chart_type": analysis_results.get("chart_type", "bar")
    }

def determine_intent(question: str) -> str:
    """
    Determine the intent based on the question.
    
    Args:
        question: Question to analyze
        
    Returns:
        Intent string
    """
    # Check for sales-related questions
    if any(term in question for term in ['sales', 'revenue', 'sold', 'selling', 'sell']):
        return "sales_analysis"
    
    # Check for profit-related questions
    if any(term in question for term in ['profit', 'margin', 'profitable', 'earnings', 'money']):
        return "profit_analysis"
    
    # Check for rep-related questions
    if any(term in question for term in ['rep', 'representative', 'salesperson', 'sales person', 'team']):
        return "rep_performance"
    
    # Check for lead source-related questions
    if any(term in question for term in ['lead', 'source', 'marketing', 'advertisement', 'campaign']):
        return "lead_source_analysis"
    
    # Check for vehicle-related questions
    if any(term in question for term in ['vehicle', 'car', 'make', 'model', 'brand']):
        return "vehicle_analysis"
    
    # Default to general analysis
    return "general_analysis"

def generate_answer_text(question: str, analysis_results: Dict[str, Any], intent: str) -> str:
    """
    Generate answer text based on the question and analysis results.
    
    Args:
        question: Original question
        analysis_results: Dictionary containing analysis results
        intent: Analysis intent
        
    Returns:
        Answer text
    """
    # Extract key information based on intent
    if intent == "sales_analysis":
        return generate_sales_answer(question, analysis_results)
    elif intent == "profit_analysis":
        return generate_profit_answer(question, analysis_results)
    elif intent == "rep_performance":
        return generate_rep_answer(question, analysis_results)
    elif intent == "lead_source_analysis":
        return generate_lead_source_answer(question, analysis_results)
    elif intent == "vehicle_analysis":
        return generate_vehicle_answer(question, analysis_results)
    else:
        return generate_general_answer(question, analysis_results)

def generate_sales_answer(question: str, analysis_results: Dict[str, Any]) -> str:
    """
    Generate answer text for sales-related questions.
    
    Args:
        question: Original question
        analysis_results: Dictionary containing analysis results
        
    Returns:
        Answer text
    """
    summary = analysis_results.get("summary", {})
    total_sales = format_currency(summary.get("total_sales", 0))
    average_sale = format_currency(summary.get("average_sale_price", 0))
    
    # Check for specific question patterns
    if re.search(r'highest|top|best|most', question):
        if re.search(r'(sales\s*rep|salesperson|representative)', question):
            # Question about top sales rep
            sales_by_rep = analysis_results.get("sales_by_rep", [])
            if sales_by_rep and len(sales_by_rep) > 0:
                top_rep = sales_by_rep[0]
                rep_name = top_rep.get("name", "")
                rep_sales = format_currency(top_rep.get("total_sales", 0))
                rep_count = top_rep.get("sale_count", 0)
                
                return f"Your top sales representative is {rep_name} with {rep_sales} in total sales. They completed {rep_count} sales with an average of {format_currency(top_rep.get('average_sale', 0))} per sale."
        
        if re.search(r'(vehicle|car|model|make)', question):
            # Question about top vehicle
            sales_by_vehicle = analysis_results.get("sales_by_vehicle_type", [])
            if sales_by_vehicle and len(sales_by_vehicle) > 0:
                top_vehicle = sales_by_vehicle[0]
                vehicle_type = top_vehicle.get("type", "")
                vehicle_sales = format_currency(top_vehicle.get("total_sales", 0))
                vehicle_count = top_vehicle.get("sale_count", 0)
                
                return f"Your top selling vehicle is the {vehicle_type} with {vehicle_sales} in total sales. You sold {vehicle_count} units with an average price of {format_currency(top_vehicle.get('average_sale', 0))} per vehicle."
    
    if re.search(r'total|overall', question):
        return f"Your dealership generated {total_sales} in total sales. The average sale price was {average_sale}."
    
    if re.search(r'average|mean', question):
        return f"The average sale price at your dealership is {average_sale}."
    
    # Default answer
    return f"Based on your sales data, your dealership generated {total_sales} in total sales with an average sale price of {average_sale}. I've provided detailed insights below."

def generate_profit_answer(question: str, analysis_results: Dict[str, Any]) -> str:
    """
    Generate answer text for profit-related questions.
    
    Args:
        question: Original question
        analysis_results: Dictionary containing analysis results
        
    Returns:
        Answer text
    """
    summary = analysis_results.get("summary", {})
    total_profit = format_currency(summary.get("total_profit", 0))
    average_profit = format_currency(summary.get("average_profit", 0))
    profit_margin = summary.get("profit_margin", 0)
    profit_margin_formatted = f"{profit_margin:.1f}%" if profit_margin is not None else ""
    
    # Check for specific question patterns
    if re.search(r'highest|top|best|most', question):
        if re.search(r'(sales\s*rep|salesperson|representative)', question):
            # Question about top profit rep
            profit_by_rep = analysis_results.get("profit_by_rep", [])
            if profit_by_rep and len(profit_by_rep) > 0:
                top_rep = profit_by_rep[0]
                rep_name = top_rep.get("name", "")
                rep_profit = format_currency(top_rep.get("total_profit", 0))
                rep_average = format_currency(top_rep.get("average_profit", 0))
                
                return f"Your top profit-generating sales representative is {rep_name} with {rep_profit} in total profit. Their average profit per sale is {rep_average}."
        
        if re.search(r'(lead\s*source|source|marketing)', question):
            # Question about top lead source
            profit_by_source = analysis_results.get("profit_by_lead_source", [])
            if profit_by_source and len(profit_by_source) > 0:
                top_source = profit_by_source[0]
                source_name = top_source.get("name", "")
                source_profit = format_currency(top_source.get("total_profit", 0))
                source_average = format_currency(top_source.get("average_profit", 0))
                
                return f"Your most profitable lead source is {source_name} with {source_profit} in total profit. The average profit per sale from this source is {source_average}."
        
        if re.search(r'(vehicle|car|model|make)', question):
            # Question about top vehicle
            profit_by_vehicle = analysis_results.get("profit_by_vehicle_type", [])
            if profit_by_vehicle and len(profit_by_vehicle) > 0:
                top_vehicle = profit_by_vehicle[0]
                vehicle_type = top_vehicle.get("type", "")
                vehicle_profit = format_currency(top_vehicle.get("total_profit", 0))
                vehicle_average = format_currency(top_vehicle.get("average_profit", 0))
                
                return f"Your most profitable vehicle is the {vehicle_type} with {vehicle_profit} in total profit. The average profit per sale for this vehicle is {vehicle_average}."
    
    if re.search(r'total|overall', question):
        return f"Your dealership generated {total_profit} in total profit with an overall profit margin of {profit_margin_formatted}."
    
    if re.search(r'average|mean', question):
        return f"The average profit per sale at your dealership is {average_profit}."
    
    if re.search(r'margin', question):
        return f"Your dealership's overall profit margin is {profit_margin_formatted}."
    
    # Default answer
    return f"Based on your data, your dealership generated {total_profit} in total profit with an average profit of {average_profit} per sale. The overall profit margin is {profit_margin_formatted}. I've provided detailed insights below."

def generate_rep_answer(question: str, analysis_results: Dict[str, Any]) -> str:
    """
    Generate answer text for sales representative-related questions.
    
    Args:
        question: Original question
        analysis_results: Dictionary containing analysis results
        
    Returns:
        Answer text
    """
    summary = analysis_results.get("summary", {})
    total_reps = summary.get("total_reps", 0)
    
    # Check for specific question patterns
    if re.search(r'highest|top|best|most', question):
        top_rep = summary.get("top_rep", {})
        if top_rep:
            rep_name = top_rep.get("name", "")
            rep_profit = format_currency(top_rep.get("total_profit", 0))
            rep_count = top_rep.get("sale_count", 0)
            
            return f"Your top performing sales representative is {rep_name} with {rep_profit} in total profit from {rep_count} sales."
    
    if re.search(r'leaderboard|ranking|rank|compare', question):
        rep_leaderboard = analysis_results.get("rep_leaderboard", [])
        if rep_leaderboard and len(rep_leaderboard) >= 3:
            top_reps = rep_leaderboard[:3]
            rep_names = [rep.get("name", "") for rep in top_reps]
            rep_profits = [format_currency(rep.get("total_profit", 0)) for rep in top_reps]
            
            return f"Your top 3 sales representatives by profit are: 1. {rep_names[0]} with {rep_profits[0]}, 2. {rep_names[1]} with {rep_profits[1]}, and 3. {rep_names[2]} with {rep_profits[2]}."
    
    if re.search(r'average|mean', question):
        average_profit = format_currency(summary.get("average_profit_per_rep", 0))
        return f"The average profit generated per sales representative is {average_profit}."
    
    # Default answer
    return f"Your sales team consists of {total_reps} representatives. I've provided detailed performance insights for your team below."

def generate_lead_source_answer(question: str, analysis_results: Dict[str, Any]) -> str:
    """
    Generate answer text for lead source-related questions.
    
    Args:
        question: Original question
        analysis_results: Dictionary containing analysis results
        
    Returns:
        Answer text
    """
    summary = analysis_results.get("summary", {})
    total_sources = summary.get("total_sources", 0)
    
    # Check for specific question patterns
    if re.search(r'highest|top|best|most', question):
        if re.search(r'roi|return|investment', question):
            # Question about highest ROI source
            source_roi = analysis_results.get("source_roi", [])
            if source_roi and len(source_roi) > 0:
                highest_roi_source = max(source_roi, key=lambda x: x.get("roi", 0), default={})
                source_name = highest_roi_source.get("name", "")
                source_roi_value = highest_roi_source.get("roi", 0)
                source_roi_formatted = f"{source_roi_value:.1f}%" if source_roi_value is not None else ""
                source_profit = format_currency(highest_roi_source.get("total_profit", 0))
                
                return f"Your highest ROI lead source is {source_name} with a return on investment of {source_roi_formatted}. This source generated {source_profit} in total profit."
        else:
            # Question about most profitable source
            top_source = summary.get("top_source", {})
            if top_source:
                source_name = top_source.get("name", "")
                source_profit = format_currency(top_source.get("total_profit", 0))
                source_count = top_source.get("sale_count", 0)
                
                return f"Your most profitable lead source is {source_name} with {source_profit} in total profit from {source_count} sales."
    
    if re.search(r'compare|comparison', question):
        source_metrics = analysis_results.get("source_metrics", [])
        if source_metrics and len(source_metrics) >= 3:
            top_sources = source_metrics[:3]
            source_names = [source.get("name", "") for source in top_sources]
            source_profits = [format_currency(source.get("total_profit", 0)) for source in top_sources]
            
            return f"Your top 3 lead sources by profit are: 1. {source_names[0]} with {source_profits[0]}, 2. {source_names[1]} with {source_profits[1]}, and 3. {source_names[2]} with {source_profits[2]}."
    
    # Default answer
    return f"Your dealership uses {total_sources} different lead sources. I've provided detailed performance insights for your lead sources below."

def generate_vehicle_answer(question: str, analysis_results: Dict[str, Any]) -> str:
    """
    Generate answer text for vehicle-related questions.
    
    Args:
        question: Original question
        analysis_results: Dictionary containing analysis results
        
    Returns:
        Answer text
    """
    summary = analysis_results.get("summary", {})
    total_vehicles = summary.get("total_vehicles", 0)
    avg_days = summary.get("average_days_to_sell", 0)
    avg_days_formatted = f"{avg_days:.1f}" if avg_days is not None else ""
    
    # Check for specific question patterns
    if re.search(r'highest|top|best|most', question):
        if re.search(r'make|brand', question):
            # Question about top make
            top_make = summary.get("top_make", {})
            if top_make:
                make_name = top_make.get("name", "")
                make_profit = format_currency(top_make.get("total_profit", 0))
                make_count = top_make.get("sale_count", 0)
                
                return f"Your most profitable vehicle make is {make_name} with {make_profit} in total profit from {make_count} sales."
        
        if re.search(r'model', question):
            # Question about top model
            top_model = summary.get("top_model", {})
            if top_model:
                model_name = top_model.get("name", "")
                model_profit = format_currency(top_model.get("total_profit", 0))
                model_count = top_model.get("sale_count", 0)
                
                return f"Your most profitable vehicle model is the {model_name} with {model_profit} in total profit from {model_count} sales."
    
    if re.search(r'fast|quick|days', question):
        # Question about fastest selling vehicles
        vehicle_metrics = analysis_results.get("vehicle_metrics", [])
        if vehicle_metrics and len(vehicle_metrics) > 0:
            # Find vehicle with fastest sales
            fastest_selling = min(vehicle_metrics, key=lambda x: x.get("average_days_to_sell", float('inf')), default={})
            if "average_days_to_sell" in fastest_selling:
                vehicle_type = fastest_selling.get("type", "")
                days_to_sell = fastest_selling.get("average_days_to_sell", 0)
                days_formatted = f"{days_to_sell:.1f}" if days_to_sell is not None else ""
                
                return f"Your fastest selling vehicle is the {vehicle_type} with an average of {days_formatted} days to sell. The overall average for all vehicles is {avg_days_formatted} days."
    
    # Default answer
    return f"Your dealership sold {total_vehicles} vehicles with an average time to sell of {avg_days_formatted} days. I've provided detailed insights about your vehicle performance below."

def generate_general_answer(question: str, analysis_results: Dict[str, Any]) -> str:
    """
    Generate answer text for general questions.
    
    Args:
        question: Original question
        analysis_results: Dictionary containing analysis results
        
    Returns:
        Answer text
    """
    summary = analysis_results.get("summary", {})
    total_sales = format_currency(summary.get("total_sales", 0))
    total_profit = format_currency(summary.get("total_profit", 0))
    average_profit = format_currency(summary.get("average_profit", 0))
    
    # Check for specific question patterns
    if re.search(r'summary|overview', question):
        return f"Your dealership generated {total_sales} in sales and {total_profit} in profit. The average profit per sale is {average_profit}. I've provided detailed insights below."
    
    # Default answer
    return f"Based on your data, I've analyzed your dealership's performance and provided key insights below. Your dealership generated {total_profit} in total profit with an average of {average_profit} per sale."

def generate_action_items_for_metric(title: str, value: str, metric_value: str) -> List[str]:
    """
    Generate action items for a metric.
    
    Args:
        title: Metric title
        value: Metric value
        metric_value: Formatted metric value
        
    Returns:
        List of action items
    """
    action_items = []
    
    if "Sales Rep" in title or "Representative" in title:
        action_items.append(f"Study {value}'s sales strategies for team training.")
        action_items.append(f"Analyze their lead source performance for optimization.")
    
    elif "Lead Source" in title:
        action_items.append(f"Increase marketing investment in {value}.")
        action_items.append(f"Analyze customer demographics from this source.")
    
    elif "Vehicle" in title or "Make" in title or "Model" in title:
        action_items.append(f"Increase inventory allocation for {value}.")
        action_items.append(f"Train sales team on {value} features and benefits.")
    
    else:
        # Generic action items
        action_items.append("Analyze trends over time for deeper insights.")
        action_items.append("Compare with industry benchmarks for context.")
    
    return action_items

def format_currency(value: float) -> str:
    """
    Format a value as currency.
    
    Args:
        value: Value to format
        
    Returns:
        Formatted currency string
    """
    if value is None:
        return "$0"
    
    try:
        # Format with commas and dollar sign
        return "${:,.2f}".format(value)
    except:
        # Return as is if formatting fails
        return str(value)
