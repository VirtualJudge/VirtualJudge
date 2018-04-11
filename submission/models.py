from django.db import models
from VirtualJudgeSpider import Config


class Submission(models.Model):
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True)
    """
    至少提交的部分
    """
    # User
    user = models.CharField(max_length=100, null=True)
    # 题目编号
    problem_id = models.IntegerField()
    # 比赛编号，可没有
    contest_id = models.IntegerField(null=True)
    # 要提交的代码
    code = models.TextField()
    # 提交的语言
    language = models.CharField(max_length=20)
    """
    通过problem_id获取的部分
    """
    # 源题目OJ
    remote_oj = models.CharField(max_length=20, null=True)
    # 源题目id
    remote_id = models.CharField(max_length=20, null=True)

    """
    源oj返回的结果
    """
    remote_run_id = models.CharField(max_length=20, null=True)
    # 返回的结果
    verdict = models.CharField(max_length=40, null=True)
    # 返回结果是否已经结束
    verdict_status = models.BooleanField(default=False)
    # 程序运行时间
    execute_time = models.CharField(max_length=20, null=True)
    # 程序运行内存
    execute_memory = models.CharField(max_length=20, null=True)
    # 编译信息
    compile_info = models.TextField(null=True)
    """
        即时修改爬虫状态
    """

    # 当前爬虫状态
    status = models.IntegerField(default=Config.Result.Status.STATUS_PENDING.value)

    class Meta:
        db_table = 'submission'
        ordering = ("-create_time",)
