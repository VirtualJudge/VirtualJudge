import traceback

from celery import shared_task

from submission.dispatcher import SubmissionDispatcher
from submission.models import Submission
from django.core.exceptions import ObjectDoesNotExist


@shared_task
def submit_task(submission_id):
    try:
        submission = Submission.objects.get(id=submission_id)
        SubmissionDispatcher(submission.id).submit()
    except ObjectDoesNotExist:
        import traceback
        traceback.print_exc()
