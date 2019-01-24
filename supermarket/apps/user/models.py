# -*- coding: utf-8 -*-
from django.core.validators import  RegexValidator
from django.db import models

# Create your models here.
from db.base_model import BaseModel

# 用户表
class User(BaseModel):
    sex_choices = (
        (1, "男"),
        (2, "女"),
    )
    phone = models.CharField(max_length=11,
                             verbose_name="手机号码",
                             validators=[
                                 RegexValidator(r'^1[3-9]\d{9}$', "手机号码格式错误!")
                             ])
    username = models.CharField(max_length=50,
                                null=True,
                                blank=True,
                                verbose_name="昵称"
                                )
    password = models.CharField(max_length=32,
                                verbose_name="密码"
                                )
    sex = models.SmallIntegerField(choices=sex_choices,
                                      default=1,
                                      verbose_name="性别"
                                      )
    school = models.CharField(max_length=50,
                                   null=True,
                                   blank=True,
                                   verbose_name="学校"
                                   )
    hometown = models.CharField(max_length=50,
                                null=True,
                                blank=True,
                                verbose_name="家乡"
                                )
    birth_of_date = models.DateField(null=True,
                                     blank=True,
                                     verbose_name="出生日期"
                                     )
    address = models.CharField(max_length=255,
                               null=True,
                               blank=True,
                               verbose_name="详细位置"
                               )

    # 设置头像字段
    head = models.ImageField(upload_to="head/%Y%m", default="head/memtx.png", verbose_name="用户头像")

    def __str__(self):
        return self.phone

    class Meta:
        db_table = "users"
        verbose_name = "用户管理"
        verbose_name_plural = verbose_name