from VirtualJudgeSpider.Control import Controller


def get_problem_from_origin_online_judge(remote_oj, remote_id):
    return Controller.get_problem(remote_oj, remote_id).get_dict()
