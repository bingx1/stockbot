from flask import Blueprint
from util.db_handler import DbHandler

items_api = Blueprint('items_api', __name__)
dbHandler = DbHandler()

@items_api.route('/api/items/all', methods=['GET'])
def fetch_all_items():
    return 