from django.urls import path

from contest import views

urlpatterns = [
    # 获取题集列表
    path('contests/', views.ContestListAPI.as_view(), name='contests'),
    # 新建题集
    path('contest/new/', views.ContestNewAPI.as_view(), name='contest_new'),
    # 获取题集的题目列表
    path('contest/<int:contest_id>/', views.ContestAPI.as_view(), name='contest'),
]
