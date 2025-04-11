# FOIL case study: online retail data analysis

Examine:
Dataset size and structure
Data types of each column
Missing values and inconsistencies
Basic distribution of key variables

Check for null values, especially in InvoiceNo, StockCode, Quantity, and Price
Validate quantity and price ranges for outliers or negative values
Convert any timestamp data to proper datetime format
Confirm date ranges and format consistency
Create derived fields like total purchase amount (Quantity × Price)
Filter out canceled orders (those with invoice numbers starting with "C")

