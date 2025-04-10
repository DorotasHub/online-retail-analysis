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
most_common_desc = {
    code: max(descs.items(), key=lambda x: x[1])[0]
    for code, descs in stockcodes.items()
}
cdf['StandardizedDescription'] = cdf['StockCode'].map(most_common_desc).astype('string')
cdf['StandardizedDescription'] = cdf['StandardizedDescription'].replace('NaN', pd.NA)
cdf['Description'] = cdf['StandardizedDescription'].fillna(cdf['OriginalDescription'])
cdf.drop(columns=['StandardizedDescription'], inplace=True)

# Flag missing values
cdf['MissingCustomerID'] = cdf['CustomerID'].isna()
cdf['MissingDescription'] = cdf['Description'].isna()

# Flag cancelled transactions, returns and free items
cdf['IsCancelled'] = cdf['InvoiceNo'].astype(str).str.startswith('C')
cdf['IsReturn'] = cdf['Quantity'] < 0
cdf['IsFreeItem'] = cdf['UnitPrice'] == 0

# Add total price column
cdf['TotalPrice'] = cdf['Quantity'] * cdf['UnitPrice']

# Convert dates and extract time features
cdf['InvoiceDate'] = pd.to_datetime(cdf['InvoiceDate'], errors='coerce')
cdf['Year'] = cdf['InvoiceDate'].dt.year
cdf['Month'] = cdf['InvoiceDate'].dt.month
cdf['MonthYear'] = cdf['InvoiceDate'].dt.to_period('M')
cdf['YearQuarter'] = df['InvoiceDate'].dt.to_period('Q')
cdf['Hour'] = cdf['InvoiceDate'].dt.hour
cdf['Minute'] = cdf['InvoiceDate'].dt.minute
cdf['Time'] = cdf['InvoiceDate'].dt.time
cdf['TimePeriod'] = pd.cut(cdf['Hour'], bins=[0, 6, 12, 18, 24], 
labels=['Night', 'Morning', 'Afternoon', 'Evening'])

# Remove duplicates
cdf = cdf.drop_duplicates()

cdf.to_csv("data/cleaned_online_retail_dataset.csv", index=False)