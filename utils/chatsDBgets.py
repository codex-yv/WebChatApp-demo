from config.mongoConfig import client

async def get_chat(collection_name):
    db = client['Contacts']
    collection = db[collection_name]  # replace with actual collection name

    # Fetch all documents
    data = await collection.find().to_list()

    # Format and print data
    formatted_data = [(doc['user'], doc['message']) for doc in data]
    return formatted_data
