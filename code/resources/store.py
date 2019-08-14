from flask_restful import Resource
from models.stores import StoreModel

class Store(Resource):

    def get(self,name):
        store=StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {"message":"Store does not exists."},404


    def post(self,name):
        if StoreModel.find_by_name(name):
            return {'message':'The item with the given name: {} already exists'.format(name)}, 400
        store=StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message":"AN error occured during Insertion"}, 500 # Internal Sever error
        return store.json(), 201 #status Code


    def delete(self,name):
        store=StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {"message": "The store is deleted Successfully"}


class StoreList(Resource):
    def get(self):
        return {'stores':[store.json() for store in StoreModel.query.all()]}
