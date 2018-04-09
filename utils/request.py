from enum import Enum
class JudgeRequest(Enum):
    status = {
        "PENDING": 0,
        "JUDGING": 1,
        "SUCCESS": 2,
        "SEND_FOR_JUDGE_ERROR": 3,
        "RETRY": 4,
    }


class ProblemStatus(Enum):
    STATUS_PENDING = 0
    STATUS_RUNING = 1
    STATUS_CRAWLING_SUCCESS = 2
    STATUS_NETWORK_ERROR = 3
    STATUS_PROBLEM_NOT_EXIST = 3
