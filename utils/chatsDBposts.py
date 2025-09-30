from config.mongoConfig import client
from security.encryptChat import encryptt

async def insert_chat(collection_name, user, message):
    db = client["Contacts"]
    collection = db[collection_name]
    key, token = encryptt(chat=message)
    data = {
        "user":user,
        "message":token,
        "key": key
    }

    await collection.insert_one(data)

