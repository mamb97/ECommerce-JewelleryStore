from flask import current_app, g
from pymongo import MongoClient
import configparser

config = configparser.ConfigParser()
config.read("../config.ini")


def get_db():
    """
    Configuration method to return db instance
    """
    return MongoClient(config['DB']['DB_URI']).jewelry_store
