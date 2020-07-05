from django.urls import path,re_path
from . import views

app_name = 'quiz'


urlpatterns = [
    path('save/', views.SaveUserChoicesAPIView.as_view(), name='quizSave'),
    path('submit/', views.SubmitQuiz.as_view(), name='quizSubmit'),
    path('', views.QuizListAPIView.as_view(), name='quizList'),
    path('<int:pk>/', (views.QuizDetailAPIView.as_view()), name="quizDetails"),
]