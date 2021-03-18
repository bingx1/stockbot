from flask import Flask, jsonify, request, render_template
from util.db import initialize_db
from celeryfile.celeryinit import make_celery
from routes.webpages import webpages
from routes.items_api import items_api


app = Flask(__name__)
app.register_blueprint(webpages)
app.register_blueprint(items_api)
app.config['MONGODB_SETTINGS'] = {
    'db': 'items',
    'host': 'localhost',
    'port': 27017,
    'connect': False
}

celery = make_celery(app)
celery.autodiscover_tasks(['celeryfile'])
initialize_db(app)


if __name__ == "__main__":
    app.run(debug=True)
