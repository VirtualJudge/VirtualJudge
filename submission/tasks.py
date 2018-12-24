from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F
from submission.dispatcher import SubmissionDispatcher
from submission.models import Submission
from spider import config
from user.models import UserProfile


@shared_task
def submit_task(submission_id):
    try:
        submission = Submission.objects.get(id=submission_id)
        result_set = Submission.objects.filter(Q(create_time__lt=submission.create_time) and
                                               Q(remote_oj=submission.remote_oj) and
                                               Q(remote_id=submission.remote_id) and
                                               Q(sha256=submission.sha256) and
                                               Q(language=submission.language) and
                                               ~Q(id=submission.id)).order_by('create_time')
        if result_set:
            history = result_set.first()
            submission.remote_run_id = history.remote_run_id
            submission.execute_memory = history.execute_memory
            submission.verdict = history.verdict
            submission.verdict_code = history.verdict_code
            submission.compile_info = history.compile_info
            submission.status = config.Result.Status.STATUS_RESULT.value
            submission.save()
            if submission.verdict_code is config.Result.VerdictCode.VERDICT_ACCEPTED.value and len(
                    Submission.objects.filter(user=submission.user, remote_oj=submission.remote_oj,
                                              remote_id=submission.remote_id,
                                              verdict_code=config.Result.VerdictCode.VERDICT_ACCEPTED.value)) == 1:
                UserProfile.objects.filter(username=submission.user).update(accepted=F('accepted') + 1)

        else:
            SubmissionDispatcher(submission.id).submit()
    except ObjectDoesNotExist:
        import traceback
        traceback.print_exc()
