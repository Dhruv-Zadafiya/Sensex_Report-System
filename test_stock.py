from data.stock_fetcher import get_sensex_data

try:
    print("Fetching SENSEX stock data...")
    stock = get_sensex_data()
    print("\nFetch Successful!")
    print(f"Trading Date: {stock['date']}")
    print(f"Open Price  : INR {stock['open']:,.3f}")
    print(f"Close Price : INR {stock['close']:,.3f}")
except Exception as e:
    print("\nStock Fetch Failed:", e)
