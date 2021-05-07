from django.contrib import admin

from training.forms import  QuestionF
from training.models import Answer, Question, QuizDomain


class AnswerInLine(admin.TabularInline):
    model = Answer
    insert_after = 'points'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    form = QuestionF
    fields = [
        'content',
        'points',
    ]
    inlines = [AnswerInLine]
    
    
@admin.register(QuizDomain)
class QuizDoaminAdmin(admin.ModelAdmin):
    model = QuizDomain