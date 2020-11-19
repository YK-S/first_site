from django.db import models

# Create your models here.
class User(models.Model):
    user_name = models.CharField(max_length=32, primary_key=True, blank=False)
    user_pwd = models.CharField(max_length=32, blank=False)

    class Meta:
        db_table = 'user'



class Vote(models.Model):
    # 自动生成id primary key
    type = (
        (0, '单选公开'),
        (1, '单选不公开'),
        (2, '多选公开'),
        (3, '多选不公开')
    )
    vote_name = models.CharField(max_length=32, blank=False, null=False)    # 禁止为None 或者 null
    vote_type = models.IntegerField(choices=type, blank=False)    # 枚举
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=False)
    builder = models.ForeignKey('User', on_delete=models.CASCADE, blank=False)     # 联级删除
    vote_details = models.TextField(null=True)  # 详细描述

    class Meta:
        db_table = 'vote'


class Item(models.Model):
    content = models.TextField(blank=False, null=False)
    poll = models.IntegerField(default=0)
    vote = models.ForeignKey('Vote', on_delete=models.CASCADE, blank=True)
    class Meta:
        db_table = 'item'

