from flask import Blueprint
from util.mongo_adaptor import MongoAdaptor
MongoAdaptor = MongoAdaptor()

items_api = Blueprint('items_api', __name__)

@items_api.route('/api/items/', methods=['GET'])
def items():
    return MongoAdaptor.fetch_items_dict()

@items_api.route('/api/changes/', methods=['GET'])
def changes():
    return MongoAdaptor.fetch_changes_dict()