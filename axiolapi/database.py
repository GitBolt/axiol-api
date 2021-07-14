import os
from pymongo import MongoClient


MONGOCLIENT = MongoClient(os.environ.get("AXIOL_MONGO_URL")) #Client

#Databases
DATABASE = MONGOCLIENT["Axiol"] #Main DB
LEVELDATABASE = MONGOCLIENT["Leveling"]

#Traning data db
MONGO_TRAINING_URL = MongoClient(os.environ.get("MONGO_TRAINING_URL"))
DB1 = MONGO_TRAINING_URL["DB1"] 
