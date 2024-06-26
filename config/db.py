import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.environ.get('DB_HOST'))

db = client.learn_fastapi

def db_conn():
    return db