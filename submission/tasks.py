from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist

from submission.dispatcher import SubmissionDispatcher
from submission.models import Submission


@shared_task
def submit_task(submission_id):
    try:
        submission = Submission.objects.get(id=submission_id)
        SubmissionDispatcher(submission.id).submit
    except ObjectDoesNotExist:
        import traceback
        traceback.print_exc()
