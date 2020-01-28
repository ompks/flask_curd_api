import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='This field can not be left blank!')

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        select_query = "SELECT * FROM ITEMS WHERE NAME = ?"
        result = cursor.execute(select_query, (name,))
        row = result.fetchone()
        if row:
            return {'item':{'name': row[1], 'price': row[2]}}, 200
        return None

    def post(self, name):
        if self.find_by_name(name):
            return {'message': 'Item already exists!'}, 400
        data = Item.parser.parse_args()
        new_item = {'name': name, 'price': data['price']}
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO ITEMS VALUES (NULL, ?, ?)"
        cursor.execute(query, (name, new_item['price']))
        connection.commit()
        connection.close()
        return new_item, 201

    def get(self, name):
        item = self.find_by_name()
        if item:
            return item
        return {'message': 'No item found!'}, 400

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
       connection = sqlite3.connect('data.db')
       cursor = connection.cursor()
       select_query = "SELECT * FROM ITEMS"
       result = cursor.execute(select_query)
       for row in result:
           return {'id': row[0], 'name': row[1], 'price': row[2]}