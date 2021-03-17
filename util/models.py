import mongoengine

class Item(mongoengine.Document):
    name = mongoengine.StringField(required=True)
    manufacturer = mongoengine.StringField()
    price = mongoengine.IntField()
    stock = mongoengine.BooleanField(required=True)
    url = mongoengine.URLField(required=True)
    lastStocked = mongoengine.DateTimeField()
    date_added =mongoengine.DateTimeField()
    img_url = mongoengine.URLField(required=True)
    meta = {'collection': 'items'}

    def __str__(self) -> str:
        if self.stock:
            stock_msg = "# **In stock**"
        else:
            stock_msg = '> Out of stock'
        return "{}\n[${}]({})\n{}\n < Last in stock: {} >\n".format(
            self.name, self.price, self.url, stock_msg, self.lastStocked)

# {"item_name" : "Rogue 45LB Ohio Power Bar - Bare Steel", 'restock': true, 'time': '7:15PM', 'date': '13/03/2021'}
class Change(mongoengine.Document):
    item_name = mongoengine.StringField(required=True)
    restock = mongoengine.BooleanField(required=True)
    timestamp = mongoengine.DateTimeField(required=True)
    meta = {'collection': 'changes'}

class Taskmeta(mongoengine.DynamicDocument):
    status = mongoengine.StringField()
    result = mongoengine.ListField()
    children = mongoengine.ListField()
    date_done = mongoengine.DateTimeField()
    meta = {'collection' : 'taskmeta'}