from django.core.validators import MinLengthValidator
from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=20,
                                validators=[
                                    MinLengthValidator(4)
                                ])
    password = models.CharField(max_length=40)

    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'users'