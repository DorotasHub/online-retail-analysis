from ucimlrepo import fetch_ucirepo

def load_online_retail_data():
    online_retail = fetch_ucirepo(id=352)
    df = online_retail.data.features
    return df

if __name__ == "__main__":
    df = load_online_retail_data()
    # print(df)
    # print(df.head())
    # print(df.columns)