from flask import Flask, jsonify, request, render_template
from util.db import initialize_db
from util.mongo_adaptor import MongoAdaptor
from celeryfile.celeryinit import make_celery
from routes.webpages import webpages
import requests
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)
app.register_blueprint(webpages)
app.config['MONGODB_SETTINGS'] = {
    'db': 'items',
    'host': 'localhost',
    'port': 27017
}

celery = make_celery(app)
initialize_db(app)
MongoAdaptor = MongoAdaptor()

@celery.task()
def update_item_status():
    items = MongoAdaptor.get_items()
    changes = fetch_and_parse(items)
    update_changes(changes)
    return changes


def update_changes(changes):
    for change in changes:
        MongoAdaptor.put_change(change)
    return


def fetch_and_parse(items):
    changes = []
    with requests.Session() as session:
        for item in items:
            response = session.get(item.url)
            change = parse_and_return(response, item)
            if change:
                changes.append(change)
    return changes


def parse_and_return(html, item):
    soup = BeautifulSoup(html.text, 'html.parser')
    change = False
    if soup.find(class_="button btn-size-m red full"):
        # Item has been restocked
        if not item.stock:
            print('Restocked!')
            item.lastStocked = datetime.now()
            item.stock = True
            change = True
    else:
        # Item is now out of stock
        if item.stock:
            print('Now OOS')
            item.stock = False
            change = True
    item.save()
    if change:
        return [item.name, item.stock, datetime.now()]
    else:
        return None





if __name__ == "__main__":
    app.run(debug=True)
