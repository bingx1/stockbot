from flask import Blueprint, render_template, request
from util.mongo_adaptor import MongoAdaptor
from datetime import datetime
MongoAdaptor = MongoAdaptor()

webpages = Blueprint('webpages', __name__, template_folder='templates')

@webpages.route('/index')
@webpages.route('/')
def index():
    items = MongoAdaptor.fetch_items_dict(2)
    return render_template('index.html', title='Home', items=items)


@webpages.route('/about')
def about():
    return render_template('about.html')


@webpages.route('/search', methods=['GET', 'POST'])
def search():
    items = MongoAdaptor.fetch_items_dict()
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

@webpages.route('/faq')
def faq():
    return render_template('faq.html')

@webpages.route('/items')
def get_items():
    all_items = MongoAdaptor.fetch_items_dict()
    return render_template('items.html', number=len(all_items), items=all_items)


@webpages.route('/dashboard')
def dashboard():
    recent_changes = MongoAdaptor.fetch_changes_dict(3)
    items = MongoAdaptor.fetch_items_dict()
    in_stock = [item for item in items if item['stock']]
    last_update = MongoAdaptor.fetch_taskresults_dict(1)
    date = last_update[0]['date_done']
    date = datetime(int(date[:4]),int(date[5:7]),int(date[8:10]),int(date[11:13]), int(date[14:16]))
    time_formatted = date.strftime(r"%A, %b %d %I:%M%p")
    return render_template('dashboard.html', date = time_formatted, changes=recent_changes, items=in_stock)