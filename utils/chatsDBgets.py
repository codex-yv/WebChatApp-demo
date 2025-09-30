from config.mongoConfig import client
from security.decrypyChat import decryptt
async def get_chat(collection_name):
    db = client['Contacts']
    collection = db[collection_name]  # replace with actual collection name

    # Fetch all documents
    data = await collection.find().to_list()

    # Format and print data
    try:
        formatted_data = [(doc['user'], decryptt(token=doc['message'], key=doc['key'])) for doc in data]
    except KeyError:
        formatted_data = [(data[0]['user'], "Update in database took place all chat deleted.")]
        
    return formatted_data
