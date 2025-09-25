from config.mongoConfig import client

async def insert_chat(collection_name, user, message):
    db = client["Contacts"]
    collection = db[collection_name]

    data = {
        "user":user,
        "message":message
    }

    await collection.insert_one(data)

