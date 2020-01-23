from flask import Flask, request
from flask_restful import Api, Resource
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-key'
api = Api(app)
jwt = JWT(app, authenticate, identity)
items = []

class Item(Resource):

	def get(self, name):
		item = next(filter(lambda x: x['name'] == name, items), None)
		return {'item': item}, 200 if item else 404

	def post(self, name):
		if next(filter(lambda x: x['name'] == name, items), None):
			return {'message': 'Item already exists!'}, 400
		data = request.get_json()
		new_item = {'name': name, 'price': data['price']}
		items.append(new_item)
		return new_item, 201

	def delete(self, name):
		global items
		items = list(filter(lambda x: x['name'] != name, items))
		return {f'message': 'Item {name} has been deleted!'}

	def put(self, name):
		item = next(filter(lambda x: x['name'] == name, items), None)
		if item:
			data = request.get_json()
			item['price'] = data['price']
			return {f'message': 'Item {name} has been updated!'}
		else:
			return {f'message': 'Item {name} does not exist!'}, 400
		

class Items(Resource):

	@jwt_required()
	def get(self):
		return {"items": items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')


app.run(debug=True)