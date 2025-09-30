from config.mongoConfig import client
from security.decrypyChat import decryptt
async def get_chat(collection_name):
    db = client['Contacts']
    collection = db[collection_name]  # replace with actual collection name

    # Fetch all documents
    data = await collection.find().to_list()

    # Format and print data
    try:
        formatted_data = [(doc['user'], decryptt(token=doc['message'], key=doc['key']), doc['time']) for doc in data]
    except KeyError:
        formatted_data = [(data[0]['user'], "Update in database took place all chat deleted.", data[0]['time'])]
        
    return formatted_data
