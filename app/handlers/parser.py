from flask_restful import reqparse

def parse(parmas):
  parser = reqparse.RequestParser()
  for key,value in parmas.items():
    parser.add_argument(key,**value)  
  return parser.parse_args()
