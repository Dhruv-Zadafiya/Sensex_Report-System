import yfinance as yf
import logging
import time

logger = logging.getLogger(__name__)

def get_sensex_data():
    """
    Fetches SENSEX stock data from yfinance.
    Handles weekends/holidays by falling back to a wider historical range if necessary.
    Includes a retry mechanism (3 attempts, 15s delay) to handle transient API issues.
    """
    ticker_symbol = "^BSESN"
    sensex = yf.Ticker(ticker_symbol)
    
    logger.info(f"Fetching SENSEX data for {ticker_symbol}...")
    
    max_retries = 3
    retry_delay = 15 
    data = None
    
    for attempt in range(1, max_retries + 1):
        try:
            data = sensex.history(period="1d")
            if not data.empty:
                break
            logger.warning(f"Attempt {attempt}/{max_retries}: yfinance returned empty data for period=1d.")
        except Exception as e:
            logger.error(f"Attempt {attempt}/{max_retries}: Error fetching data from yfinance: {e}")
            if attempt == max_retries:
                raise e
        
        if attempt < max_retries:
            logger.info(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)

    if data is None or data.empty:
        logger.warning("Latest day's data is empty. Fetching last 5 days history to get the most recent trading session...")
        for attempt in range(1, max_retries + 1):
            try:
                data = sensex.history(period="5d")
                if not data.empty:
                    break
                logger.warning(f"Attempt {attempt}/{max_retries}: yfinance returned empty data for period=5d.")
            except Exception as e:
                logger.error(f"Attempt {attempt}/{max_retries}: Error fetching historical data from yfinance: {e}")
                if attempt == max_retries:
                    raise e
            
            if attempt < max_retries:
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
        
    if data is None or data.empty:
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