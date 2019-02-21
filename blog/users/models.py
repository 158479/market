from django.db import models


# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=100, verbose_name='用户名')
    password = models.CharField(max_length=32, verbose_name='密码')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name


class Comment(models.Model):
    text = models.TextField(verbose_name='留言')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')
    post = models.ForeignKey('myblog.Post', verbose_name='评论')

    def __str__(self):
        return self.text[:20]

    class Mete:
        verbose_name = '评论管理'
        verbose_name_plural = verbose_name
