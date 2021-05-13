from django.urls import path

from training import views as v
from training import api_views as api


app_name = 'training'

urlpatterns = [
    path('', v.StartView.as_view(), name='start'),
    path('question/', v.OneQuestionView.as_view(), name='one-question'),
    path('tmp-logout/', v.TmpLogout.as_view(), name='logout'),
    path('ok/', v.OkView.as_view(), name='ok'),
    path('register/', v.RegisterUserView.as_view(), name='register'),
    path('question-summary/', v.QuizSummaryView.as_view(),
         name='question-summary'),
    
    path('tmp/', v.Tmp.as_view(), name='tmp'),
    
    path('api/start/', api.StartView.as_view(), name='api-start'),
    path('api/register/<str:username>/', api.Register.as_view(),
         name='api-register'),
]
