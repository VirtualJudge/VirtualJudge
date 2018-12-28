from django.db import models
from spider import config


class Submission(models.Model):
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True)
    """
    至少提交的部分
    """
    # User
    user = models.CharField(max_length=20)
    # 要提交的代码
    code = models.TextField()
    # 提交的语言
    language = models.CharField(max_length=20)

    language_name = models.CharField(max_length=30, null=True)
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
    unique_key = models.CharField(max_length=20, null=True)
    # 返回的结果
    verdict_info = models.CharField(max_length=40, null=True, blank=True)
    # 返回结果是那种类型
    verdict = models.CharField(default=config.Result.Status.STATUS_PENDING.value, max_length=50)
    # 程序运行时间
    execute_time = models.CharField(max_length=20, null=True)
    # 程序运行内存
    execute_memory = models.CharField(max_length=20, null=True)
    # 编译信息
    compile_info = models.TextField(null=True, blank=True)
    """
        即时修改爬虫状态
    """

    # 当前爬虫状态
    sha256 = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=50, default=config.Result.Status.STATUS_PENDING.value)

    hook = models.BooleanField(default=False)

    reloadable = models.BooleanField(default=False)

    class Meta:
        db_table = 'submission'
        ordering = ("-create_time",)
