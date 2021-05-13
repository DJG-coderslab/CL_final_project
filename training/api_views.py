from django.contrib.auth import login
from rest_framework.response import Response
from rest_framework.views import APIView

from training import models, serializers, business_logic as bl


class StartView(APIView):
    def get(self, request, format=None):
        dat = serializers.StartPageSerializer(models.QuizDomain.objects.first()).data
        return Response(dat)


class Register(bl.Register, APIView):
    def post(self, request, username, format=None):
        print(username)
        employee = self.handle_register_data(form_data=request.data)
        login(self.request, employee)
        return Response()
