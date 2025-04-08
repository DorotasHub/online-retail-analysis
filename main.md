<class 'pandas.core.frame.DataFrame'>
RangeIndex: 541909 entries, 0 to 541908
Data columns (total 8 columns):
 #   Column       Non-Null Count   Dtype         
---  ------       --------------   -----         
 0   InvoiceNo    541909 non-null  object        
 1   StockCode    541909 non-null  object        
 2   Description  540455 non-null  object        
 3   Quantity     541909 non-null  int64         
 4   InvoiceDate  541909 non-null  datetime64[ns]
 5   UnitPrice    541909 non-null  float64       
 6   CustomerID   406829 non-null  float64       
 7   Country      541909 non-null  object        
dtypes: datetime64[ns](1), float64(2), int64(1), object(4)
memory usage: 33.1+ MB
None
ALL DUPES
       InvoiceNo StockCode  ... CustomerID         Country
485       536409     22111  ...    17908.0  United Kingdom
489       536409     22866  ...    17908.0  United Kingdom
494       536409     21866  ...    17908.0  United Kingdom
517       536409     21866  ...    17908.0  United Kingdom
521       536409     22900  ...    17908.0  United Kingdom
...          ...       ...  ...        ...             ...
541675    581538     22068  ...    14446.0  United Kingdom
541689    581538     23318  ...    14446.0  United Kingdom
541692    581538     22992  ...    14446.0  United Kingdom
541699    581538     22694  ...    14446.0  United Kingdom
541701    581538     23343  ...    14446.0  United Kingdom

[10147 rows x 8 columns]
DUPES TO BE DROPPED
       InvoiceNo StockCode  ... CustomerID         Country
517       536409     21866  ...    17908.0  United Kingdom
527       536409     22866  ...    17908.0  United Kingdom
537       536409     22900  ...    17908.0  United Kingdom
539       536409     22111  ...    17908.0  United Kingdom
555       536412     22327  ...    17920.0  United Kingdom
...          ...       ...  ...        ...             ...
541675    581538     22068  ...    14446.0  United Kingdom
541689    581538     23318  ...    14446.0  United Kingdom
541692    581538     22992  ...    14446.0  United Kingdom
541699    581538     22694  ...    14446.0  United Kingdom
541701    581538     23343  ...    14446.0  United Kingdom

[5268 rows x 8 columns]
any dupes?:
Empty DataFrame
Columns: [InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country]
Index: []
<class 'pandas.core.frame.DataFrame'>
Index: 536641 entries, 0 to 541908
Data columns (total 8 columns):
 #   Column       Non-Null Count   Dtype         
---  ------       --------------   -----         
 0   InvoiceNo    536641 non-null  object        
 1   StockCode    536641 non-null  object        
 2   Description  535187 non-null  object        
 3   Quantity     536641 non-null  int64         
 4   InvoiceDate  536641 non-null  datetime64[ns]
 5   UnitPrice    536641 non-null  float64       
 6   CustomerID   401604 non-null  float64       
 7   Country      536641 non-null  object        
dtypes: datetime64[ns](1), float64(2), int64(1), object(4)
memory usage: 36.8+ MB
CLEANED_DF None
<class 'pandas.core.frame.DataFrame'>
Index: 536641 entries, 0 to 541908
Data columns (total 8 columns):
 #   Column       Non-Null Count   Dtype         
---  ------       --------------   -----         
 0   InvoiceNo    536641 non-null  object        
 1   StockCode    536641 non-null  object        
 2   Description  535187 non-null  object        
 3   Quantity     536641 non-null  int64         
 4   InvoiceDate  536641 non-null  datetime64[ns]
 5   UnitPrice    536641 non-null  float64       
 6   CustomerID   401604 non-null  float64       
 7   Country      536641 non-null  object        
dtypes: datetime64[ns](1), float64(2), int64(1), object(4)
memory usage: 36.8+ MB
None
ORIGINAL_DF
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 541909 entries, 0 to 541908
Data columns (total 8 columns):
 #   Column       Non-Null Count   Dtype         
---  ------       --------------   -----         
 0   InvoiceNo    541909 non-null  object        
 1   StockCode    541909 non-null  object        
 2   Description  540455 non-null  object        
 3   Quantity     541909 non-null  int64         
 4   InvoiceDate  541909 non-null  datetime64[ns]
 5   UnitPrice    541909 non-null  float64       
 6   CustomerID   406829 non-null  float64       
 7   Country      541909 non-null  object        
dtypes: datetime64[ns](1), float64(2), int64(1), object(4)
memory usage: 33.1+ MB
None
