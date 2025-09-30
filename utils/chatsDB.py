from config.mongoConfig import client

async def create_contact(collection_name:str, user_data:dict):
    db = client["Contacts"]
    collection = db[collection_name]

    # Insert the new user document
    result = await collection.insert_one(user_data)

