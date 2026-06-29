import os
import re
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL", "liveupdate377@gmail.com")
APP_PASSWORD = os.getenv("APP_PASSWORD", "Dhruv@0377")

raw_mongo_uri = os.getenv("MONGO_URI", "mongodb+srv://zadafiyadhruv_db_user:Dhruv6147@cluster0.h1togyr.mongodb.net/stockdb?appName=Cluster0")

if raw_mongo_uri:
    MONGO_URI = re.sub(r':<([^>]*)>@', r':\1@', raw_mongo_uri)
else:
    MONGO_URI = raw_mongo_uri