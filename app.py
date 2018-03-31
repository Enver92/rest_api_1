from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = []

class Item(Resource):
    def get(self, name):
        item = next(filter(lambda item: item['name']==name, items), None) # returns the first item found
        return {"item": item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda item: item['name']==name, items), None):
            return {"message": f"An item with name {name} already exists"}, 400
        data = request.get_json()
        item = {"name": name, "price": data['price']}
        items.append(item)
        return item, 201 # to ensure a client that the item has been created (that's what 201 mean)

class ItemList(Resource):
    def get(self):
        return {"items": items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)
