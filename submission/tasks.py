from celery import shared_task, Task

from submission.dispatcher import SpiderDispatcher, SubmissionException
import time


class SubmissionTask(Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('on_failure execute')


@shared_task(bind=True, base=SubmissionTask)
def submit_task(self, submission_id):
    try:
        SpiderDispatcher(submission_id).submit()
    except SubmissionException as e:
        time.sleep(2)
        self.retry(exc=e, max_retries=15)
