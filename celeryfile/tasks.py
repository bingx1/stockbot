from celery import shared_task
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from util.mongo_adaptor import MongoAdaptor
from util.scraper_handler import ScraperHandler
MongoAdaptor = MongoAdaptor()
ScraperHandler = ScraperHandler()

@shared_task()
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
    parsed = ScraperHandler.parse(item.url, soup)
    if parsed['stock']:
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
    if 'config' in parsed:
        print('hello')
        config = MongoAdaptor.make_config(parsed['config'])
        item.config = config
    item.save()
    if change:
        return [item.name, item.stock, datetime.now()]
    else:
        return None