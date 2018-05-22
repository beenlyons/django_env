'''定义learning_logs的url模式'''
from django.urls import path, include, re_path
from django.contrib import admin
from . import views

app_name = 'learning_logs'
urlpatterns = [
    # 主页
    path(r"", views.index, name='index'), # 匹配开头和结尾没有任何东西的正则表达式
    # path("index", views.index, name="Index"),
    path("topics/", views.topics, name='topics'),
    # re_path("^topics/(?P<topic_id>\d+)/$", views.topic, name='topic'), # 用正则表达式匹配数字
    # path("<int:topic_id>/", views.topic, name='topic'), # url特定形式匹配数字
    path("topics/<int:topic_id>/", views.topic, name='topic'),
    path("new_topic", views.new_topic, name="new_topic"),
    path("new_entry/<int:topic_id>/", views.new_entry, name="new_entry"),
    path("edit_entry/<int:entry_id>/", views.edit_entry, name="edit_entry")
]