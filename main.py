import pandas as pd
import json

df = pd.read_excel("data/online-retail-dataset.xlsx")

# print(df)
# print(df.head())
print(df.info())
# print(df.describe())

"""See Duplicates"""
duplicates = df[df.duplicated()]
# print("DUPES TO BE DROPPED")
# print(duplicates)

"""Remove duplicates"""
cdf = df.drop_duplicates()


""" Missing/Null Values """
null_info = cdf.isnull().sum().reset_index()
null_info.columns = ['Column', 'Null Count']
null_info = null_info[null_info['Null Count'] > 0]
# print(null_info)

null_rows = cdf[cdf.isnull().any(axis=1)]
null_rows

"""Standardize descriptions based on the most frequent description for the same StockCode."""
cdf = cdf.copy()
cdf['Original_Description'] = cdf['Description']
conflicts = cdf.groupby('StockCode')['Description'].nunique()
conflicts = conflicts[conflicts > 1]
conflict_codes = conflicts.index.tolist()

grouped = (
    cdf[cdf['StockCode'].isin(conflict_codes)]
    .groupby(['StockCode', 'Description'])
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

# """Write to json file for visualization"""
# with open('output.json', 'w') as f:
#     json.dump(stockcodes, f, indent=4)

most_common_desc = {
    code: max(descs.items(), key=lambda x: x[1])[0]
    for code, descs in stockcodes.items()
}

"""Replace all descriptions based on the most common one per StockCode"""
cdf['Description'] = cdf['StockCode'].map(most_common_desc).fillna(cdf['Description'])

"""Drop remaining NaNs where Description wasn't populated based on stockcode"""
cdf = cdf[~(cdf['Description'].isna() & cdf['Original_Description'].isna())]

filled_from_nulls = cdf[
    cdf['Original_Description'].isna() & cdf['Description'].notna()
]
print(filled_from_nulls)

# See which rows changed
changed = cdf[cdf['Original_Description'] != cdf['Description']]
print(changed)


# # check nulls
# null_info = cdf.isnull().sum().reset_index()
# null_info.columns = ['Column', 'Null Count']
# null_info = null_info[null_info['Null Count'] > 0]
# print(null_info)

"""Tag rows with missing CustomerIDs"""
cdf['HasCustomerID'] = cdf['CustomerID'].notna()
print(cdf)

# # check nulls ==> should be none/empty
# null_info = cdf.isnull().sum().reset_index()
# null_info.columns = ['Column', 'Null Count']
# null_info = null_info[null_info['Null Count'] > 0]
# print(null_info)

"""Convert dtypes"""
cdf['InvoiceNo'] = cdf['InvoiceNo'].astype('string')
cdf['StockCode'] = cdf['StockCode'].astype('string')
cdf['Description'] = cdf['Description'].astype('string')
cdf['Country'] = cdf['Country'].astype('string')
cdf['InvoiceDate'] = pd.to_datetime(cdf['InvoiceDate'])
cdf['CustomerID'] = pd.to_numeric(cdf['CustomerID'], errors='coerce').astype('Int64')
cdf['Original_Description'] = cdf['Original_Description'].astype('string')

cdf.info()
cdf.head()
cdf.describe()
# # Drop rows with null values
# df_cleaned.dropna(inplace=True)
# df_cleaned.info()

# Copy and clean
# cdf = df.copy()

# # find which columns have empty/missing values 
# # print(cdf.isnull())

# # Remove rows with missing CustomerID
# cdf.dropna(subset=['CustomerID'], inplace=True)

# Add Sales column
# cdf['Sales'] = cdf['Quantity'] * cdf['UnitPrice']

# # Split into purchases and returns
# df_purchases = cdf[cdf['Quantity'] > 0].copy()
# top_selling = df_purchases.groupby('Description')['Sales'].sum().sort_values(ascending=False).head(10)
# top_selling

# # Top 10 Returned Products
# df_returns = cdf[cdf['Quantity'] < 0].copy()
# top_returned = df_returns.groupby('Description')['Quantity'].sum().abs().sort_values(ascending=False).head(10)
# top_returned
