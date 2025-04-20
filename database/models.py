from pymongo import MongoClient
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client.get_database("k_master")

users = db.users
countries = db.countries
services = db.services
promos = db.promos

# USER
def get_user(chat_id): return users.find_one({"_id": chat_id})
def create_user(chat_id, data): users.insert_one(data)
def update_user(chat_id, data): users.update_one({"_id": chat_id}, {"$set": data})

# COUNTRY
def add_country(name, cid):
    countries.update_one({"id": cid}, {"$set": {"name": name, "id": cid}}, upsert=True)

def get_all_countries():
    return list(countries.find())

# SERVICE
def add_service(name, sid, price, country_id, country_name):
    services.update_one(
        {"id": sid, "country_id": country_id},
        {"$set": {
            "name": name,
            "id": sid,
            "price": price,
            "country_id": country_id,
            "country_name": country_name
        }},
        upsert=True
    )

def get_services_by_country_id(country_id):
    return list(services.find({"country_id": country_id}))

# PROMO
def add_promo(code, amount):
    promos.update_one({"code": code.upper()}, {"$set": {"amount": amount}}, upsert=True)

def get_promo(code):
    return promos.find_one({"code": code.upper()})
    # --- UTR Validation ---
utr_records = db.utr_records

def is_utr_used(utr):
    return utr_records.find_one({"utr": utr}) is not None

def mark_utr_as_used(utr):
    utr_records.insert_one({"utr": utr})
