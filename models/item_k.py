from db import db

class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision = 2))
    
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price 
        self.store_id = store_id


    def json(self):
        return {
            "id":self.id,
            "name":self.name,
            "price":self.price,
            "store_id":self.store_id
           }


    @classmethod
    def find_by_name(cls, name):
        
        return ItemModel.query.filter_by(name = name).first()  #"SELECT * FROM items WHERE name = ?
        # return ItemModel.query.filter_by(name = name).filter_by(id = 1)
        #return ItemModel.query.filter_by(name = name, id = 1)
        # return ItemModel.query.filter_by(name = name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()


    def save_to_db(self): #SQLALCHEMY both updates and inserts by using the following code

        #The session in this instance is a collection of objects
        #that we're going to write to the database.
        #We can add multiple objects to the session
        #and then write them all at one, and that's more efficient
        db.session.add(self)
        db.session.commit()



    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        
    
    