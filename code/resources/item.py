from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3
from models.item import ItemModel

class Item(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='This Field Cannot be Left Blank!')

    @jwt_required()
    def get(self,name):
        item=ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message":"Item does not exists."},404


    def post(self,name):
        if ItemModel.find_by_name(name):
            return {'message':'The item with the given name: {} already exists'.format(name)}, 400

        data=Item.parser.parse_args()
        item=ItemModel(name, data['price'])
        try:
            item.save_to_db()
        except:
            return {"message":"AN error occured during Insertion"}, 500 # Internal Sever error
        return item.json(), 201 #status Code


    def delete(self,name):
        item=ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {"message": "The item is deleted Successfully"}


    def put(self,name):
        data=Item.parser.parse_args()
        item=ItemModel.find_by_name(name)
        if item is None:
            item=ItemModel(name,data['price'])
        else:
            item.price=data['price']
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        connection=sqlite3.connect('mydata.db')
        cursor=connection.cursor()
        item=cursor.execute("SELECT * FROM items")
        items=[]
        for row in item:
            items.append({'name':row[0],'price':row[1]})
        return {"items":items}
