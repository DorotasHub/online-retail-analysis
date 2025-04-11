import pandas as pd

df = pd.read_excel("data/online-retail-dataset.xlsx")

# Convert types
cdf = df.copy()
cdf['InvoiceNo'] = cdf['InvoiceNo'].astype('string')
cdf['StockCode'] = cdf['StockCode'].astype('string')
cdf['Description'] = cdf['Description'].astype('string')
cdf['Country'] = cdf['Country'].astype('string')
cdf['CustomerID'] = pd.to_numeric(cdf['CustomerID'], errors='coerce').astype('Int64')

# Standardize descriptions
cdf['StockCode'] = cdf['StockCode'].str.upper()
cdf['OriginalDescription'] = cdf['Description']
cdf_with_null_desc = cdf.copy()
cdf_with_null_desc['Description'] = cdf_with_null_desc['Description'].fillna('NaN')
grouped = (
    cdf_with_null_desc.groupby(['StockCode', 'Description'])
    .size()
    .reset_index(name='Count')
)
stockcodes = {}
for _, row in grouped.iterrows():
    stockcode = row['StockCode']
    description = row['Description']
    count = row['Count']

    if stockcode not in stockcodes:
        stockcodes[stockcode] = {}

    stockcodes[stockcode][description] = count
# # write dict to file for viz    
# with open('stockcodes.json', 'w') as f:
#     json.dump(stockcodes, f, indent=4)

# create dict mapping stockcode to most common desc
most_common_desc = {
    code: max(descs.items(), key=lambda x: x[1])[0]
    for code, descs in stockcodes.items()
}
# with open('most_common_desc.json', 'w') as f:
#     json.dump(most_common_desc, f, indent=4)

cdf['StandardizedDescription'] = cdf['StockCode'].map(most_common_desc).astype('string')
cdf['StandardizedDescription'] = cdf['StandardizedDescription'].replace('NaN', pd.NA)
cdf['Description'] = cdf['StandardizedDescription'].fillna(cdf['OriginalDescription'])
cdf.drop(columns=['StandardizedDescription'], inplace=True)

# Add total price column
cdf['TotalPrice'] = cdf['Quantity'] * cdf['UnitPrice']

# Convert dates and extract time features
cdf['InvoiceDate'] = pd.to_datetime(cdf['InvoiceDate'], errors='coerce')
cdf['Year'] = cdf['InvoiceDate'].dt.year
cdf['Month'] = cdf['InvoiceDate'].dt.month
cdf['MonthYear'] = cdf['InvoiceDate'].dt.to_period('M')
cdf['YearQuarter'] = df['InvoiceDate'].dt.to_period('Q')
cdf['Time'] = cdf['InvoiceDate'].dt.time
cdf['Hour'] = cdf['InvoiceDate'].dt.hour
cdf['Minute'] = cdf['InvoiceDate'].dt.minute
cdf['Weekday'] = cdf['InvoiceDate'].dt.day_name()
cdf['TimeOfDay'] = pd.cut(cdf['Hour'], bins=[0, 6, 12, 18, 24], 
labels=['Night', 'Morning', 'Afternoon', 'Evening'])

# Tag missing values
cdf['MissingCustomerID'] = cdf['CustomerID'].isna()
cdf['MissingDescription'] = cdf['Description'].isna()

# Tag Valid Sale Transactions
cdf['IsValidSale'] = (
    (cdf['Quantity'] > 0) &
    (cdf['UnitPrice'] > 0) &
    (cdf['InvoiceNo'].str.startswith('C') == False)
)

# Tag Valid Reversals (Cancellations or Returns)
cdf['IsValidReturn'] = (
    (cdf['Quantity'] < 0) &
    (cdf['UnitPrice'] > 0) &
    (cdf['InvoiceNo'].str.startswith('C'))
)

# Remove duplicates
cdf = cdf.drop_duplicates()

# Grab only valid txns
valid_txns = cdf[cdf['IsValidSale'] | cdf['IsValidReturn']].copy()

# filter out non-product transactions
keywords = ["FEE", "ADJUST", "POSTAGE", "CREDIT", "CHARGES", "SAMPLES", "Discount"]
pattern = '|'.join(keywords)

sales_df = valid_txns[valid_txns["IsValidSale"]].copy()
filtered_sales_df = sales_df[~sales_df["Description"].str.contains(pattern, case=False, na=False)]
filtered_sales_df.to_csv("data/filtered_sales.csv", index=False)

returns_df = valid_txns[valid_txns["IsValidReturn"]].copy()
filtered_returns_df = returns_df[~returns_df["Description"].str.contains(pattern, case=False, na=False)]
filtered_returns_df.to_csv("data/filtered_returns.csv", index=False)