import os
from pymongo import MongoClient


MONGOCLIENT = MongoClient(os.environ.get("MONGO_URL")) #Client

#Databases
DATABASE = MONGOCLIENT["Axiol"] #Main DB
LEVELDATABASE = MONGOCLIENT["Leveling"]

