from VirtualJudgeSpider.Control import Controller


def get_problem_from_origin_online_judge(remote_oj, remote_id):
    response = Controller.get_problem(remote_oj, remote_id)
    if response:
        return response.get_dict()
    return None
