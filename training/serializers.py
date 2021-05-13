from rest_framework import serializers

from training import models


class StartPage(serializers.ModelSerializer):
    class Meta:
        model = models.QuizDomain
        fields = ['description', 'manual']
        
    
class Quiz(serializers.ModelSerializer):
    question_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = models.Quiz
        fields = ['id', 'is_active', 'question_set']
