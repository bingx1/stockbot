import mongoengine
import json
from util.models import Change, Item

class Connection:
    def __enter__(self):
        self.conn = mongoengine.connect(db="items")
        print("Connected to mongodb")
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

class DbHandler():

    def __init__(self):
        self.db = "items"

    def put_item(self, json_input: json) -> None:
        ''' Puts an item using the json data passed into the database''' 
        new_item = Item.from_json(json_input)
        with Connection():
            if not self.exists(new_item.name):
                new_item.save()
                print("{} succesfully added. Now tracking {}".format(
                    new_item.name, new_item.name))
            else:
                print("Item already exists in the database. {} is already being tracked by the stock bot".format(
                    new_item.name))
        return


    def put_change(self, change_data):
        ''' change_data = [item.name, item.stock, datetime.now()] '''
        new_change = Change(item_name = change_data[0], restock = change_data[1], timestamp = change_data[2])
        with Connection():
            new_change.save()
        return

    def exists(self, item_name: str) -> bool:
        ''' Checks to see whether an item with the same name already exists in the database'''
        for item in Item.objects:
            if item.name == item_name:
                return True
        return False

    def list_tracked_items(self):
        ''' Returns a list of the items currently in the database as strings''' 
        output = ""
        with Connection():
            for index, item in enumerate(Item.objects):
                s = '{}. {} \n'.format(index + 1, item.name)
                output += s
                print(s)
        return output

    def fetch_items_dict(self):
        ''' Returns a list of items as python dictionaries'''
        with Connection():
            return [item._data for item in Item.objects]

    def fetch_changes_dict(self):
        ''' Returns a list of changes as python dictionaries'''
        with Connection():
            return [change._data for change in Change.objects]

    def get_items(self):
        ''' Returns a list of all the Item objects in the database'''
        with Connection():
            return Item.objects

    def get_changes(self):
        ''' Returns a list of all the Item objects in the database'''
        with Connection():
            return Change.objects

if __name__ == "__main__":
    db = DbHandler()
    x = db.fetch_items_dict()
    print(x)
