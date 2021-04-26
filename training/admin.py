from django.contrib import admin

# Register your models here.

from training.forms import QuestionForm
from training.models import Answer, Question


class AnswerInLine(admin.TabularInline):
    model = Answer
    insert_after = 'points'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    # form = QuestionForm
    fields = [
        'content',
        'points',
    ]
    inlines = [AnswerInLine]




# admin.site.register(Question)

    # def save_model(self, request, obj, form, change):
    #     for field in form:
    #         print(f"F: {field}")
    #         # print(f"f: {field.get('ans1')}")
    #
    #     breakpoint()

    # fieldsets = (
    #     (None, {
    #         'fields': ('content', 'points')
    #     }),
    #     ('Advanced options', {
    #         'classes': ('collapse',),
    #         'fields': ('answer_set', )
    #     }),
    # )