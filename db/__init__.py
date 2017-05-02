from pymongo import MongoClient
from config.settings import SETTINGS, ENV

class BasicMongoClient():
  def __init__(self, env=None):
    self.env = env
    if not self.env or self.env not in SETTINGS:
      self.env = ENV
    self.client = MongoClient(SETTINGS[self.env]['mongo']['host'],
      SETTINGS[self.env]['mongo']['port'])

class RedditMongoClient(BasicMongoClient):
  def __init__(self, subreddit, env=None):
    BasicMongoClient.__init__(self, env)
    self.db = self.client[SETTINGS[self.env]['mongo']['database']]
    self.collection = self.db[subreddit]

  def insert_comment(self, comment):
    entity = {
      'text':comment.body,
      'type':'comment',
    }
    self.collection.insert_one(entity)

  def insert_submission(self, submission):
    entity = {
      'text':submission.title,
      'type':'submission',
    }
    self.collection.insert_one(entity)
    # print entity
    #ObjectId. generation_time