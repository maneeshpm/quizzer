from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.response import Response
from rest_framework import generics
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.utils.decorators import method_decorator
from quiz.models import Quiz, UserResponse, Choices, Question,PointTable
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import HTTP_400_BAD_REQUEST,HTTP_200_OK

from .serializers import (
    QuizListSerializer, 
    QuizDetailSerializer, 
    UserAnswerSerializer, 
    SubmitQuizSerializer
    )
import datetime
import pytz

class QuizListAPIView(generics.ListAPIView):
    serializer_class = QuizListSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = Quiz.objects.filter()
        return queryset
      
class QuizDetailAPIView(generics.RetrieveAPIView):
    serializer_class = QuizDetailSerializer
    permission_classes=[IsAuthenticated]
    def get_object(self, pk):
        try:
            return Quiz.objects.get(id=pk, isLive=True)
        except:
            raise Http404

    @method_decorator(login_required())
    def get(self, request, pk, format=None):
        quiz       = self.get_object(pk)
        serializer = QuizDetailSerializer(quiz)
        return Response(serializer.data)

class SaveUserChoicesAPIView(generics.UpdateAPIView):
    serializer_class =  UserAnswerSerializer
    permission_classes=[IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user    = request.user
        question = get_object_or_404(Question, id=request.data['question'])
        quiz     = get_object_or_404(Quiz, id=request.data['quiz'])
 
        if(
        UserResponse.objects.filter(user = user, question = question).count() == 0
        and quiz.isLive==True
        and pytz.UTC.localize(datetime.datetime.now()) <= quiz.end
        and pytz.UTC.localize(datetime.datetime.now()) >= quiz.begin
        ):
            obj = UserResponse(user = user, quiz = quiz, question = question, label = request.data['label'])
            obj.save()
            return Response({"message": "Response Submitted"}) 
        else:
            return Response({"message": "Quiz already taken or quiz is not live"})
        
class SubmitQuiz(generics.UpdateAPIView):
    serializer_class =  SubmitQuizSerializer
    permission_classes=[IsAuthenticated]
    
    
    def post(self, request, *args, **kwargs):
        user    = request.user
        quiz     = get_object_or_404(Quiz, id=request.data['quiz'])
        points =0
        if PointTable.objects.filter(user=user, quiz=quiz).count()!=0:
            return Response({"message":"quiz already submitted"}, status=HTTP_400_BAD_REQUEST)

        for question in Question.objects.filter(quiz = quiz):
            if UserResponse.objects.filter(user=user, question=question).count()==0:
                obj = UserResponse(
                    user = user,
                    quiz = quiz, 
                    question = question, 
                    label = "skipped")
                obj.save()
            else:
                if UserResponse.objects.filter(user=user, question=question).first().label==Choices.objects.filter(question=question, isCorrect=True).first().label:
                    points+=1

        obj = PointTable(user=user, quiz=quiz,score=points)
        obj.save()
        return Response({"message": "Quiz Submitted","points":points})




# def home(request):
#     context = {
#         'quizzes': Quiz.objects.all()
#     }
#     return render(request, 'quiz/home.html', context)   

# def about(request):
#     return render(request, 'quiz/about.html')
