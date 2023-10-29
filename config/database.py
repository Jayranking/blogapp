from pymongo import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus

# My username and password
username = "Godfrey" 
password = "password@2"

# Encoded the username and password
encoded_username = quote_plus(username)
encoded_password = quote_plus(password)

# Construct the MongoDB URI with the encoded username and password
uri = f"mongodb+srv://{encoded_username}:{encoded_password}@cluster0.tcmrpkk.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.blog_db
collection_name = db["blog_collections"]

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("You successfully connected to MongoDB!")
except Exception as e:
    print(e)
