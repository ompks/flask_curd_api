import sqlite3
from flask_restful import Resource,reqparse

class User:

    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM USERS WHERE username=?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        connection.close()
        return user

    @classmethod
    def find_by_uid(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM USERS WHERE id=?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        connection.close()
        return user

class UserRegistration(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
			type=str,
			required=True,
			help='This field can not be left blank!')
    parser.add_argument('password',
            type=str,
            required=True,
            help='This field can not be left blank!')

    @classmethod
    def post(cls):
        data = cls.parser.parse_args()
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        create_user = "INSERT INTO USERS VALUES(NULL,?,?)"
        cursor.execute(create_user, (data['username'], data['password']))
        connection.commit()
        connection.close()
        return {'message': 'User has been created sucessfully!'}