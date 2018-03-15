class JudgeRequest:
    status = {
        "PENDING": 0,
        "JUDGING": 1,
        "SUCCESS": 2,
        "SEND_FOR_JUDGE_ERROR": 3,
        "RETRY": 4,
    }


class ProblemRequest:
    status = {
        "PENDING": 0,
        "CRAWLING": 1,
        "SUCCESS": 2,
        "ERROR": 3,
        "RETRY": 4
    }
