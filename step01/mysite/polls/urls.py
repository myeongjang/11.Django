from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]

'''
http://localhost:8000/polls/
    path('', views.index, name='index'),

    1. '' : polls
    2. views.index
        -views - polls 라는 앱에 존재하는 views.py 파일
        -index - views 내의 함수
    3. name='index'
        다수의 path 설정이 존재할 경우 이름 설정
'''
