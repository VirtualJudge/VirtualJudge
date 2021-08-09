from celery import shared_task

from problem.models import Problem


# remote run task
@shared_task(name='retrieve_problem_task')
def retrieve_problem_task(remote_oj, remote_id, problem_id=None):
    print(problem_id, remote_oj, remote_id)


# call back task
@shared_task(name='result_problem_task')
def result_problem_task(problem_id, remote_oj, remote_id, time_limit, memory_limit, remote_url, title, spj, content):
    if problem_id:
        problem = Problem.objects.get(id=problem_id)
        problem.remote_oj = remote_oj
        problem.remote_id = remote_id
        problem.time_limit = time_limit
        problem.memory_limit = memory_limit
        problem.content = content
        problem.remote_url = remote_url
        problem.title = title
        problem.spj = spj
        problem.save()
    else:
        Problem(
            remote_oj=remote_oj,
            remote_url=remote_url,
            remote_id=remote_id,
            memory_limit=memory_limit,
            time_limit=time_limit,
            title=title,
            content=content,
            spj=spj
        ).save()


@shared_task(name='sync_problem')
def sync_problem():
    for oj in ['Codeforces', 'HDU']:
        pids = [item['remote_id'] for item in Problem.objects.filter(remote_oj=oj).values('remote_id')]
        sync_problem_list.apply_async(
            args=[oj, pids],
            queue='requests'
        )
    # pids = [item['remote_id'] for item in Problem.objects.filter(remote_oj='Codeforces').values('remote_id')]
    # sync_problem_list.apply_async(
    #     args=['Codeforces', pids],
    #     queue='requests'
    # )


@shared_task(name='sync_problem_list')
def sync_problem_list(remote_oj: str, local_id_list: list[str]):
    print(remote_oj, local_id_list)
