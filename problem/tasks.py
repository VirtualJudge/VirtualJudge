from celery import shared_task

from problem.models import Problem


# remote run task
@shared_task(name='retrieve_problem_task')
def retrieve_problem_task(remote_oj, remote_id, problem_id=None):
    print(problem_id, remote_oj, remote_id)
    result_problem_task.apply_async(
        args=[problem_id, remote_oj, remote_id, '1000MS', '256MB', '', f'TEST:{remote_oj}-{remote_id}',
              f'{remote_oj}-{remote_id}'],
        queue='result')


# call back task
@shared_task(name='result_problem_task')
def result_problem_task(problem_id, remote_oj, remote_id, time_limit, memory_limit, content, remote_url, title):
    if problem_id:

        problem = Problem.objects.get(id=problem_id)
        problem.remote_oj = remote_oj
        problem.remote_id = remote_id
        problem.time_limit = time_limit
        problem.memory_limit = memory_limit
        problem.content = content
        problem.remote_url = remote_url
        problem.title = title
        problem.save()
    else:
        Problem(
            remote_oj=remote_oj,
            remote_url=remote_url,
            remote_id=remote_id,
            memory_limit=memory_limit,
            time_limit=time_limit,
            title=title,
            content=content
        ).save()
