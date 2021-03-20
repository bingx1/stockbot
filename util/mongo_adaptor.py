import json
from util.models import Change, Item, Taskmeta, Configuration

class MongoAdaptor():

    def put_item(self, json_input: json) -> None:
        ''' Puts an item using the json data passed into the database''' 
        new_item = Item.from_json(json_input)
        if not self.exists(new_item.name):
            new_item.save()
            print("{} succesfully added. Now tracking {}".format(
                new_item.name, new_item.name))
        else:
            print("Item already exists in the database. {} is already being tracked by the stock bot".format(
                new_item.name))
        return


    def put_change(self, change_data):
        ''' Puts an item using the change data passed into the database '''
        new_change = Change(item_name = change_data[0], restock = change_data[1], timestamp = change_data[2])
        new_change.save()
        return

    def exists(self, item_name: str) -> bool:
        ''' Checks to see whether an item with the same name already exists in the database'''
        for item in Item.objects:
            if item.name == item_name:
                return True
        return False


    def fetch_items_dict(self, num = None):
        ''' Returns a list of items as python dictionaries'''
        if not num:
            return [item._data for item in Item.objects]    
        else:
            return [item._data for item in Item.objects[:num]]

    def fetch_changes_dict(self, num= None):
        ''' Returns a list of changes as python dictionaries'''
        if not num:
            return [change._data for change in Change.objects().order_by('-timestamp')]
        else:
            return [change._data for change in Change.objects().order_by('-timestamp')[:num]]

    def fetch_taskresults_dict(self, num):
        return [taskmeta._data for taskmeta in Taskmeta.objects().order_by('-date_done')[:num]]

    def get_items(self):
        ''' Returns a list of all the Item objects in the database'''
        return Item.objects

    def get_changes(self):
        ''' Returns a list of all the Item objects in the database'''
        return Change.objects

    def make_config(self, config_list):
        output = []
        for config in config_list:
            output.append(Configuration(config_name = config['config_name'], stock = config['stock']))
        print(output)
        return output