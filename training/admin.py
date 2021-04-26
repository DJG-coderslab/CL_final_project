from django.contrib import admin

# Register your models here.

from training.forms import QuestionForm, QuestionF
from training.models import Answer, Question


class AnswerInLine(admin.TabularInline):
    model = Answer
    insert_after = 'points'

    # def get_formset(self, request, obj=None, **kwargs):
    #     breakpoint()

    # def form(self, *args, **kwargs):
    #     print("CLEAN!!!")
    #     super().form(*args, **kwargs)
    
    def save_existing_objects(self, commit=False):
        cd = self.cleaned_data()
        breakpoint()


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    form = QuestionF
    fields = [
        'content',
        'points',
    ]
    inlines = [AnswerInLine]
    
    def save_formset(self, request, form, formset, change):
        # if formset.model != Answer:
        #     return super(QuestionAdmin, self).save_formset(request, form,
        #                                                    formset, change)
        instances = formset.save(commit=False)
        for instance in formset.cleaned_data:
            print(f"I: {instance}")
        breakpoint()
    

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