from pymongo import MongoClient
from config import MONGO_URI

# MongoDB क्लाइंट इनिशियलाइज़ करें
client = MongoClient(MONGO_URI)

# डेटाबेस का नाम: otp_bot
db = client["otp_bot"]
