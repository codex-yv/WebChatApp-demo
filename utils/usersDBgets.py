from config.mongoConfig import client


async def get_all_user():
    db = client["Users"]
    
    collections = await db.list_collection_names()
    
    return collections

async def get_user_cred(collection_name) -> list:
    db = client["Users"]
    collection = db[collection_name]

    documents = await collection.find({}, {"_id": 0}).to_list()

    results = list(documents)
    return results

async def get_all_keys() -> list:

    db = client["Users"]
    all_keys = set()
    all_users = await db.list_collection_names()

    # Loop through all collections in the database
    for collection_name in all_users:
        collection = db[collection_name]
        
        # Find all documents that have the 'key' field
        cursor = collection.find({"key": {"$exists": True}}, {"key": 1})

        async for doc in cursor:
            value = doc.get("key")
            if value is not None:
                all_keys.add(value)

    return list(all_keys)

async def get_user_cred_key(collection_name) -> list:
    db = client["Users"]
    collection = db[collection_name]

    documents = await collection.find({}, {"_id": 0}).to_list()

    results = documents[0].get("key")
    return results

async def get_user_cred_contacts(collection_name) -> list:
    db = client["Users"]
    collection = db[collection_name]

    documents = await collection.find({}, {"_id": 0}).to_list()

    results = documents[0].get("contacts")
    return results

async def get_user_contacts_key(collection_name, contact_name) -> list:
    db = client["Users"]
    collection = db[collection_name]

    documents = await collection.find({}, {"_id": 0}).to_list()
    try:
        results = documents[0].get("contact_keys")[contact_name]
        return results
    except KeyError:
        pass