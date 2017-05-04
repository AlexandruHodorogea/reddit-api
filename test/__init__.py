import unittest

import pymongo

from config.settings import SETTINGS
SETTINGS['env'] = 'test'

from app import app
from db import RedditMongoClient

class TestComment():
  def __init__(self, text='test_text'):
    self.body = text

class TestSubmission():
  def __init__(self, text='test_text'):
    self.title = text

class MongoBaseTest(unittest.TestCase):
  def setUp(self):
    self.mongo = RedditMongoClient(env='test')
    self.mongo.client.drop_database(SETTINGS['test']['mongo']['database'])

  def tearDown(self):
    self.mongo.client.drop_database(SETTINGS['test']['mongo']['database'])
    self.mongo.client.close()


class ServerBaseTest(MongoBaseTest):

  def setUp(self):
    MongoBaseTest.setUp(self)
    app.config['TESTING'] = True
    self.app = app.test_client()
    self.mongo.collection.create_index([('text', pymongo.TEXT)])