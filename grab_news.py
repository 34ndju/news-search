from authentication import Secrets
from pymongo import MongoClient

secrets = Secrets()

client = MongoClient('mongodb://' + secrets.USERNAME + ':' + secrets.PASSWORD + '@ds117858.mlab.com:17858/news-search')
