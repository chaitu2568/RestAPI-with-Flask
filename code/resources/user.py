import sqlite3
from flask_restful import reqparse,Resource
from models.user import UserModel

class UserRegister(Resource):

    parser=reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='This Field Should not be Blank')
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='This Field Should not be Blank')
    def post(self):
        data=UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"message":"user name already Exists"},400
        connection=sqlite3.connect('mydata.db')
        cursor=connection.cursor()
        query="INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query,(data['username'],data['password']))
        connection.commit()
        connection.close()

        return {"Message": "User registred Successfully"}, 201

