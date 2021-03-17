result_backend = 'mongodb://localhost:27017/'
mongodb_backend_settings = {
    'database': 'items',
    'taskmeta_collection': 'taskmeta',
}
timezone = 'Australia/Melbourne'
broker_url = 'redis://localhost:6379/0'
#used to schedule tasks periodically and passing optional arguments 
beat_schedule = {
    'every-minute': {
        'task': 'app.add',
        'schedule': 30.0,
        'args': (1,2)
    },
}