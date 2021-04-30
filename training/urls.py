from django.urls import path

from training import views as v


app_name = 'training'

urlpatterns = [
    # path('tmp/', v.Tmp.as_view(), name='tmp'),
    path('ok/', v.OkView.as_view(), name='ok'),
    path('register/', v.RegisterUserView.as_view(), name='register'),
]
