from flask import Flask, jsonify, request, render_template
from util.db_handler import DbHandler
from tasks import make_celery
import requests
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)
DbHandler = DbHandler()
celery = make_celery(app)


@celery.task()
def update_item_status():
    items = DbHandler.get_items()
    changes = fetch_and_parse(items)
    update_changes(changes)
    return changes


def update_changes(changes):
    for change in changes:
        DbHandler.put_change(change)
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
        print('Restocked!')
        if not item.stock:
            item.lastStocked = datetime.now()
            item.stock = True
            change = True
    else:
        print('Now OOS')
        # Item is now out of stock
        if item.stock:
            item.stock = False
            change = True
    item.save()
    if change:
        return [item.name, item.stock, datetime.now()]
    else:
        return None


@app.route('/index')
@app.route('/')
def index():
    all_items = DbHandler.fetch_items_dict()
    return render_template('index.html', title='Home', items=all_items[:2])


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    items = DbHandler.fetch_items_dict()
    if request.method == 'POST':
        req = request.form
        print(req)
        query = req.get('search')
        query_result = parse_query(query, items)
        return render_template('search_results.html', items=query_result, query=query)
    return render_template('search.html')


def parse_query(query, items):
    queries = query.split()
    result = []
    for item in items:
        for q in queries:
            if q in item['name'].lower().split():
                result.append(item)
    return result


@app.route('/items')
def get_items():
    all_items = DbHandler.fetch_items_dict()
    return render_template('items.html', number=len(all_items), items=all_items)


@app.route('/dashboard')
def dashboard():
    all_changes = DbHandler.fetch_changes_dict()
    items = DbHandler.fetch_items_dict()
    in_stock = [item for item in items if item['stock']]
    return render_template('dashboard.html', number=10, changes=all_changes, items=in_stock)


if __name__ == "__main__":
    app.run(debug=True)
