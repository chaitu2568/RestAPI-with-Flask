from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3

class Item(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='This Field Cannot be Left Blank!')

    @jwt_required()
    def get(self,name):
        item=self.find_by_name(name)
        if item:
            return item
        return {"message":"Item does not exists."},404

    @classmethod
    def find_by_name(cls,name):
        connection=sqlite3.connect('mydata.db')
        cursor=connection.cursor()
        query="SELECT * FROM items WHERE name= ?"
        result=cursor.execute(query,(name,))
        row=result.fetchone()
        if row:
            return {"item":{"name":row[0],"price":row[1]}}


    def post(self,name):
        if self.find_by_name(name):
            return {'message':'The item with the given name: {} already exists'.format(name)}, 400

        data=Item.parser.parse_args()
        item={'name':name, 'price':data['price']}
        try:
            self.insert(item)
        except:
            return {"massage":"AN error occured during Insertion"}, 500 # Internal Sever error
        return item, 201 #status Code

    @classmethod
    def insert(cls,item):
        connection=sqlite3.connect('mydata.db')
        cursor=connection.cursor()
        query="INSERT INTO items VALUES (?,?)"
        cursor.execute(query,(item['name'],item['price']))
        connection.commit()
        connection.close()


    def delete(self,name):
        connection=sqlite3.connect('mydata.db')
        cursor=connection.cursor()
        query="DELETE FROM items WHERE name=?"
        cursor.execute(query,(name,))
        connection.commit()
        connection.close()
        return {'message': 'The requested item is deleted' }

    def put(self,name):
        # data=request.get_json()
        data=Item.parser.parse_args()
        item=self.find_by_name(name)
        updated_item={'name':name, 'price':data['price']}
        if item is None:
            try:
                self.insert(updated_item)
            except:
                return {"message":"Error occured during the Insertion"},500
        else:
            try:
                self.update(updated_item)
            except:
                return {"message":"Error occured during the Updation"},500
        return updated_item

    @classmethod
    def update(cls,item):
        connection=sqlite3.connect('mydata.db')
        cursor=connection.cursor()
        query="UPDATE items SET price =? WHERE name=?"
        cursor.execute(query,(item['price'],item['name']))
        connection.commit()
        connection.close()



class ItemList(Resource):
    def get(self):
        connection=sqlite3.connect('mydata.db')
        cursor=connection.cursor()
        item=cursor.execute("SELECT * FROM items")
        items=[]
        for row in item:
            items.append({'name':row[0],'price':row[1]})
        return {"items":items}
