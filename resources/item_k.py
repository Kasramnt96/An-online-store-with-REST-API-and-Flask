
from flask_restful import Resource, reqparse

from flask import Flask, request
from flask_jwt import  jwt_required
from models.item_k import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price", type = float, required = True, help = "This field can not be blank")
    parser.add_argument("store_id", type = int, required = True, help = "Every item needs a store id")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message" : "Item not found."}


        

    
    def post(self, name): 
        
        if ItemModel.find_by_name(name):
            return {"message": f"An item with name {name} already exists."}, 400
            
        data = Item.parser.parse_args()
        #data = request.get_json() #get_json(force=True) get_json(silent=True)

       # item = {"name":name, "price": data["price"]}
        item = ItemModel(name,  data["price"], data["store_id"])

        try:
            item.save_to_db()
        except:
            return {"message" : "An error occurred inserting the item"}, 500 #Internal server error 

        return item.json(), 201

    
    def delete(self, name):
        
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted.'}
        return {'message': 'Item not found.'}, 404

    def put(self, name):

        #data = request.get_json()
        data = Item.parser.parse_args() # parse the arguments comming through json payload and put valid ones in data

        item = ItemModel.find_by_name(name)
        

        if item is None:
            item = ItemModel(name, data["price"], data["store_id"])

        else:
            item.price = data["price"]

        item.save_to_db()

        return item.json()

    
              
            
class ItemList(Resource):
    def get(self):
        
         return {"items": [item.json() for item in ItemModel.query.all()]}
         #return {"items": list(map(lambda x:x.json(), ItemModel.query.all()))}

   