from flask import Flask
from flask_restful import Api
from resources.card_resource import Card


app = Flask(__name__)
api = Api(app)


api.add_resource(Card, "/verify")
#api.add_resource(Card, "/card/<int:number>")
#api.add_resource(Card, "/insert")

if __name__ == "__main__":
    app.run(debug=True, port=12345)
