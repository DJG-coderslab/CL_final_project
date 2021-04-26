from django.contrib import admin

# Register your models here.

from training.forms import QuestionForm, QuestionF
from training.models import Answer, Question


class AnswerInLine(admin.TabularInline):
    model = Answer
    insert_after = 'points'

    def get_formset(self, request, obj=None, **kwargs):
        breakpoint()

    # def form(self, *args, **kwargs):
    #     print("CLEAN!!!")
    #     super().form(*args, **kwargs)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    form = QuestionF
    fields = [
        'content',
        'points',
    ]
    inlines = [AnswerInLine]

# TODO może wyjściem jest napisanie własnych formularzy, na bazie modeli,
#  ale z zaimplementowaną własną metoda clean()?



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