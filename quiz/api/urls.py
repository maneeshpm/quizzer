from django.urls import path,re_path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'quiz'


urlpatterns = [
    path('save/', views.SaveUserChoicesAPIView.as_view()),
    path('submit/', views.SubmitQuiz.as_view()),
    path('', views.QuizListAPIView.as_view(), name='quizList'),
    path('<int:pk>/', (views.QuizDetailAPIView.as_view()), name="quizDetails"),
]