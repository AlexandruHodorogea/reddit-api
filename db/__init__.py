from pymongo import MongoClient
from config.settings import SETTINGS

class BasicMongoClient():
  def __init__(self, env=None):
    self.env = env
    if not self.env or self.env not in SETTINGS:
      self.env = SETTINGS['env']
    self.client = MongoClient(SETTINGS[self.env]['mongo']['host'],
      SETTINGS[self.env]['mongo']['port'])

class RedditMongoClient(BasicMongoClient):
  def __init__(self, env=None):
    BasicMongoClient.__init__(self, env)
    self.db = self.client[SETTINGS[self.env]['mongo']['database']]
    self.collection = self.db['entities']

  def insert_comment(self, subreddit, comment):
    entity = {
      'text':comment.body,
      'subreddit':subreddit,
      'type':'comment',
    }
    return self.collection.insert_one(entity)

  def insert_submission(self, subreddit, submission):
    entity = {
      'text':submission.title,
      'subreddit':subreddit,
      'type':'submission',
    }
    return self.collection.insert_one(entity)

  def get_entities(self, subreddit, from_oid, to_oid, keyword=None):
    if not keyword:
      data = self.collection.find({
        '_id': {
          '$gt': from_oid,
          '$lt': to_oid
        },
        'subreddit': subreddit,
      })
    else:
      data = self.collection.find({
        '_id': {
          '$gt': from_oid,
          '$lt': to_oid
        },
        'subreddit': subreddit,
        '$text': {'$search': keyword},
      })
      
    count = data.count()
    data = list(data)
    for d in data:
      del d['_id']
    return dict(
      results=data,
      count=count,
    )
