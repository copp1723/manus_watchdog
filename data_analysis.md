# Watchdog AI - Data Analysis

## Sample Data Files Analysis

### File 1: "watchdog test data .csv"
This file contains basic dealership sales data with the following fields:

- `lead_source`: Origin of the lead (e.g., NeoIdentity, AutoTrader, Website)
- `listing_price`: Original price of the vehicle (formatted with $ and commas)
- `sold_price`: Final selling price (formatted with $ and commas)
- `profit`: Profit from the sale (formatted with $ and commas)
- `expense`: Expenses associated with the sale (some with $ prefix, some without)
- `sales_rep_name`: Name of the sales representative
- `vehicle_year`: Year the vehicle was manufactured
- `vehicle_make`: Make of the vehicle (e.g., GMC, Honda, Toyota)
- `vehicle_model`: Model of the vehicle (e.g., Sierra, Accord, Camry)
- `days_to_close`: Number of days from lead to sale completion

### File 2: "Copy of April 2024 - ROI Calc - Sold Log.csv"
This file contains more comprehensive dealership data with the following fields:

- Customer information: IDs, names, contact details, addresses
- Lead tracking: Lead source, creation date, status
- Sales details: Deal number, selling price, gross profit breakdowns
- Vehicle information: Year, make, model, VIN, stock number, inventory type
- Sales rep information: Name, split sales rep
- Dates: Sold date, lead created date

## Common Fields and Data Patterns

### Common Fields Between Files:
- Lead source information
- Sales representative names
- Vehicle details (year, make, model)
- Pricing information (though formatted differently)
- Profit information

### Data Patterns:
1. **Monetary Values**: Inconsistent formatting ($, commas, decimal places)
2. **Dates**: Different formats across files
3. **Lead Sources**: Common sources appear in both files (AutoTrader, Website)
4. **Sales Performance**: Both files track sales rep performance
5. **Vehicle Information**: Consistent tracking of year, make, model

## Data Cleaning Requirements

1. **Monetary Value Standardization**:
   - Remove $ symbols and commas
   - Convert to numeric values
   - Handle missing or zero values

2. **Date Standardization**:
   - Parse different date formats
   - Convert to consistent ISO format
   - Calculate time-based metrics (days to close, etc.)

3. **Text Field Normalization**:
   - Standardize lead source names
   - Normalize sales rep names
   - Handle missing values

4. **Data Validation**:
   - Check for outliers in pricing and profit data
   - Validate vehicle information
   - Ensure required fields are present

## Potential Insights to Extract

1. **Sales Performance Metrics**:
   - Top performing sales representatives
   - Average profit per sale
   - Profit trends over time

2. **Lead Source Effectiveness**:
   - Conversion rates by lead source
   - ROI by marketing channel
   - Cost per acquisition

3. **Inventory Analysis**:
   - Best-selling vehicle makes and models
   - Profit margins by vehicle type
   - Days to sell by vehicle category

4. **Temporal Analysis**:
   - Seasonal sales patterns
   - Day of week/time of day patterns
   - Lead time to conversion

5. **Customer Insights**:
   - Geographic distribution of customers
   - Repeat customer identification
   - Customer preferences by region

## Data Processing Approach

1. **Initial Parsing and Validation**:
   - Detect file format and headers
   - Validate required columns
   - Check for data integrity issues

2. **Transformation Pipeline**:
   - Clean and normalize data
   - Convert data types appropriately
   - Handle missing values

3. **Analysis Engine**:
   - Calculate key metrics
   - Generate insights based on user questions
   - Prepare visualization data

4. **Response Generation**:
   - Convert analysis results to natural language
   - Generate actionable recommendations
   - Format for presentation in UI

This analysis will inform the architecture and implementation of the Watchdog AI system, ensuring it can handle the variety of dealership data formats while providing valuable insights through a simple interface.
