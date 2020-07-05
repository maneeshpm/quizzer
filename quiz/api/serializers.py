from rest_framework import serializers
from quiz.models import Quiz, Question, Choices, UserResponse
from rest_framework.serializers import BooleanField
class QuizListSerializer(serializers.ModelSerializer):
    questionCount = serializers.SerializerMethodField(method_name='getQuestionCount')
    class Meta:
        model = Quiz
        fields = ["id","title","begin","end","isLive","questionCount"]
        read_only_fields = ["questionCount"]

    def getQuestionCount(self,obj):
        return obj.question_set.all().count()

class ChoiceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choices
        fields = ["id", "label"]



class QuestionListSerializer(serializers.ModelSerializer):
    choices_set = serializers.SerializerMethodField()
    # choices_set = ChoiceListSerializer(many=True)
  
    class Meta:
        model = Question
        fields = ["id", "text", "image","questionType","choices_set"]
    def get_choices_set(self, obj):
        if obj.questionType == 'text':
            return None
        else:
            return ChoiceListSerializer(obj.choices_set,many=True).data    
    

class QuizDetailSerializer(serializers.ModelSerializer):
    question_set = QuestionListSerializer(many=True)
    
    class Meta:
        model = Quiz
        fields = "__all__"
    
class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserResponse
        fields = [ "quiz", "question","label"]

class SubmitQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserResponse
        fields = ["quiz"]