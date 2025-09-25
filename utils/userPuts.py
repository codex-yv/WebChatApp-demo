from config.mongoConfig import client

async def update_user_cred_one(collection_name, password_value, field_name,  new_value):

    db = client["Users"]
    collection = db[collection_name]

    # Filter documents where 'password' matches the given value
    filter_query = {"password": password_value}

    # Define the update
    update_query = {"$set": {field_name: new_value}}

    # Apply the update
    result = await collection.update_many(filter_query, update_query)

async def update_user_contact(collection_name, field_name, field_value, new_contact):
    db = client["Users"]
    collection = db[collection_name]
    result = await collection.update_one(
        {field_name: field_value},
        {"$push": {"contacts": new_contact}}
    )

async def update_contact_keys(collection_name, field_name, field_value, new_contact, key):

    db = client["Users"]
    collection = db[collection_name]

    result = await collection.update_one(
        {field_name: field_value},
        {"$set": {f"contact_keys.{new_contact}": key}}
    )



