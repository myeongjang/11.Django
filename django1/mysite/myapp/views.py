from django.shortcuts import render
import json

# Create your views here.
from myapp.models import Question, Choice

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse


#요청 및 응답을 처리하는 django의 view(mvc 관점에선 controller)단 로직 처리 클래스

'''
    1. 모든 요청(crud)를 중앙집중형으로 하나의 views.py에서 처리
    2. 사용자 정의 메소드로 구분해서 개발
        1. 단순 메인 화면
        2. 상세보기 화면
        3. 수정
        4. 삭제
        ...
'''

# http://ip:port/myapp에서 실행되는 함수
# 로직 : 입력되는 데이터(client가 전송하는 데이터)는 없이 응답
# 응답 데이터 : 질문 리스트
# DB에 저장된 데이터 검색해서 응답 가능한 화면으로 데이터 처리 위임

# API : request: HttpRequest, render() 반환값 : HttpResponse
def index(request):
    print("---------index()-------------")
    latest_question_list = Question.objects.all().order_by('-pub_date')[:5]
    print(latest_question_list)

    #html에서 사용하고자 하는 데이터를 dict 형태로 저장
    context = {'latest_question_list': latest_question_list, 'myname':'조명장'}
    return render(request, 'myapp/index.html', context)

# http://127.0.0.1:8000/myapp/5/
# myapp/urls.py의 설정 path값
# path('<int:question_id>/', views.detail, name='detail'),
# myapp의 url이 기본 상태에서 정수형의 값이 url의 일부로 요청
# client가 동작(event 발생)을 수행 하면 5라는 값이 두번째 parameter로 유입
# 함수명 자유롭게(첫번째:HttpRequest객체, 두번째:int형의 유입되는 데이터)
def detail(request, question_id):
    print("---------detail()-------------")
    question = get_object_or_404(Question, pk=question_id)
    friends = ['유재석', '신동엽', '이영자']
    return render(request, 'myapp/detail.html', {'question' : question, 'friends':friends})

# <form action="/myapp/5/vote/" method="post"> : detail.html
# 요청시 전송시킨 데이터 개수? 2개(choice=숫자)
# (보안을 고려한 기본 설정 : csrfmiddlewaretoken=난수값)
# request.POST['choice'] 
    # request - HttpRequest
    # .POST - post 요청 의미
    # ['choice'] - choice=5 형태로 전송된 데이터

# 처리 직후 실행되는 url - http://127.0.0.1:8000/myapp/7/results/
def vote(request, question_id):
    print("---------vote()-------------")
    question = get_object_or_404(Question, pk=question_id)
    try:
    
        #<input type="radio" name="choice" id="choice1" value="5" />
        '''
        question.choice_set.get(pk=request.POST['choice'])
        1. question : Model의 Question 즉 question table
        2. choice_set : xxx_set 즉 question의 pk를 fk로 보유하고 있는 
                        종관계의 table명을 소문자로 "자동변환_set"
                        모든 데이터 읨
        3. get() : 검색
        4. request.POST['choice']
            reuqest - client가 접속시 자동 생성되는 HttpRequest객체
            POST - post방식의 요청
            ['choice'] - choiec=값 구조로 전송된 데이터에서 값 반환코드
        '''
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        #<input type="text" name="myname" value="김혜경----">
        print('-', request.POST['myname'])

    except(KeyError, Choice.DoesNotExist):
        return render(request, 'myapp/detail.html', {'question':question, 'error_message' : '선택 불가입니다'})
    
    # 접속한 client의 지속적인 상태유지를 위한 개발 기술 : 세션
    # 세션에 해당 client의 정보를 저장 및 유지 및 활용
    request.session['myname'] = request.POST['myname']
    request.session['hiddenTag'] = request.POST['hiddenTag']
   
    #1씩 증가되는 counting 데이터 제작
    selected_choice.votes += 1
    #DB에 반영
    selected_choice.save()
    print("---------vote() return전-------------")
    return HttpResponseRedirect(reverse('myapp:results', args=(question.id,)))

	
#폼 데이터 처리 결과를 보여주는 로직
# http://127.0.0.1:8000/myapp/5/results/
# views.results함수 -> myapp/results.html
# 1씩 증가된 갱신된 투표 결과 보기 화면
# 갱신된 데이터 재 검색 -> results.html에 전송
def results(request, question_id):
    print("---------results()-------------")
    question = get_object_or_404(Question, pk=question_id)
    print('---', request.session['myname'])
    return render(request, 'myapp/results.html', {'question':question, 'myname':request.session['myname'], 'message':request.session['hiddenTag']})


#json 형태의 문자열로 응답 : 비동기
def ajaxRes(request):
    print("----- ajaxRes() -----")
    context = {'message': "비동기로 응답하는 데이터", 'age' : 20, 'like_count': 10, 'data':"['Task', 'Hours per Day'],['Work',     11],['Eat',      2],['Commute',  2],['Watch TV', 2],['Sleep',    7]"}
    return HttpResponse(json.dumps(context), content_type="application/json")



'''
* mysite/urls.py
    
urlpatterns = [
    path('admin/', admin.site.urls),
    path('myapp/', views.index, name='index'),
    path('myapp/<int:question_id>/', views.detail, name='detail'),
    path('myapp/<int:question_id>/results', views.results, name='results'),
    path('myapp/<int:question_id>/vote', views.vote, name='vote'),
]

'''