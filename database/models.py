from .mongo_client import db

users = db["users"]
services = db["services"]
countries = db["countries"]
used_utrs = db["used_utrs"]
promo_codes = db["promo_codes"]  # ✅ Added

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

def add_service(name, sid, price, cid=None, cname=None):
    service_data = {
        "name": name,
        "id": sid,
        "price": int(price)
    }
    if cid and cname:
        service_data["country_id"] = cid
        service_data["country_name"] = cname

    services.update_one(
        {"name": name, "country_id": cid} if cid else {"name": name},
        {"$set": service_data},
        upsert=True
    )

def get_all_services():
    return list(services.find())

def get_service_by_name(name):
    return services.find_one({"name": name})

def get_services_by_country_id(cid):
    return list(services.find({"country_id": cid}))

# -------------------------------
# COUNTRY FUNCTIONS
# -------------------------------

def add_country(name, cid):
    countries.update_one(
        {"id": cid},
        {"$set": {"name": name, "id": cid}},
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

# -------------------------------
# PROMO CODE FUNCTIONS ✅
# -------------------------------

def add_promo(code, amount):
    promo_codes.update_one(
        {"code": code.upper()},
        {"$set": {"code": code.upper(), "amount": amount}},
        upsert=True
    )

def get_promo(code):
    return promo_codes.find_one({"code": code.upper()})
