
from flask_restful import Resource, reqparse

from flask import Flask, request
from flask_jwt_extended import  jwt_required, get_jwt, get_jwt_identity
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


        

    @jwt_required(fresh=True)
    def post(self, name): 
        
        if ItemModel.find_by_name(name):
            return {"message": f"An item with name {name} already exists."}, 400
            
        data = Item.parser.parse_args()
        #data = request.get_json() #get_json(force=True) get_json(silent=True)

       
        item = ItemModel(name,  data["price"], data["store_id"])

        try:
            item.save_to_db()
        except:
            return {"message" : "An error occurred inserting the item"}, 500 #Internal server error 

        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        claims = get_jwt()
        if not claims["is_admin"]:
            return{"message":"admin privilege required"}, 401
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
    @jwt_required(optional=True)
    def get(self):
        user_id = get_jwt_identity()
        items = [item.json() for item in ItemModel.find_all()]
        if user_id:
            return {"items": items}, 200
        return {"items": [item["name"] for item in items], "message":"More data if you log in"}, 200
        #return {"items": list(map(lambda x:x.json(), ItemModel.query.all()))}

   