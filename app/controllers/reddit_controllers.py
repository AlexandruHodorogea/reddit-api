import datetime

from bson.objectid import ObjectId
from flask import request
from flask_restful import Resource

from app.handlers.parser import parse
from app.handlers import ok_response, error_response, \
  parse_error_response

items_parser_sett = dict(
  get= {
    'subreddit': dict(type=str, required=True, location='args'),
    'from': dict(type=int, required=True, location='args'),
    'to': dict(type=int, required=True, location='args'),
    'keyword': dict(type=str, required=False, location='args'),
  }
)

class ItemsController(Resource):

  def get(self):
    try:
      args = parse(items_parser_sett['get'])
    except Exception as e:
      return parse_error_response(e)
    subreddit = args['subreddit']
    from_oid = ObjectId.from_datetime(
      datetime.datetime.utcfromtimestamp(args['from']))
    to_oid = ObjectId.from_datetime(
      datetime.datetime.utcfromtimestamp(args['to']))
    keyword = args.get('keyword', None)

    data = request.mongo.get_entities(subreddit, from_oid, to_oid, keyword)

    return ok_response(data=data)
