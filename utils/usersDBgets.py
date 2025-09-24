from config.mongoConfig import client


async def get_all_user():
    db = client["Users"]
    
    collections = await db.list_collection_names()
    
    return collections

async def get_user_cred(collection_name):
    db = client["Users"]
    collection = db[collection_name]

    documents = await collection.find({}, {"_id": 0}).to_list()

    results = list(documents)
    return results

