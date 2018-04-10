import traceback

from celery import shared_task

from submission.dispatcher import SubmissionDispatcher
from submission.models import Submission


@shared_task
def submit_task(submission_id):
    try:
        submission = Submission.objects.get(id=submission_id)
        tries = 3
        while tries > 0 and SubmissionDispatcher(submission.id).submit() is False:
            tries -= 1
    except:
        traceback.print_exc()
