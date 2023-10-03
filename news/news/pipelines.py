# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
from pymongo import MongoClient
# config file reader
from configparser import ConfigParser

# Read config file
config = ConfigParser()
config.read('config.ini')

class NewsPipeline:
    def __init__(self):
        self.conn = MongoClient("mongodb+srv://mangodb:mangodb@cluster0.pxkjnl6.mongodb.net/?retryWrites=true&w=majority")

        db = self.conn['cnn_db']

        self.collection = db['cnn_collection']


    def process_item(self, item, spider):
        self.collection.insert_one(dict(item))
        return item
    
