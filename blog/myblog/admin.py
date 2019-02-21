from django.contrib import admin

# Register your models here.
from myblog.models import Post, Category, Tag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['is_delete', 'title', 'created_time', 'modified_time', 'category', 'author']
    # 设置可编辑连接字段
    list_display_links = ['is_delete', 'title', 'created_time', 'modified_time', 'category', 'author']


admin.site.register(Category)
admin.site.register(Tag)