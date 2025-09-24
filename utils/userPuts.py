from config.mongoConfig import client

async def update_user_status(collection_name, password_value, new_status):

    db = client["Users"]
    collection = db[collection_name]

    # Filter documents where 'password' matches the given value
    filter_query = {"password": password_value}

    # Define the update
    update_query = {"$set": {"status": new_status}}

    # Apply the update
    result = await collection.update_many(filter_query, update_query)