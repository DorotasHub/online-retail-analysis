import pandas as pd
import json

df = pd.read_excel("data/online-retail-dataset.xlsx")

print(df.head())
print(df.info())

# show columns with null values
null_info = df.isnull().sum().reset_index()
null_info.columns = ['Column', 'Null Count']
null_info = null_info[null_info['Null Count'] > 0]
print(null_info)

# show duplicates (excluding first occurrence)
duplicates = df[df.duplicated()].copy()
cols_with_nulls = ['Description', 'CustomerID']
merge_columns = [col for col in df.columns if col not in cols_with_nulls]
duplicate_counts = (
    duplicates.groupby(merge_columns)
    .size()
    .reset_index(name='DuplicateCount')
)
duplicates = duplicates.merge(duplicate_counts, on=merge_columns, how='left')
duplicates = duplicates.sort_values(by='DuplicateCount', ascending=False).reset_index(drop=True)
print(duplicates)

# drop dupes
cdf = df.drop_duplicates().copy()
print(cdf)

# convert dtypes
cdf['InvoiceNo'] = cdf['InvoiceNo'].astype('string')
cdf['StockCode'] = cdf['StockCode'].astype('string')
cdf['Description'] = cdf['Description'].astype('string')
cdf['Country'] = cdf['Country'].astype('string')
cdf['InvoiceDate'] = pd.to_datetime(cdf['InvoiceDate'])
cdf['CustomerID'] = pd.to_numeric(cdf['CustomerID'], errors='coerce').astype('Int64')


# standardize descriptions
cdf['StockCode'] = cdf['StockCode'].str.upper()
cdf['Original_Description'] = cdf['Description']
cdf_with_null_desc = cdf.copy()
cdf_with_null_desc['Description'] = cdf_with_null_desc['Description'].fillna('NaN')
grouped = (
    cdf_with_null_desc.groupby(['StockCode', 'Description'])
    .size()
    .reset_index(name='Count')
)

# dict with stockcode & corresponding descriptions + count of occurrences per 
# description. description with highest count will be used for nulls & as 
# standardized description 
stockcodes = {}
for _, row in grouped.iterrows():
    stockcode = row['StockCode']
    description = row['Description']
    count = row['Count']

    if stockcode not in stockcodes:
        stockcodes[stockcode] = {}
    stockcodes[stockcode][description] = count

# writing stockcodes dict to json file for demo
with open('stockcodes.json', 'w') as f:
    json.dump(stockcodes, f, indent=4)

most_common_desc = {
    code: max(descs.items(), key=lambda x: x[1])[0]
    for code, descs in stockcodes.items()
}
# writing most_common_desc per stockcode dict to json file for demo
with open('standardized_descs.json', 'w') as f:
    json.dump(most_common_desc, f, indent=4)

cdf['Standardized_Description'] = cdf['StockCode'].map(most_common_desc).astype('string')
cdf['Standardized_Description'] = cdf['Standardized_Description'].replace('NaN', pd.NA)
cdf['Description'] = cdf['Standardized_Description'].fillna(cdf['Original_Description'])
cdf.drop(columns=['Standardized_Description'], inplace=True)
print(cdf)

# show txns with populated desc
filled_desc = cdf[cdf['Description'].notna() & cdf['Original_Description'].isna()].copy()
print(filled_desc)

# see updated nulls
null_info = cdf.isnull().sum().reset_index()
null_info.columns = ['Column', 'Null Count']
null_info = null_info[null_info['Null Count'] > 0]
print(null_info)

# filter txns with missing descriptions
missing_descriptions = cdf[cdf['Description'].isna()].copy()
print(missing_descriptions)
# cdf = cdf.dropna(subset=['Description'])

# filter txns with missing customerids
missing_customerids = cdf[cdf['CustomerID'].isna()].copy()
print(missing_customerids)
# cdf = cdf.dropna(subset=['CustomerID'])