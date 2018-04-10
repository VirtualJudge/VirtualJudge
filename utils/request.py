from enum import Enum


class JudgeRequest(Enum):
    status = {
        "PENDING": 0,
        "JUDGING": 1,
        "SUCCESS": 2,
        "SEND_FOR_JUDGE_ERROR": 3,
        "RETRY": 4,
    }

