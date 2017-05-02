from flask import Flask
from flask_restful import Api

app = Flask(__name__)
rest_api = Api(app)

from app.controllers.reddit_controllers import ItemsController

rest_api.add_resource(ItemsController, '/items/')

if __name__ == '__main__':
    app.run(debug=True)