from .db import db

class Item(db.Document):
    name = db.StringField(required=True)
    manufacturer = db.StringField()
    price = db.IntField()
    stock = db.BooleanField(required=True)
    url = db.URLField(required=True)
    lastStocked = db.DateTimeField()
    date_added =db.DateTimeField()
    img_url = db.URLField(required=True)
    meta = {'collection': 'items'}

    def __str__(self) -> str:
        if self.stock:
            stock_msg = "# **In stock**"
        else:
            stock_msg = '> Out of stock'
        return "{}\n[${}]({})\n{}\n < Last in stock: {} >\n".format(
            self.name, self.price, self.url, stock_msg, self.lastStocked)

# {"item_name" : "Rogue 45LB Ohio Power Bar - Bare Steel", 'restock': true, 'time': '7:15PM', 'date': '13/03/2021'}
class Change(db.Document):
    item_name = db.StringField(required=True)
    restock = db.BooleanField(required=True)
    timestamp = db.DateTimeField(required=True)
    meta = {'collection': 'changes'}

class Taskmeta(db.DynamicDocument):
    status = db.StringField()
    result = db.ListField()
    children = db.ListField()
    date_done = db.DateTimeField()
    meta = {'collection' : 'taskmeta'}