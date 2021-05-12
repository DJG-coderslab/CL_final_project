from rest_framework.response import Response
from rest_framework.views import APIView

from training import models, serializers


class StartView(APIView):
    def get(self, request, format=None):
        dat = serializers.StartPage(models.QuizDomain.objects.first()).data
        return Response(dat)


class Register(APIView):
    def post(self, request, username, format=None):
        print(username)
        return Response()
