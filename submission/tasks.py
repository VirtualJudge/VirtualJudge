from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from spider import config
from spider.platforms.codeforces import Codeforces
from submission.dispatcher import SubmissionDispatcher
from submission.models import Submission
from support.models import Support


@shared_task
def submit_task(submission_id):
    try:
        submission = Submission.objects.get(id=submission_id)
        if Support.objects.get(oj_name=submission.remote_oj).oj_reuse or submission.remote_oj in [Codeforces.__name__]:
            result_set = Submission.objects.filter(Q(create_time__lt=submission.create_time) &
                                                   Q(remote_oj=submission.remote_oj) &
                                                   Q(remote_id=submission.remote_id) &
                                                   Q(sha256=submission.sha256) &
                                                   Q(language=submission.language) &
                                                   ~Q(id=submission.id)).order_by('create_time')
            if result_set:
                history = result_set.first()
                submission.unique_key = history.unique_key
                submission.execute_memory = history.execute_memory
                submission.execute_time = history.execute_time
                submission.verdict = history.verdict
                submission.verdict_info = history.verdict_info
                submission.compile_info = history.compile_info
                submission.status = config.Result.Status.STATUS_RESULT_SUCCESS.value
                submission.save()
            else:
                SubmissionDispatcher(submission.id).submit()
        else:
            SubmissionDispatcher(submission.id).submit()
    except ObjectDoesNotExist:
        import traceback
        traceback.print_exc()
