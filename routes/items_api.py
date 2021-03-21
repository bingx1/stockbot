from flask import Blueprint, jsonify
from util.mongo_adaptor import MongoAdaptor
MongoAdaptor = MongoAdaptor()

items_api = Blueprint('items_api', __name__)

@items_api.route('/api/items/all', methods=['GET'])
def items():
    items = MongoAdaptor.fetch_items_dict()
    for item in items:
        del item['_id'] 
        # item.pop('_id', None)
    
    return jsonify(items)

@items_api.route('/api/changes', methods=['GET'])
def changes():
    return MongoAdaptor.fetch_changes_dict()