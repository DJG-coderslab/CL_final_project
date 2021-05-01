from django.urls import path

from training import views as v


app_name = 'training'

urlpatterns = [
    path('tmp/', v.Tmp.as_view(), name='tmp'),
    path('tmp-logout/', v.TmpLogout.as_view(), name='logout'),
    path('ok/', v.OkView.as_view(), name='ok'),
    path('register/', v.RegisterUserView.as_view(), name='register'),
]
