from django.core.validators import MinLengthValidator
from django.db import models

# Create your models here.


class User(models.Model):
    sex_choices = (
        (1, '男'),
        (2, "女"),
        (3,'保密')
    )
    phone = models.CharField(max_length=20,
                                validators=[
                                    MinLengthValidator(4)
                                ])
    password = models.CharField(max_length=40)
    head_portrait = models.CharField(max_length=260)
    username = models.CharField(max_length=20,default=False)
    sex = models.SmallIntegerField(choices=sex_choices,default=1)
    school = models.CharField(max_length=50,default=False)
    address = models.CharField(max_length=100,default=False)
    hometown = models.CharField(max_length=70,default=False)
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'users'