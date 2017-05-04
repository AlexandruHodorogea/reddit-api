from flask import Flask, request
from flask_restful import Api

from db import RedditMongoClient

app = Flask(__name__)
rest_api = Api(app)


@app.before_request
def before_request():
  request.mongo = RedditMongoClient()
  pass

@app.after_request
def after_request(response):
  request.mongo.client.close()
  return response

from app.controllers.reddit_controllers import ItemsController

rest_api.add_resource(ItemsController, '/items/')

if __name__ == '__main__':
    app.run(debug=True)