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

    @classmethod
    def insert_item(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO ITEMS VALUES (NULL, ?, ?)"
        cursor.execute(query, (item['name'], item['price']))
        connection.commit()
        connection.close()

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "UPDATE ITEMS SET PRICE=? WHERE NAME=?"
        cursor.execute(query, (item['price'], item['name']))
        connection.commit()
        connection.close()

    def post(self, name):
        @jwt_required()
        if self.find_by_name(name):
            return {'message': 'Item already exists!'}, 400
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        try:
            self.insert_item(item)
        except:
            return {'message': 'An error happened while inserting item!'}, 500
        return item, 201

    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'No item found!'}, 400

    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "DELETE FROM ITEMS WHERE NAME=?"
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()
        return {'message': 'Item has been deleted!'}

    def put(self, name):
        item = self.find_by_name(name)
        data = Item.parser.parse_args()
        updated_item = {'name': name, 'price': data['price']}
        if item:
            try:
                self.update(updated_item)
            except:
                return {'message': 'An error happened while inserting item!'}, 500
        else:
            try:
                self.insert_item(updated_item)
            except:
                return {'message': 'An error happened while updating item!'}, 500
        return {'message': 'Item has been updated!'}
		

class Items(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        select_query = "SELECT * FROM ITEMS"
        result = cursor.execute(select_query)
        items = []
        for row in result:
            items.append({'id': row[0], 'name': row[1], 'price': row[2]})
        connection.close()
        return {'items': items}        