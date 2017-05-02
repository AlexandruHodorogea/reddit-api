import datetime

from bson.objectid import ObjectId
from flask_restful import Resource

from app.handlers.parser import parse
from app.handlers import ok_response, error_response, \
  parse_error_response
from db import RedditMongoClient

items_parser_sett = dict(
  get= {
    'subreddit': dict(type=str, required=True, location='args'),
    'from': dict(type=int, required=True, location='args'),
    'to': dict(type=int, required=True, location='args'),
  }
)

class ItemsController(Resource):

  def get(self):
    try:
      args = parse(items_parser_sett['get'])
    except Exception as e:
      return parse_error_response(e)

    from_oid = ObjectId.from_datetime(
      datetime.datetime.fromtimestamp(args['from']))
    to_oid = ObjectId.from_datetime(
      datetime.datetime.fromtimestamp(args['to']))

    mongo_client = RedditMongoClient(args['subreddit'])

    data = mongo_client.collection.find({'_id':{'$gt': from_oid,'$lt': to_oid}})
    count = data.count()
    data = list(data)
    for d in data:
      del d['_id']
    return ok_response(data={'results': data, 'count': count})
