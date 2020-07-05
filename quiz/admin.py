from django.contrib import admin
import nested_admin
from .models import Quiz, Question, Choices, PointTable, UserResponse

class ChoicesInline(nested_admin.NestedTabularInline):
    model   = Choices
    extra   = 4
    max_num = 4

class QuestionInline(nested_admin.NestedTabularInline):
    model   = Question
    inlines = [ChoicesInline,]
    extra   = 5

class QuizAdmin(nested_admin.NestedModelAdmin):
    inlines = [QuestionInline,]

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question)
admin.site.register(Choices)
admin.site.register(PointTable)
admin.site.register(UserResponse)
