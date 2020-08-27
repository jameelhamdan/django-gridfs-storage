from django.conf import settings
from pymongo import MongoClient


DEFAULT_GRIDFS_URL = getattr(settings, 'DEFAULT_GRIDFS_URL', 'mongodb://127.0.0.1:27017')
DEFAULT_BASE_URL = getattr(settings, 'DEFAULT_GRIDFS_SERVE_URL', None)
DEFAULT_COLLECTION = getattr(settings, 'DEFAULT_GRIDFS_COLLECTION', 'storage')
MONGO_CLIENT = MongoClient(DEFAULT_GRIDFS_URL)
