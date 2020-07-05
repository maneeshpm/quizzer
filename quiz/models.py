from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Quiz(models.Model):
    begin = models.DateTimeField()
    end = models.DateTimeField()
    title = models.CharField(max_length = 250)
    isLive = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Question(models.Model): 
    text = models.CharField(max_length = 250)
    image = models.ImageField(null=True, blank=True, default=None)
    questionType = models.CharField(choices=[('text','text'),('mcq','mcq')],max_length=100)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.text

class Choices(models.Model):
    label = models.CharField(max_length = 150)
    isCorrect = models.BooleanField(default=False) 
    question = models.ForeignKey(Question,on_delete=models.CASCADE)

    def __str__(self):
        return self.label

class UserResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, default = -1)
    time = models.DateTimeField(auto_now_add=True)
    label = models.CharField(max_length = 150)

    def __str__(self):
        return self.user.username + " => " + self.label

class PointTable(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    submitTime = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0)
    
    def __str__(self):
        return self.user.username + " => " + str(self.score)
