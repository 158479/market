from django.core import paginator
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from db.base_view import VerifyLoginView
from myblog.models import Post, Category, Tag


# 首页
from users.forms import CommentForm
from users.models import Comment


class BlogIndex(View):
    def get(self, request, cate_id, tag_id):
        # 查询所有分类
        categorys = Category.objects.all()
        # 取出第一个分类
        if cate_id == "":
            category = categorys.first()
            cate_id = category.pk
        else:
            # 根据分类id查询对应的分类
            cate_id = int(cate_id)
            category = Category.objects.get(pk=cate_id)
        # 查询对应分类下的文章
        posts = Post.objects.filter(category_id=category)
        # 查询所有标签
        tags = Tag.objects.all()
        if tag_id == '':
            tag = tags.first()
            tag_id = tag.pk
        else:
            tag_id = int(tag_id)
            tag = Tag.objects.get(pk=tag_id)
        result = Post.objects.filter(tags=tag)

        # 分页
        paginator = Paginator(posts, 5)  # 每页显示n条记录
        # 获取当前页码数据
        page = request.GET.get('page', 1)  # 当前页码?Page=1
        # 获取对应页码数据
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            # 页码不是整数 显示第一页
            posts = paginator.page(1)
        except EmptyPage:
            # 页码为空 显示最后一页
            posts = paginator.page(paginator.num_pages)
        context = {
            'posts': posts,
            'result': result,
            'cate_id': cate_id,
            'tag_id': tag_id,
            'categorys':categorys,
            'tags':tags,
        }
        return render(request, 'myblog/index.html', context=context)

    def post(self, request):
        pass


# 详情
class BlogDetail(View):
    def get(self, request, id):
        post = Post.objects.get(pk=id, is_delete=False)
        comment = Comment.objects.filter(post_id=id,is_delete=False)
        categorys = Category.objects.all()
        tags = Tag.objects.all()
        paginator = Paginator(comment, 5)  # 每页显示n条记录
        # 获取当前页码数据
        page = request.GET.get('page', 1)  # 当前页码?Page=1
        # 获取对应页码数据
        try:
            comment = paginator.page(page)
        except PageNotAnInteger:
            # 页码不是整数 显示第一页
            comment = paginator.page(1)
        except EmptyPage:
            # 页码为空 显示最后一页
            comment = paginator.page(paginator.num_pages)
        context = {
            'post': post,
            'comment':comment,
            'categorys':categorys,
            'tags':tags

        }
        return render(request, 'myblog/info.html', context=context)

    def post(self, request):
        pass

class CommentView(VerifyLoginView):
    def get(self,request):
        return render(request,'user/login.html')

    def post(self,request,post_pk):
        try:
            post = Post.objects.filter(pk=post_pk,
                                       is_delete=False
                                       )
        except Post.DoesNotExist:
            return redirect('blog:首页')

        # 接收参数
        data = request.POST
        form = CommentForm(data)
        # 接收用户的id
        user_id = request.session.get("ID")
        # 验证数据的合法性
        if form.is_valid():
            # 获取清洗后的数据
            cleaned = form.cleaned_data
            # 取出清洗后的评论
            text = cleaned.get('text')
            # 保存到数据库
            Comment.objects.create(text=text,post_id=post_pk)
            return redirect('blog:详情' ,post_pk)
        else:
            return redirect('blog:详情', post_pk)

