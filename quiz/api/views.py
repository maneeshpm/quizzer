from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from django.http import Http404
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import HTTP_400_BAD_REQUEST,HTTP_200_OK
import datetime
import pytz

from quiz.models import (
    Quiz, 
    UserResponse, 
    Choices, 
    Question,
    PointTable
    )

from .serializers import (
    QuizListSerializer, 
    QuizDetailSerializer, 
    UserAnswerSerializer, 
    SubmitQuizSerializer
    )

# Retrieves a list of running quizzes ["GET"]
class QuizListAPIView(generics.ListAPIView):
    serializer_class = QuizListSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = Quiz.objects.filter()
        return queryset

# Retrieves details of a perticular quiz ["GET"]      
class QuizDetailAPIView(generics.RetrieveAPIView):
    serializer_class    = QuizDetailSerializer
    permission_classes  = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return Quiz.objects.get(id = pk, isLive = True)
        except:
            raise Http404

    def get(self, request, pk, format = None):
        quiz       = self.get_object(pk)
        serializer = QuizDetailSerializer(quiz)
        return Response(serializer.data)

# Submits the user ans for a perticular question ["POST"]
class SaveUserChoicesAPIView(generics.UpdateAPIView):
    serializer_class    = UserAnswerSerializer
    permission_classes  = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user     = request.user
        question = get_object_or_404(Question, id = request.data['question'])
        quiz     = get_object_or_404(Quiz, id = request.data['quiz'])

        if PointTable.objects.filter(user = user, quiz = quiz).count() != 0:
            return Response({"message":"Quiz already submitted."}, status=HTTP_400_BAD_REQUEST)

        if(
        quiz.isLive == True
        and pytz.UTC.localize(datetime.datetime.now()) <= quiz.end
        and pytz.UTC.localize(datetime.datetime.now()) >= quiz.begin
        ):
            if UserResponse.objects.filter(quiz = quiz, user = user, question = question).count()==0:
                obj = UserResponse(user = user, quiz = quiz, question = question, label = request.data['label'])
                obj.save()
            else:
                obj = UserResponse(user = user, quiz = quiz, question = question)
                obj.label = request.data['lable']
                obj.save()
            return Response({"message": "Response Submitted"}) 
        else:
            return Response({"message": "Quiz is not live"})

# Perform Final Submit, commit to the pointtable
class SubmitQuiz(generics.UpdateAPIView):
    serializer_class    =  SubmitQuizSerializer
    permission_classes  =[IsAuthenticated]
    
    
    def post(self, request, *args, **kwargs):
        user    = request.user
        quiz    = get_object_or_404(Quiz, id=request.data['quiz'])
        points  = 0
        
        if PointTable.objects.filter(user = user, quiz = quiz).count()!=0:
            return Response({"message":"Quiz already submitted."}, status=HTTP_400_BAD_REQUEST)

        for question in Question.objects.filter(quiz = quiz):
            if UserResponse.objects.filter(user = user, question = question).count() == 0:
                obj = UserResponse(
                    user     = user,
                    quiz     = quiz, 
                    question = question, 
                    label    = "skipped"
                    )
                obj.save()
            else:
                if UserResponse.objects.filter(user = user, question = question).first().label == Choices.objects.filter(question=question, isCorrect=True).first().label:
                    points += 1

        obj = PointTable(user = user, quiz = quiz, score = points)
        obj.save()

        return Response({"message": "Quiz Submitted","points":points})
