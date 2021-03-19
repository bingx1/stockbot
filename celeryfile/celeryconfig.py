result_backend = 'mongodb://localhost:27017/'
mongodb_backend_settings = {
    'database': 'items',
    'taskmeta_collection': 'taskmeta',
}
timezone = 'Australia/Melbourne'
broker_url = 'redis://localhost:6379/0'
worker_prefetch_multiplier = 1
imports = ['util.mongo_adaptor', 'util.scraper_handler']
#used to schedule tasks periodically and passing optional arguments 
beat_schedule = {
    'every-minute': {
        'task': 'celeryfile.tasks.update_item_status',
        'schedule': 30.0,
    },
}