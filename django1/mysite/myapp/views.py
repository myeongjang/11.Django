from django.shortcuts import render
import json

# Create your views here.
from myapp.models import Question, Choice

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
# 요청 및 응답을 처리하는 django의 view(mvc 관점에선 controller)단 로직 처리 클래스
'''
    1. 모든 요청(crud)를 중앙집중형으로 하나의 views.py에서 처리
    2. 사용자 정의 메소드로 구분해서 개발
        1. 단순 메인 화면
        2. 상세보기 화면
        3. 수정 
        4. 삭제
        ...
'''
# http://ip:port/myapp에서 실현되는 함수
# 로직 : 입력되는 데이터(client가 전송하는 데이터)는 없이 응답
#응답 데이터 : 질문 리스트
# DB에 저장된 데이터 검색해서 응답 가능한 화면으로 데이터 처리 위임

#API : request: HttpRe
def index(request):
    print("---------index()-------------")
    latest_question_list = Question.objects.all().order_by('-pub_date')[:5]
    print(latest_question_list)
    context = {'latest_question_list': latest_question_list}
    return render(request, 'myapp/index.html', context)
# http://127.0.0.1:8000/myapp/1/
# myapp/urls.py의 설정 path값
# path('<int:question_id>/', views.detail, name='detail'),
# myapp의 url이 기본 상태에서 정수형의 값이 url의 일부로 요청
# client가 동작(event 발생)을 수행 하면 1라는 값이 두번째 parameter로 유입
# 함수명 자유롭게(첫번째:HttpRequest객체, 두번째:int형의 유입되는 데이터)

def detail(request, question_id):
    print("---------detail()-------------")
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'myapp/detail.html', {'question' : question})

def vote(request, question_id):
    print("---------vote()-------------")
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request, 'myapp/detail.html', {'question':question, 'error_message' : '선택 불가입니다'})

    selected_choice.votes += 1
    selected_choice.save()
    print("---------vote() return전-------------")
    return HttpResponseRedirect(reverse('myapp:results', args=(question.id,)))

#폼 데이터 처리 결과를 보여주는 로직
def results(request, question_id):
    print("---------results()-------------")
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'myapp/results.html', {'question':question})


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