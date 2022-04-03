from flask import current_app, g
from pymongo import MongoClient
import configparser
import os

config = configparser.ConfigParser()
config_file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../config.ini')
config.read(config_file_path)


def get_db():
    """
    Configuration method to return db instance
    """
    return MongoClient(config['DB']['DB_URI']).jewelry_store
