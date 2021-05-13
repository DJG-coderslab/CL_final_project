from rest_framework import serializers

from training import models


class StartPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.QuizDomain
        fields = ['description', 'manual']
        

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = ['id', 'content', 'is_correct']

    
class QuestionSerializer(serializers.ModelSerializer):
    answer_set = AnswerSerializer(many=True, read_only=True)
    
    class Meta:
        model = models.Question
        fields = ['id', 'content', 'answer_set']


class QuizSerializer(serializers.ModelSerializer):
    question_set = QuestionSerializer(many=True, read_only=True)
    
    class Meta:
        model = models.Quiz
        fields = ['id', 'is_active', 'question_set']


class OnlyQuiz(serializers.ModelSerializer):
    question_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = models.Quiz
        fields = ['id', 'is_active', 'question_set']
