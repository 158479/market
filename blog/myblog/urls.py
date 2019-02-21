from django.conf.urls import url

from myblog.views import BlogIndex, BlogDetail, CommentView

urlpatterns = [
    url(r'^(?P<cate_id>\d*)_{1}(?P<tag_id>\d?)\.html$',BlogIndex.as_view(),name='博客首页'),
    url(r'^detail/(?P<id>\d+)$',BlogDetail.as_view(),name='详情'),
    url(r'^comment/(?P<post_pk>\d+)$',CommentView.as_view(),name='留言')
]