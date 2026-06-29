import logging
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from config import MONGO_URI

logger = logging.getLogger(__name__)

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
    db = client["stockdb"]
    collection = db["Sensex_Reports"]
except Exception as e:
    logger.critical(f"Failed to initialize MongoDB client: {e}")
    client = None
    db = None
    collection = None

def is_db_connected():
    """
    Checks if MongoDB connection is alive.
    """
    if client is None:
        return False
    try:
        client.admin.command('ping')
        return True
    except Exception:
        return False

def save_stock_data(open_price, close_price, date_str="N/A"):
    """
    Save Sensex stock data to MongoDB
    """
    if collection is None:
        logger.error("MongoDB Collection is uninitialized. Skipping database save.")
        return None

    change = close_price - open_price
    percentage_change = (change / open_price) * 100 if open_price != 0 else 0

    document = {
        "open_price": round(open_price, 2),
        "close_price": round(close_price, 2),
        "change": round(change, 2),
        "percentage_change": round(percentage_change, 2),
        "trading_date": date_str,
        "created_at": datetime.now()
    }

    try:
        client.admin.command('ping')
        result = collection.insert_one(document)
        logger.info(f"Database insertion successful. Document ID: {result.inserted_id}")
        return result.inserted_id
    except Exception as e:
        logger.error(f"Database insertion failed: {e}")
        return None

def get_all_reports():
    """
    Fetch and return all reports from MongoDB
    """
    if collection is None:
        logger.error("MongoDB Collection is uninitialized.")
        return []

    try:
        return list(collection.find().sort("created_at", -1))
    except PyMongoError as e:
        logger.error(f"Failed to fetch all reports: {e}")
        return []

def get_recent_reports(limit=5):
    """
    Fetch and return the N most recent reports
    """
    if collection is None:
        logger.error("MongoDB Collection is uninitialized.")
        return []

    try:
        return list(collection.find().sort("created_at", -1).limit(limit))
    except PyMongoError as e:
        logger.error(f"Failed to fetch recent reports: {e}")
        return []