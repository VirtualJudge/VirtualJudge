from django.urls import path

from contest import views

urlpatterns = [
    # 获取比赛列表
    path('contests/', views.ContestListAPI.as_view(), name='contests'),
    # 新建比赛
    path('contest/', views.ContestAPI.as_view(), name='contest'),
    # 获取比赛信息
    #    path('contest/<int:contest_id>/'),
    # 获取比赛题目列表
    #   path('contest/<int:contest_id>/problems/'),
    # 获取比赛提交列表
    #  path('contest/<int:contest_id>/submissions/'),
]
