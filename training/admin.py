from django.contrib import admin

# Register your models here.

from training.forms import QuestionForm
from training.models import Question

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    form = QuestionForm
    