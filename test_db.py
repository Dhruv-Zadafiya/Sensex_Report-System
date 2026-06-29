
from pymongo import MongoClient
from config import MONGO_URI

print(f"Attempting connection with MONGO_URI: {MONGO_URI}")
client = MongoClient(MONGO_URI)

try:
    client.admin.command("ping")
    print("MongoDB Connected Successfully!")
except Exception as e:
    print("Connection Failed:", e)