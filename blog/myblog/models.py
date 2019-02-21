from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


from django.urls import reverse


# 分类
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='类名', )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "类别管理"
        verbose_name_plural = verbose_name


# 标签
class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name='标签名称', )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "标签管理"
        verbose_name_plural = verbose_name


# 文章
class Post(models.Model):
    title = models.CharField(max_length=70, verbose_name='文章标题')
    body = RichTextUploadingField(verbose_name='文章正文')
    created_time = models.DateTimeField(verbose_name='创建时间', )
    modified_time = models.DateTimeField(verbose_name='修改时间', )
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')
    category = models.ForeignKey(Category, verbose_name='文章类别', )
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='文章标签', )
    author = models.ForeignKey(User, verbose_name='文章作者', )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:详情', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "文章管理"
        verbose_name_plural = verbose_name
