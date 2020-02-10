from django.db import models
from destination.models import Platform


class Problem(models.Model):
    # 平台名称
    platform = models.ForeignKey(Platform, on_delete=models.PROTECT)
    # 平台题目编号
    index = models.CharField(max_length=20)
    # 平台题目路径
    url = models.CharField(max_length=200, null=True)
    # 标题
    title = models.CharField(max_length=200, null=True)
    # 时间限制
    time_limit = models.CharField(max_length=20, null=True)
    # 内存限制
    memory_limit = models.CharField(max_length=20, null=True)
    # 特判
    spj = models.BooleanField(default=False)
    # 题目的主体内容
    html = models.TextField(blank=True, null=True)
    # 更新时间
    update_time = models.DateTimeField(auto_now=True)
    # 状态
    status = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.platform.name + '|' + self.index + '|' + self.title

    class Meta:
        ordering = ('update_time',)
        unique_together = ('platform', 'index')
        db_table = 'problem'


class Request(models.Model):
    # 平台名称
    platform = models.ForeignKey(Platform, on_delete=models.PROTECT)
    # 平台题目编号
    index = models.CharField(max_length=20)
    #
    user = models.IntegerField(null=False)

    submit_time = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.platform.name + '|' + self.index + '|' + self.index

    class Meta:
        db_table = 'request'
