import yfinance as yf
import logging

logger = logging.getLogger(__name__)

def get_sensex_data():
    """
    Fetches SENSEX stock data from yfinance.
    Handles weekends/holidays by falling back to a wider historical range if necessary.
    """
    ticker_symbol = "^BSESN"
    sensex = yf.Ticker(ticker_symbol)
    
    logger.info(f"Fetching SENSEX data for {ticker_symbol}...")
    try:
        data = sensex.history(period="1d")
    except Exception as e:
        logger.error(f"Error fetching data from yfinance: {e}")
        raise e

    if data.empty:
        logger.warning("Latest day's data is empty. Fetching last 5 days history to get the most recent trading session...")
        try:
            data = sensex.history(period="5d")
        except Exception as e:
            logger.error(f"Error fetching historical data from yfinance: {e}")
            raise e
        
    if data.empty:
        raise ValueError(f"No stock data could be retrieved for ticker {ticker_symbol}.")

    latest_row = data.iloc[-1]
    date_str = str(latest_row.name.date()) if hasattr(latest_row, 'name') else 'N/A'
    
    open_price = float(latest_row['Open'])
    close_price = float(latest_row['Close'])
    
    logger.info(f"SENSEX data retrieved successfully for date {date_str}. Open: {open_price:.2f}, Close: {close_price:.2f}")

    return {
        "open": open_price,
        "close": close_price,
        "date": date_str
    }