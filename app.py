from flask import Flask, jsonify, request, render_template
from util.db_handler import DbHandler
from tasks import make_celery

app = Flask(__name__)
DbHandler = DbHandler() 
celery = make_celery(app)

@celery.task()
def add(a, b):
    return a + b

@app.route('/index')
@app.route('/')
def index():
    all_items = DbHandler.fetch_items_dict()
    return render_template('index.html', title='Home', items=all_items[:2])

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/search', methods = ['GET','POST'])
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
    return render_template('items.html', number = len(all_items), items = all_items)


@app.route('/dashboard')
def dashboard():
    all_changes = DbHandler.fetch_changes_dict()
    items = DbHandler.fetch_items_dict()
    in_stock = [item for item in items if item['stock']]
    return render_template('dashboard.html', number=10, changes = all_changes, items=in_stock)

if __name__ == "__main__":
    app.run(debug=True)
