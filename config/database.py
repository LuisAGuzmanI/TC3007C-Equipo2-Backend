from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
from os import environ
import certifi

load_dotenv()
mongodb_uri = environ.get('MONGODB_URI')

client = MongoClient(mongodb_uri, tlsCAFile=certifi.where())

db = client["classroom-ai"]

users = db["users"]
courses = db["courses"]