from celery import shared_task
from judge.dispatcher import SpiderDispatcher


@shared_task
def submit_task(submission_id):
    SpiderDispatcher(submission_id).submit()
