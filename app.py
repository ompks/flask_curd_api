from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from user import UserRegistration
from item import Item, Items

app = Flask(__name__)
app.config['SECRET_KEY'] = 'f3ff4158c7fc7ac1086f284e568143b6a97249508998c0b3474541d17bbe74ccba891f048e98e33a375dd714'
api = Api(app)
jwt = JWT(app, authenticate, identity)


api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')
api.add_resource(UserRegistration, '/register')

if __name__ == "__main__":
	app.run(debug=True)