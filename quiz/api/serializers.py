from rest_framework import serializers
from quiz.models import (
    Quiz, 
    Question, 
    Choices, 
    UserResponse
    )

# Quiz List Handling
class QuizListSerializer(serializers.ModelSerializer):
    questionCount = serializers.SerializerMethodField(method_name='getQuestionCount')
    
    class Meta:
        model = Quiz
        fields = [
            "id",
            "title",
            "begin",
            "end",
            "isLive",
            "questionCount"
            ]
        read_only_fields = ["questionCount"]

    def getQuestionCount(self,obj):
        return obj.question_set.all().count()

# List of Options if available
class ChoiceListSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Choices
        fields  = ["id", "label"]


# List of questions
class QuestionListSerializer(serializers.ModelSerializer):
    choices_set = serializers.SerializerMethodField()
  
    class Meta:
        model = Question
        fields = [
            "id", 
            "text", 
            "image",
            "questionType",
            "choices_set"
            ]
    def get_choices_set(self, obj):
        if obj.questionType == 'text':
            return None
        else:
            return ChoiceListSerializer(obj.choices_set, many = True).data    
    
# The Entire Quiz
class QuizDetailSerializer(serializers.ModelSerializer):
    question_set = QuestionListSerializer(many = True)
    
    class Meta:
        model   = Quiz
        fields  = "__all__"

# For handling user responses    
class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserResponse
        fields = [
            "quiz", 
            "question",
            "label"
            ]

# For handling user submissions TODO: integrate to UserAnswerSerializer
class SubmitQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserResponse
        fields = ["quiz"]