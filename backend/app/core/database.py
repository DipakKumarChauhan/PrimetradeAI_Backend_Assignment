from pymongo import MongoClient
from app.core.config import settings
from datetime import datetime
from app.core.security import hash_password

client: MongoClient = None
db = None


def connect_to_mongo():
    global client, db
    client = MongoClient(settings.MONGODB_URI)
    db = client[settings.DATABASE_NAME]
    db["users"].create_index("email", unique=True)
    seed_admin_user()


def close_mongo_connection():
    global client
    if client:
        client.close()

def get_user_collection():
    return db["users"]

def seed_admin_user():
    users = db["users"]

    admin = users.find_one({"email": settings.ADMIN_EMAIL})
    if admin:
        return

    users.insert_one({
        "email": settings.ADMIN_EMAIL,
        "password_hash": hash_password(settings.ADMIN_PASSWORD),
        "role": "admin",
        "created_at": datetime.utcnow()
    })

    print("✅ Admin user seeded")
