from bookmyshow import app
from .services import get_user_data
from bookmyshow.celery import celery

@celery.task(bind=True, ignore_result=False)
def fetch_user_data(self, user_id):
  """Background task to get User Data"""
  with app.test_request_context():
    return get_user_data(user_id)
