from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app = Flask(__name__)
app.config['SECRET_KEY'] = 'f3ff4158c7fc7ac1086f284e568143b6a97249508998c0b3474541d17bbe74ccba891f048e98e33a375dd714'
api = Api(app)
jwt = JWT(app, authenticate, identity)
items = []

class Item(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('price',
			type=float,
			required=True,
			help='This field can not be left blank!')

	def get(self, name):
		item = next(filter(lambda x: x['name'] == name, items), None)
		return {'item': item}, 200 if item else 404

	def post(self, name):
		if next(filter(lambda x: x['name'] == name, items), None):
			return {'message': 'Item already exists!'}, 400
		data = Item.parser.parse_args()
		new_item = {'name': name, 'price': data['price']}
		items.append(new_item)
		return new_item, 201

	def delete(self, name):
		global items
		items = list(filter(lambda x: x['name'] != name, items))
		return {'message': 'Item has been deleted!'}

	def put(self, name):
		item = next(filter(lambda x: x['name'] == name, items), None)
		if item:
			data = Item.parser.parse_args()
			item['price'] = data['price']
			return {'message': 'Item has been updated!'}
		else:
			return {'message': 'Item does not exist!'}, 400
		

class Items(Resource):

	@jwt_required()
	def get(self):
		return {"items": items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')


app.run(debug=True)