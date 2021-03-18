from celery import Celery

def make_celery(app):
    celery = Celery('__name__')
    celery.config_from_object('celeryfile.celeryconfig')

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery



