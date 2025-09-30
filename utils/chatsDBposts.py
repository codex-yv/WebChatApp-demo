from config.mongoConfig import client
from security.encryptChat import encryptt
from utils.IST import ISTtime
async def insert_chat(collection_name, user, message):
    db = client["Contacts"]
    collection = db[collection_name]
    key, token = encryptt(chat=message)
    current_time = ISTtime()
    data = {
        "user":user,
        "message":token,
        "key": key,
        "time":current_time
    }

    await collection.insert_one(data)

