from .mongo_client import db

users = db["users"]
services = db["services"]
countries = db["countries"]
used_utrs = db["used_utrs"]  # नया कलेक्शन

# -------------------------------
# USER FUNCTIONS
# -------------------------------

def get_user(chat_id):
    return users.find_one({"_id": chat_id})

def create_user(chat_id, data):
    data["_id"] = chat_id
    users.insert_one(data)

def update_user(chat_id, updates):
    users.update_one({"_id": chat_id}, {"$set": updates})

# -------------------------------
# SERVICE FUNCTIONS
# -------------------------------

def add_service(name, sid, price):
    services.update_one(
        {"name": name},
        {"$set": {"id": sid, "price": int(price), "name": name}},
        upsert=True
    )

def get_all_services():
    return list(services.find())

def get_service_by_name(name):
    return services.find_one({"name": name})

# -------------------------------
# COUNTRY FUNCTIONS
# -------------------------------

def add_country(name, code):
    countries.update_one(
        {"name": name},
        {"$set": {"name": name, "code": code}},
        upsert=True
    )

def get_all_countries():
    return list(countries.find())

# -------------------------------
# UTR FUNCTIONS (Anti-Reuse)
# -------------------------------

def is_utr_used(utr):
    return used_utrs.find_one({"utr": utr}) is not None

def mark_utr_as_used(utr):
    used_utrs.insert_one({"utr": utr})
