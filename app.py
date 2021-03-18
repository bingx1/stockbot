from flask import Flask, jsonify, request, render_template
from util.db_handler import DbHandler
from celeryfile.tasks import make_celery
import requests
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'items',
    'host': 'localhost',
    'port': 27017
}

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
    items = DbHandler.fetch_items_dict(2)
    return render_template('index.html', title='Home', items=items)


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

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/items')
def get_items():
    all_items = DbHandler.fetch_items_dict()
    return render_template('items.html', number=len(all_items), items=all_items)


@app.route('/dashboard')
def dashboard():
    recent_changes = DbHandler.fetch_changes_dict(3)
    items = DbHandler.fetch_items_dict()
    in_stock = [item for item in items if item['stock']]
    last_update = DbHandler.fetch_taskresults_dict(1)
    date = last_update[0]['date_done']
    date = datetime(int(date[:4]),int(date[5:7]),int(date[8:10]),int(date[11:13]), int(date[14:16]))
    time_formatted = date.strftime(r"%A, %b %d %I:%M%p")
    return render_template('dashboard.html', date = time_formatted, changes=recent_changes, items=in_stock)


if __name__ == "__main__":
    app.run(debug=True)
