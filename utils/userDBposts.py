from config.mongoConfig import client


async def create_user(collection_name:str, user_data:dict):
    db = client["Users"]
    collection = db[collection_name]

    # Insert the new user document
    result = await collection.insert_one(user_data)

    print(f"New user created with _id: {result.inserted_id}")


