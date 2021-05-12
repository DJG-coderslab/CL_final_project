from rest_framework import serializers

from training import models


class StartPage(serializers.ModelSerializer):
    class Meta:
        model = models.QuizDomain
        fields = ['description', 'manual']
        
    
